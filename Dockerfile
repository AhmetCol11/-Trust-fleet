# Python tabanlı resmi imajı kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli sistem paketlerini kur (SQLite için gerekli derleyiciler vb.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Portu dışarı aç
EXPOSE 5000

# Çevre değişkenlerini ayarla
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Uygulamayı başlat
CMD ["python", "run.py"]
