# Gunakan image Python ringan
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin file requirements terlebih dahulu untuk caching
COPY requirements.txt .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Buka port Flask (5000)
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
