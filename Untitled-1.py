%cd /content
!git clone https://github.com/comfyanonymous/ComfyUI /content/ComfyUI
!git clone https://github.com/city96/ComfyUI-GGUF /content/ComfyUI/custom_nodes/ComfyUI-GGUF
!pip install torchsde gguf

!apt install aria2 -qqy
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/city96/Wan2.1-T2V-14B-gguf/resolve/main/wan2.1-t2v-14b-Q3_K_S.gguf -d /content/ComfyUI/models/unet -o wan2.1-t2v-14b-Q3_K_M.gguf
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/city96/umt5-xxl-encoder-gguf/resolve/main/umt5-xxl-encoder-Q3_K_S.gguf -d /content/ComfyUI/models/clip -o umt5-xxl-encoder-Q3_K_M.gguf
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors -d /content/ComfyUI/models/vae -o/wan_2.1_vae.safetensors
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/vrgamedevgirl84/Wan14BT2VFusioniX/resolve/main/FusionX_LoRa/Wan2.1_T2V_14B_FusionX_LoRA.safetensors -d /content/ComfyUI/models/loras/FusionX -o Wan2.1_T2V_14B_FusionX_LoRA.safetensors
%cd /content/ComfyUI
!apt-get install -y ffmpeg
!pip install av
import asyncio
await load_custom_node("/content/ComfyUI/custom_nodes/ComfyUI-GGUF")

import torch
import random, time
from PIL import Image
import numpy as np

from nodes import NODE_CLASS_MAPPINGS, load_custom_node
from comfy_extras import nodes_hunyuan, nodes_model_advanced

load_custom_node("/content/ComfyUI/custom_nodes/ComfyUI-GGUF")

UnetLoaderGGUF = NODE_CLASS_MAPPINGS["UnetLoaderGGUF"]()
CLIPLoaderGGUF = NODE_CLASS_MAPPINGS["CLIPLoaderGGUF"]()
LoraLoaderModelOnly = NODE_CLASS_MAPPINGS["LoraLoaderModelOnly"]()
VAELoader = NODE_CLASS_MAPPINGS["VAELoader"]()

CLIPTextEncode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
EmptyHunyuanLatentVideo = nodes_hunyuan.NODE_CLASS_MAPPINGS["EmptyHunyuanLatentVideo"]()

KSampler = NODE_CLASS_MAPPINGS["KSampler"]()
ModelSamplingSD3 = nodes_model_advanced.NODE_CLASS_MAPPINGS["ModelSamplingSD3"]()
VAEDecode = NODE_CLASS_MAPPINGS["VAEDecode"]()

with torch.inference_mode():
    unet = UnetLoaderGGUF.load_unet("wan2.1-t2v-14b-Q3_K_M.gguf")[0]
    clip = CLIPLoaderGGUF.load_clip("umt5-xxl-encoder-Q3_K_M.gguf", "wan")[0]
    lora = LoraLoaderModelOnly.load_lora_model_only(unet, "FusionX/Wan2.1_T2V_14B_FusionX_LoRA.safetensors", 1.0)[0]
    vae = VAELoader.load_vae("wan_2.1_vae.safetensors")[0]

import torch, random, time
from PIL import Image
import numpy as np
import imageio

with torch.inference_mode():
    # ==== Thông số sinh video ====
    seed = 0
    steps = 20                # nhiều steps hơn cho video mượt hơn
    cfg = 1.5                 # classifier-free guidance
    sampler_name = "euler"
    scheduler = "beta"
    width = 720               # giảm width để tiết kiệm VRAM
    height = 480
    fps = 8
    seconds = 8
    length = fps * seconds    # số frame = 8 giây × 8 fps = 64

    positive_prompt = (
        "A stop-motion style short film featuring two clay characters sitting at a small studio "
    "table under bright TV studio lights, speaking to each other about science. The scene "
    "looks like a live television broadcast, with a professional camera pointing at them. "
    "The clay figures move with slight handmade animation imperfections, giving an authentic "
    "stop-motion feel. The atmosphere is playful yet educational, like a children’s science show. "
    "Their clay faces are expressive, mouths moving clearly as they exchange scientific ideas. "
    "Lighting is cinematic, warm and well-balanced, resembling a TV talk show set. "
    "Camera motion: slow pan left, slow pan right, cinematic dolly in, smooth zoom, alternating "
    "between medium shot and close-up, steady framing, subtle stop-motion style frame jitter."
)
    negative_prompt = (
        "distorted faces, extra limbs, glitch textures, broken clay surface, low quality, blurry, "
    "noisy, bad hands, malformed body, unnatural camera movement, inconsistent character design, "
    "flickering frames, overexposed lighting, wrong perspective, static frame, messy background, "
    "poor anatomy, extra fingers, duplicate body parts, frozen scene"

    )

    # ==== Encode prompt ====
    positive = CLIPTextEncode.encode(clip, positive_prompt)[0]
    negative = CLIPTextEncode.encode(clip, negative_prompt)[0]

    # ==== Patch model với LoRA ====
    model = ModelSamplingSD3.patch(lora, 1.0)[0]

    # ==== Tạo latent video ====
    latent_video = EmptyHunyuanLatentVideo.generate(width, height, length)[0]

    # ==== Random seed ====
    if seed == 0:
        random.seed(int(time.time()))
        seed = random.randint(0, 18446744073709551615)

    # ==== Sampling ====
    samples = KSampler.sample(
        model, seed, steps, cfg, sampler_name, scheduler,
        positive, negative, latent_video
    )[0]

    # ==== Decode thành video frames ====
    decoded = VAEDecode.decode(vae, samples)[0].detach().cpu()
    frames = (decoded.numpy() * 255).astype(np.uint8)  # shape: [frames, H, W, C]

    # ==== Xuất video mp4 ====
    video_path = "/content/testvideo.mp4"
    imageio.mimsave(video_path, frames, fps=fps, quality=8)

print("🎬 Video saved to", video_path)
