# Python tabanlı resmi imajı kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli sistem paketlerini kur
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
ENV PYTHONUNBUFFERED=1

# Uygulamayı gunicorn ile başlat (docker-compose command ile override edilebilir)
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "run:app"]
