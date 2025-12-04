# Použijeme oficiálny Python image
FROM python:3.11-slim

# Nastavíme pracovný adresár
WORKDIR /app

# Skopírujeme requirements a nainštalujeme závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopírujeme celý projekt
COPY . .

# Gunicorn bude počúvať na porte, ktorý Render nastaví v premennej PORT
# Zvýšime timeout, aby sa deploy neukončil predčasne
CMD gunicorn -b 0.0.0.0:$PORT app:app --timeout 120
