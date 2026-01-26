from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from IPython.display import Image

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_WEBPAGE = 'https://www.tottus.com.pe/tottus-pe/lista/CATG16782/Leches'
WAIT_TIME = 30


def get_browser():
  """Crea y retorna un navegador en modo headless."""
  chrome_options = Options()

  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=chrome_options)
  # browser.maximize_window()
  browser.set_window_size(1100, 750)

  return browser