from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import subprocess
import threading
import tempfile

app = Flask(__name__)
CORS(app)

# API Key — read from env var for security, fallback for local dev
API_KEY = os.environ.get("GEMINI_KEY", "AIzaSyCozzvnEINgCyA18MxhEXbKGr60-qpmjd0")
genai.configure(api_key=API_KEY)

# gemini-flash-latest: Most stable flash model
model = genai.GenerativeModel('gemini-flash-latest')

# --- وظيفة تشغيل بايثون الحقيقي ---
@app.route('/run-python', methods=['POST'])
def execute_python():
    try:
        data = request.json
        code = data.get("code", "")
        
        if not code:
            return jsonify({"output": "الرجاء كتابة كود بايثون لتنفيذه."})

        # إنشاء ملف مؤقت للكود
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        # تنفيذ الكود في بيئة معزولة (timeout 5 ثواني)
        result = subprocess.run(
            ['python3', tmp_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        os.remove(tmp_path)
        output = result.stdout if result.stdout else result.stderr
        return jsonify({"output": output if output else "تم تنفيذ الكود بنجاح (لا يوجد مخرجات نصية)."})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "خطأ: تجاوز الكود الوقت المسموح به للتنفيذ (5 ثوانٍ)."})
    except Exception as e:
        return jsonify({"output": f"خطأ تقني أثناء التشغيل: {str(e)}"})

# --- وظيفة تشغيل الـ Terminal (ttyd) ---
def start_terminal():
    try:
        subprocess.Popen(["ttyd", "-p", "7681", "bash"])
        print("[SYSTEM]: Linux Terminal Lab started on port 7681")
    except Exception as e:
        print(f"[TERMINAL ERROR]: Could not start ttyd: {e}")

# --- الوظيفة المطورة: Robbie الذكي المتخصص والمتوافق ---
@app.route('/ask', methods=['POST'])
def ask_tutor():
    try:
        data = request.json
        if not data:
            return jsonify({"answer": "لم أستلم أي بيانات.", "response": "لم أستلم أي بيانات."}), 400
            
        # دعم الاسمين 'question' و 'message' لضمان التوافق مع كل نسخ الكود
        question = data.get("question") or data.get("message")
        if not question:
            return jsonify({"answer": "لم أستلم أي سؤال.", "response": "لم أستلم أي سؤال."}), 400

        # استقبال نوع المختبر لضبط شخصية Robbie
        lab_type = data.get('lab_type', 'default').lower()
        
        # قواميس الشخصيات (System Contexts) لإبهار الحكام
        prompts = {
            "cisco": "أنت Robbie، خبير شبكات سيسكو في مختبر جامعة البلقاء (FET). ساعد الطالب في أوامر CLI والراوترات بأسلوب تقني دقيق ومختصر.",
            "kali": "أنت Robbie، خبير أمن سيبراني في مختبر جامعة البلقاء (FET). ساعد الطالب في أدوات الاختراق الأخلاقي والتحليل بأسلوب احترافي.",
            "python": "أنت Robbie، مدرب برمجة بايثون في مختبر جامعة البلقاء (FET). ساعد الطالب في تصحيح الكود وشرح المنطق البرمجي.",
            "default": "أنت Robbie، المساعد الذكي لمختبر Cloud-Native Digital Lab في جامعة البلقاء التطبيقية (FET). خبير في الأمن السيبراني والبرمجة."
        }
        
        system_context = prompts.get(lab_type, prompts["default"])
        full_prompt = f"{system_context}\nسؤال الطالب: {question}"
        
        # توليد الرد من Gemini
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            # إرجاع answer و response معاً لضمان عمل الواجهة القديمة والجديدة بدون تعديل
            return jsonify({
                "answer": response.text, 
                "response": response.text
            })
        else:
            error_fallback = "عذراً، لم أتمكن من صياغة رد حالياً."
            return jsonify({
                "answer": error_fallback,
                "response": error_fallback
            })
            
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            error_msg = "⚠️ عذراً! Robbie يحتاج لاستراحة قصيرة (تجاوز حصة الاستخدام). يرجى المحاولة بعد دقيقة واحدة."
        else:
            error_msg = f"⚠️ Robbie يواجه تحدياً تقنياً: {error_str}"
        
        return jsonify({
            "answer": error_msg, 
            "response": error_msg
        }), 200

if __name__ == "__main__":
    # تشغيل الـ Terminal في Thread منفصل لضمان عدم توقف السيرفر
    terminal_thread = threading.Thread(target=start_terminal)
    terminal_thread.daemon = True
    terminal_thread.start()

    # تشغيل سيرفر الـ API على البورت الممرر من Cloud Run (افتراضي 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)