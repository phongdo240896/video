# Sử dụng Python 3.9
FROM python:3.9-slim

# Cài đặt FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép các tệp cần thiết
COPY requirements.txt requirements.txt
COPY app.py app.py

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Chạy ứng dụng
CMD ["python", "app.py"] 