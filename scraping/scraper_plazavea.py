from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

URL_WEBPAGE = "https://www.plazavea.com.pe/abarrotes/arroz"

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

   
    xpath_products = '//div[contains(@class,"ga-product-item")]'
    wait = WebDriverWait(browser, 15)
    try:
        e_products = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_products))
        )
    except:
        print("No se encontraron productos.")
        return

   

    print(f"Productos encontrados: {len(e_products)}")
    print("=======================")

    for e_product in e_products[:10]:
        dict_data = {}
         
        dict_data['product_link'] = e_product.find_element(By.XPATH, './div[contains(@class,"Showcase__content")]/div/a').get_attribute('href')
        dict_data['descripcion'] = e_product.find_element(By.XPATH, './div[contains(@class,"Showcase__content")]/div[2]/descendant::button').text
        dict_data['marca'] = e_product.find_element(By.XPATH, './div[contains(@class,"Showcase__content")]/div[2]/div[1]/descendant::a').text
        dict_data['formato'] = e_product.find_element(By.XPATH, './div[contains(@class,"Showcase__content")]/div[2]/descendant::div[contains(@class,"Showcase__units-reference")]').text
        xpath_precio_actual = './/div[contains(@class,"Showcase__salePrice")]//span[contains(@class,"price")]'
        xpath_precio_anterior = './/div[contains(@class,"Showcase__oldPrice")]//span[contains(@class,"price")]'
        xpath_precio_oh = './/div[contains(@class,"Showcase__ohPrice")]//span[contains(@class,"price")]'
        #dict_data['imagen'] = e_product.find_element(By.XPATH,'.//a[contains(@class,"Showcase__link")]//img').get_attribute('data-src')
        
        try:
            dict_data['precio'] = e_product.find_element(By.XPATH, xpath_precio_actual).text
        except:
            dict_data['precio'] = None
        try:
            dict_data['precio_anterior'] = e_product.find_element(By.XPATH, xpath_precio_anterior).text

        except:
            dict_data['precio_anterior'] = None
        try:
            dict_data['precio_oh'] = e_product.find_element(By.XPATH, xpath_precio_oh).text

        except:
            dict_data['precio_oh'] = None


       

        list_dict.append(dict_data)

    return list_dict
           
data = collect_products_from_page(browser)


#data = collect_all_products(browser)
#print(data)

for idx, item in enumerate(data, start=1):
    print(f"{idx}. {item['product_link']}\n"
            
            f"   descripcion: {item['descripcion']}\n"
            f"   marca: {item['marca']}\n"
            
            f"   formato: {item['formato']}\n"
            f"   precio_anterior: {item['precio_anterior']}\n"
            f"   precio: {item['precio']}\n"            
            f"   precio_oh: {item['precio_oh']}\n"
            
           
            
          
          )