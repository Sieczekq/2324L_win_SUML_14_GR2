# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.10

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Zainstaluj niezbędne zależności
RUN apt-get -y update && \
    apt-get install -y \
    python3-dev \
    apt-utils \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Zaktualizuj setuptools i zainstaluj zależności Pythona
RUN pip3 install --upgrade setuptools && \
    pip3 install \
    cython==3.0.6 \
    numpy==1.26.0 \
    pandas==2.1.3

# Skopiuj requirements.txt i zainstaluj pakiety Pythona
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Skopiuj resztę kodu aplikacji
COPY . .

# Zdefiniuj numer portu, który kontener powinien eksponować
ENV PORT 8000

# Eksponuj określony port
EXPOSE 8000

# Polecenie do uruchomienia aplikacji
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
