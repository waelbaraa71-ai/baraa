from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

def setup_browser():
    # إعدادات المتصفح عشان يشتغل على السيرفر بدون شاشة (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # تحميل وتسطيب الكروم درايفر أوتوماتيكياً
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@app.route('/')
def home():
    return "<h1>Baraa Robot is Live!</h1><p>Use /attack to start.</p>"

@app.route('/attack')
def attack():
    driver = None
    try:
        driver = setup_browser()
        # الدخول للموقع التركي
        driver.get("https://takipcibase.com/")
        
        # تصوير الصفحة أو سحب العنوان للتأكد
        title = driver.title
        
        # محاولة العثور على أزرار الدخول (بالتركي Giriş Yap)
        return jsonify({
            "status": "Success",
            "message": "Connected to Turkish Site",
            "page_title": title,
            "system": "Baraa Engine v1.0"
        })
    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": str(e)
        })
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # تشغيل السيرفر على البورت اللي Railway بيحدده
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)