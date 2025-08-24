import os
import whisper
import torch

# 🔧 Chọn thiết bị (ưu tiên MPS của Apple Silicon)
device = "mps" if torch.backends.mps.is_available() else "cpu"
print("💻 Đang chạy trên:", device)

# 📦 Load model (small cho nhanh, có thể đổi thành "medium" nếu muốn)
model = whisper.load_model("small", device=device)


def transcribe_video(file_path, output_txt_path, output_srt_path, target_lang="vi"):
    print(f"🗂 Đang xử lý: {file_path}")
    
    # 📝 Chạy dịch/nhận diện
    if target_lang == "en":
        result = model.transcribe(file_path, task="translate", fp16=False)
    else:
        result = model.transcribe(file_path, language=target_lang, fp16=False)

    # Lưu dạng TXT
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"✅ Đã lưu: {output_txt_path}")

    # Lưu dạng SRT
    if "segments" in result:
        with open(output_srt_path, "w", encoding="utf-8") as srt_file:
            for i, seg in enumerate(result["segments"], 1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        print(f"🎬 Đã lưu phụ đề: {output_srt_path}")


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def process_folder(folder_path, target_lang="vi"):
    video_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('.mp4', '.mov', '.mkv', '.avi', '.flv'))
    ]
    total = len(video_files)

    if total == 0:
        print("❗ Không tìm thấy video hợp lệ trong thư mục.")
        return

    for idx, filename in enumerate(video_files, 1):
        video_path = os.path.join(folder_path, filename)
        base = os.path.splitext(video_path)[0]
        txt_path = base + "_translated.txt"
        srt_path = base + "_translated.srt"
        transcribe_video(video_path, txt_path, srt_path, target_lang)

        percent = int((idx / total) * 100)
        print(f"📊 Tiến độ: {idx}/{total} ({percent}%)\n")


# 🚀 Giao diện nhập
if __name__ == "__main__":
    folder = input("📁 Nhập đường dẫn tới thư mục chứa video: ").strip()
    lang = input("🌐 Ngôn ngữ đầu ra (mã ISO, ví dụ: vi, en, ja...): ").strip().lower()

    if os.path.isdir(folder):
        process_folder(folder, lang)
    else:
        print("❌ Đường dẫn không hợp lệ.")
