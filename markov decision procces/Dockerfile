# Resmi Python 3.9 tabanlı bir image'i temel alıyoruz
FROM python:3.9

# Bağımlılıkların yüklenmesi için gerekenler
RUN apt-get update --fix-missing && apt-get install -y \
    python3-dev \
# Pygame için resim yükleme desteği.
    libsdl2-image-dev \
# Pygame için TrueType font renderlama desteği.
    libsdl2-ttf-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

# Çalışma dizinini ayarla
WORKDIR /usr/src/app
# Python bağımlılıklarını yükle
COPY requirements.txt .
COPY images/ images/

RUN pip install --no-cache-dir -r requirements.txt
#Pygame default ALSA seslerinin cikarilmasi (sessiz uygulama)
RUN echo "pcm.!default { type hw card 0 }" > /etc/asound.conf
RUN echo "ctl.!default { type hw card 0 }" >> /etc/asound.conf

# XDG_RUNTIME_DIR ortam değişkenini ayarla
ENV XDG_RUNTIME_DIR=/tmp/runtime-dir
RUN mkdir -p $XDG_RUNTIME_DIR && chmod 0700 $XDG_RUNTIME_DIR

# Kod dosyalarını kopyala
COPY . .

# Uygulamayı çalıştır
CMD ["python", "MDP neco.py"]
