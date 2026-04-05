from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # عشان يشتغل في الخلفية بدون شاشة
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver

@app.route('/')
def home():
    return "Baraa Robot: System is Ready for Scraping!"

@app.route('/login_test')
def login_test():
    try:
        driver = setup_browser()
        driver.get("https://takipcibase.com/")
        # هنا بنخلي الروبوت يدور على زرار تسجيل الدخول
        title = driver.title
        driver.quit()
        return jsonify({"status": "Success", "page_title": title})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)