# المرحلة الأولى: مرحلة البناء (Build Stage)
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .

# تثبيت curl لتحميل أدوات المختبر والمكتبات
RUN apt-get update && apt-get install -y curl && \
    pip install --user --no-cache-dir -r requirements.txt

# المرحلة الثانية: مرحلة التشغيل النهائية (Final Stage)
FROM python:3.13-slim
WORKDIR /app

# 1. تثبيت أدوات اللينكس الأساسية، ttyd، و Ngrok
RUN apt-get update && apt-get install -y \
    bash \
    net-tools \
    iputils-ping \
    curl \
    git \
    vim \
    gnupg && \
    # تثبيت ttyd
    curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.x86_64 -o /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd && \
    # تثبيت Ngrok
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok && \
    rm -rf /var/lib/apt/lists/*

# 2. إعداد المستخدم (labuser) للأمان
RUN groupadd -r labuser && useradd -m -r -g labuser labuser

# 3. نسخ المكتبات والملفات من المرحلة الأولى
COPY --from=builder /root/.local /home/labuser/.local
COPY . .

# 4. منح الصلاحيات لضمان عمل الأدوات بدون أخطاء Permission Denied
RUN chown -R labuser:labuser /app && \
    chown labuser:labuser /usr/local/bin/ttyd && \
    # العثور على مسار ngrok وتغيير ملكيته
    chown labuser:labuser $(which ngrok)

USER labuser

# 5. إعدادات البيئة والمنافذ (الربط بين الشات بوت والتيرمينال)
ENV PATH=/home/labuser/.local/bin:$PATH

# مفتاح Gemini (سيستخدمه Robbie للرد على الطلاب)
ENV GEMINI_KEY="AIzaSyB4DqnmzAUdrsUNyeiXERKIEFG-LdbwEWA"

# البورت 8080 للـ API والبورت 7681 للـ Terminal (ttyd)
EXPOSE 8080 7681

# 6. تشغيل السيرفر الأساسي (tutor_service.py)
# السيرفر مبرمج داخلياً ليشغل ttyd في الخلفية تلقائياً
CMD ["sh", "-c", "python3 tutor_service.py"]