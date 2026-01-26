from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

URL_WEBPAGE = "https://www.tottus.com.pe/tottus-pe/lista/CATG16815/Arroz"

# RUTA ABSOLUTA DEL PROYECTO

product = {
    'product_1': 'Arroz'
}

def get_params():
    return {
        'url_login': URL_WEBPAGE
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

def go_to_webpage(browser, web_page):
    browser.get(web_page)



browser = get_browser()
go_to_webpage(browser, URL_WEBPAGE)
#display_screenshot(path_png)

def collect_products_from_page(browser):
    print("Esperando productos...")
    list_dict = list()

    # 1. Buscar productos con XPATH estable 
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
    for e_product in e_products:
        
        dict_data = {}  
        dict_data['product_link'] = e_product.find_element(By.XPATH, './a').get_attribute('href')  
        dict_data['product_descripcion'] = e_product.find_element(By.XPATH, './a/div[2]/div/b').text
        dict_data['product_marca'] = e_product.find_element(By.XPATH, './a/div[2]/div/div/b').text
        #dict_data['product_precio'] = e_product.find_element(By.XPATH, './a/div[3]/div/ol/li/div/span[1]').text
        prices = e_product.find_elements(
            By.XPATH,
            './/ol[contains(@class,"pod-prices")]//li'
        )

        
        precio_anterior = "N/A"
        precio = "N/A"        
        precio_cmr = "N/A"

        for price in prices:
            try:
                text_price = price.find_element(By.XPATH, './/span[1]').text.strip()

                if price.get_attribute("data-cmr-price"):
                    precio_cmr = text_price

                elif price.get_attribute("data-internet-price"):
                    precio = text_price
                
            except:
                continue

        dict_data['precio_cmr'] = precio_cmr
        dict_data['precio'] = precio
        dict_data['precio_anterior'] = precio_anterior
        
        # Definiendo nueva ventana
        browser.execute_script('window.open();')
        window_before = browser.window_handles[0]
        window_after = browser.window_handles[1]

        # Cambiando de ventana
        browser.switch_to.window(window_after)

        # Desarrollamos el codigo
        browser.get(dict_data['product_link'])
        #time.sleep(2)


        #obtener imagen
        xpath_img = '//div[@id="breadcrumb"]/following-sibling::div[1]/section/div/div/div/img' 
        e_img = browser.find_elements(By.XPATH, xpath_img)
        dict_data['product_imagen'] = e_img[0].get_attribute("src") if e_img else "N/A"
       

        specs = {}

        rows = browser.find_elements(
            By.XPATH,
            '//table[contains(@class,"specification-table")]//tr'
        )

        for row in rows:
            try:
                key = row.find_element(By.CLASS_NAME, "property-name").text.strip()
                value = row.find_element(By.CLASS_NAME, "property-value").text.strip()
                specs[key] = value
            except:
                continue

        dict_data['presentacion']  = specs.get("Presentación", "N/A")
        dict_data['tipo_arroz']    = specs.get(f"Tipo de {product['product_1']}", "N/A")
        dict_data['tipo_producto'] = specs.get("Tipo de Producto", "N/A")
        dict_data['contenido']     = specs.get("Contenido", "N/A")
        dict_data['formato']       = specs.get("formato", "N/A")
      

        # Cerrando pestaña actual
        browser.close()

        # Regresando a pestaña inicial
        browser.switch_to.window(window_before)

        
        list_dict.append(dict_data)
    return list_dict
           
#data = collect_products_from_page(browser)

def collect_all_products(browser):
    all_products = []
    wait = WebDriverWait(browser, 15)
    while True:
        # 1. Extraer productos
        page_products = collect_products_from_page(browser)
        if page_products:
            all_products.extend(page_products)

        # 2. Buscar botón siguiente
        try:
            btn_next = browser.find_element(
                By.ID,
                "testId-pagination-bottom-arrow-right"
            )
        except:
            print("No existe botón siguiente")
            break

        # 3. Verificar si está deshabilitado
        if btn_next.get_attribute("disabled"):
            print("Última página alcanzada")
            break

        # 4. Esperar y capturar primer producto actual
        try:
            first_product = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="testId-searchResults-products"]/div[1]')
                )
            )
        except:
            print("No se pudo identificar el primer producto")
            break

        # 5. Click en siguiente
        browser.execute_script("arguments[0].click();", btn_next)

        # 6. Esperar que cambie el DOM
        wait.until(EC.staleness_of(first_product))

        # 7. Esperar nuevos productos
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="testId-searchResults-products"]/div')
            )
        )

    return all_products


data = collect_all_products(browser)
print(data)

for idx, item in enumerate(data, start=1):
    print(f"{idx}. {item['product_link']}\n"
          f"   descripcion: {item['product_descripcion']}\n"
          f"   marca: {item['product_marca']}\n"
          f"   precio_anterior: {item['precio_anterior']}\n"
          f"   precio_internet: {item['precio']}\n"
          f"   precio_tarjeta: {item['precio_cmr']}\n"        
          
          f"   imagen: {item['product_imagen']}\n"
          f"   presentacion: {item['presentacion']}\n"
          f"   tipo: {item['tipo_arroz']}\n"
          f"   tipo_producto: {item['tipo_producto']}\n"
          f"   contenido: {item['contenido']}\n"
          f"   formato: {item['formato']}\n"
          
          )