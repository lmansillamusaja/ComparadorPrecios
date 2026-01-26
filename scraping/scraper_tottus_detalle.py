from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

URL_WEBPAGE = "https://www.tottus.com.pe/tottus-pe/articulo/115807081/mezcla-lactea-ideallight-lata-390-g/115807082"

# RUTA ABSOLUTA DEL PROYECTO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_OUTPUTS = os.path.join(BASE_DIR, "outputs")
FUENTE = "tottus_scrape"
WAIT_TIME = 10
def get_params():
    return {
        'url_login': URL_WEBPAGE,
        'path_png': os.path.join(PATH_OUTPUTS, f'{FUENTE}.png')
    }

def get_browser():
    options = Options()
    # options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1100, 750)
    return browser

def go_to_webpage(browser, web_page):
    browser.get(web_page)

def display_screenshot(path_png):
    # Crear carpeta
    os.makedirs(os.path.dirname(path_png), exist_ok=True)

    # Guardar PNG
    ok = browser.save_screenshot(path_png)
    print("¿Screenshot guardado?:", ok)
    print("Guardado en:", path_png)

    # Abrir imagen
    os.startfile(path_png)

dict_params = get_params()
path_png = dict_params['path_png']

browser = get_browser()
go_to_webpage(browser, URL_WEBPAGE)
#display_screenshot(path_png)

def collect_products_from_page(browser):
    print("Esperando productos...")
    list_dict = list()

    # 1. Intentar cerrar cookies
    try:
        btn_cookie = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Aceptar')]"))
        )
        btn_cookie.click()
        print("Cookies aceptadas.")
    except:
        pass

    # 2. Intentar cerrar selección de tienda
    try:
        btn_store = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Seleccionar tienda')]"))
        )
        btn_store.click()
        print("Modal de tienda cerrado.")
    except:
        pass

    # 3. Hacer scroll para forzar carga de productos
    browser.execute_script("window.scrollTo(0, 800);")
    time.sleep(2)

    # 4. Buscar productos con XPATH estable
    xpath_products = '//div[@id="breadcrumb"]/following-sibling::div[1]/section/div/div/div/img' 
    #'[@id="testId-pod-image-4babc503-ab22-49e2-b25a-b07280eb0d97"]'
    wait = WebDriverWait(browser, 10)

    try:
        elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_products))
        )
    except:
        print("No se encontraron productos.")
        return

    print("Productos encontrados:", len(elements))
    print("=======================")

    for e in elements:
        print(e.get_attribute("src"))
        
         

        # Regresando a pestaña inicial
       

        
        
    return list_dict

               

collect_products_from_page(browser)
