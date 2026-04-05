import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # تحديد مسار الكروم والدرايفر اللي نزلوا عن طريق railway.json
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    # هنا بنقوله استخدم الدرايفر اللي موجود في السيرفر مباشرة
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@app.route('/')
def home():
    return "<h1>Baraa Robot: Ready for Action!</h1>"

@app.route('/attack')
def attack():
    driver = None
    try:
        driver = setup_browser()
        driver.get("https://takipcibase.com/")
        title = driver.title
        return jsonify({
            "الحالة": "نجاح",
            "الموقع": "TakipciBase",
            "عنوان_الصفحة": title,
            "الرسالة": "الروبوت اخترق الموقع بنجاح!"
        })
    except Exception as e:
        return jsonify({
            "الحالة": "خطأ",
            "الرسالة": str(e)
        })
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)