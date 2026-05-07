# 1. اختيار نسخة كالي لينكس الرسمية الخفيفة
FROM kalilinux/kali-rolling:latest

# 2. منع الرسائل التفاعلية أثناء التثبيت لضمان استقرار البناء
ENV DEBIAN_FRONTEND=noninteractive

# 3. تحديث النظام وتثبيت الواجهة الرسومية (XFCE) وأدوات الوصول عبر المتصفح
# اخترنا XFCE لأنها تستهلك أقل قدر ممكن من الـ RAM والمعالج
RUN apt-get update && apt-get install -y \
    kali-desktop-xfce \
    kasmvncserver \
    dbus-x11 \
    sudo \
    nmap \
    && apt-get clean

# 4. إعداد مستخدم "طالب" لضمان أمان النظام (Best Practice)
RUN useradd -m -s /bin/bash student && \
    echo "student:password123" | chpasswd && \
    adduser student sudo

# 5. ضبط إعدادات البيئة للمستخدم
USER student
WORKDIR /home/student

# 6. فتح منفذ 6901 (المنفذ الافتراضي لـ KasmVNC للوصول عبر المتصفح)
EXPOSE 6901

# 7. تشغيل خادم الواجهة الرسومية عند تشغيل الحاوية
CMD ["vncserver", "-select-column", "1", "-o", "-SecurityTypes", "None", "-httpd", "/usr/share/kasmvnc/www", ":1"]