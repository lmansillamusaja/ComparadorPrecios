from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def get_browser(headless=False):

    options = Options()
    if headless:
        options.add_argument("--headless=new")

    # Flags para evitar bloqueos y logs de Chrome
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=OptimizationGuideModelDownloading")

    # Quitar logs molestos
    options.add_argument("--log-level=3")                     # solo errores graves
    options.add_argument("--v=0")                             # sin verbose
    options.add_argument("--disable-logging")                 # sin logging global
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Silenciar logs de ChromeDriver
    #service = Service(log_output=os.devnull)
     # browser.maximize_window()
    #browser.set_window_size(1100, 750)
    # Crear driver
    #driver = webdriver.Chrome(options=options, service=service)

    browser = webdriver.Chrome(options=options)
    # browser.maximize_window()
    browser.set_window_size(1100, 750)

    return browser