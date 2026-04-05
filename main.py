import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

app = Flask(__name__)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # محاولة تشغيل الكروم بأي طريقة متاحة في السيرفر
    try:
        # دي بتخلي السيرفر يحمل الدرايفر المناسب أوتوماتيكياً
        driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        # لو فشلت الطريقة الأولى، بيجرب المسار الافتراضي للينكس
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
        return jsonify({
            "status": "Success",
            "message": "Robot connected successfully!",
            "page_title": driver.title
        })
    except Exception as e:
        return jsonify({"status": "Error", "msg": str(e)})
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))