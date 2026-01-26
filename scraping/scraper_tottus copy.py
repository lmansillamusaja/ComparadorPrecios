from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

URL_WEBPAGE = "https://www.tottus.com.pe/tottus-pe/lista/CATG16782/Leches"

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
  """Crea y retorna un navegador en modo headless."""
  chrome_options = Options()

  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=chrome_options)
  # browser.maximize_window()
  browser.set_window_size(1100, 750)

  return browser

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
    #time.sleep(2)

    # 4. Buscar productos con XPATH estable
    xpath_products = '//*[@id="testId-searchResults-products"]/div[contains(@class, "grid-pod")]'
    wait = WebDriverWait(browser, 10)

    try:
        e_products = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_products))
        )
    except:
        print("No se encontraron productos.")
        return

    print(f"Productos encontrados: {len(e_products)}")           
    print("=======================")
    # 5. Obtener texto o datos
    for e_product in e_products[3]:
        dict_data = {}  
        dict_data['product_link'] = e_product.find_element(By.XPATH, './a').get_attribute('href')

        #imgs = e_product.find_elements(By.XPATH, './a/div[1]/div[1]/section/picture[1]/img')
        #dict_data['product_imagen'] = imgs[0].get_attribute("src") if imgs else "none"     

       
        dict_data['product_marca'] = e_product.find_element(By.XPATH, './a/div[2]/div/div/b').text
        dict_data['product_precio'] = e_product.find_element(By.XPATH, './a/div[3]/div/ol/li/div/span[1]').text
        
            # Definiendo nueva ventana
        browser.execute_script('window.open();')
        window_before = browser.window_handles[0]
        window_after = browser.window_handles[1]

        # Cambiando de ventana
        browser.switch_to.window(window_after)

        # Desarrollamos el codigo
        browser.get(dict_data['product_link'])
        #time.sleep(2)

        #obtener preesntacion        
        xpath_presentacion = '//table[@class="jsx-513032616 specification-table "]/tbody/tr/td[2]'
        e_desc = browser.find_elements(By.XPATH, xpath_presentacion)
        dict_data['presentacion'] = e_desc[0].text

        xpath_img = '//div[@id="breadcrumb"]/following-sibling::div[1]/section/div/div/div/img' 
        e_img = browser.find_elements(By.XPATH, xpath_img)
        dict_data['product_imagen'] = e_img[0].get_attribute("src")
       

            # Cerrando pestaña actual
        browser.close()

        # Regresando a pestaña inicial
        browser.switch_to.window(window_before)

        
        list_dict.append(dict_data)
    return list_dict

               

data = collect_products_from_page(browser)
for idx, item in enumerate(data, start=1):
    print(f"{idx}. {item['product_link']}\n"
          f"   Presentación: {item['presentacion']}\n"
          f"   Marca: {item['product_marca']}\n"
          f"   Precio: {item['product_precio']}\n"
          f"   Imagen: {item['product_imagen']}\n"
          
          )