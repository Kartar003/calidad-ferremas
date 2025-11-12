import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select # <--- ¡Nuevo! Para los menús dropdown

# --- Configuración ---
RUTA_DRIVER = "chromedriver.exe" 
URL_LOGIN = "http://127.0.0.1:8000/" 

# --- Inicializar el Driver ---
service = Service(executable_path=RUTA_DRIVER)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15) 

print("Iniciando prueba de CREAR PRODUCTO...")

# Generamos un nombre de producto único cada vez que corremos la prueba
# para que no falle por "producto ya existe".
nombre_producto_nuevo = f"Taladro Selenium {int(time.time())}" 

try:
    # ==================================================================
    # PARTE 1: INICIAR SESIÓN
    # ==================================================================
    driver.get(URL_LOGIN)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar Sesión"))).click()
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("an.salcedo@duocuc.cl")
    driver.find_element(By.NAME, "password").send_keys("Admin.123456789")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    print("Login de Administrador exitoso.")
    wait.until(EC.url_contains("/dashboard/"))

    # ==================================================================
    # PARTE 2: CREAR EL NUEVO PRODUCTO
    # ==================================================================
    
    # 1. Clic en el enlace "Productos"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Productos"))).click()
    print("Navegando a la página de productos...")

    # 2. Esperar a que la página de productos cargue
    wait.until(EC.url_contains("/productos"))
    
    # 3. Clic en el enlace "Crear Producto"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Crear Producto"))).click()
    print("Navegando al formulario de crear producto...")

    # 4. Esperar a que el formulario cargue
    wait.until(EC.url_contains("/productos/crear"))
    print("Formulario cargado. Rellenando campos...")

    # 5. Rellenar el formulario con los 'name' que encontraste
    
    # Rellenar Nombre (de image_e0cb31.png)
    wait.until(EC.element_to_be_clickable((By.NAME, "nombre"))).send_keys(nombre_producto_nuevo)
    
    # Rellenar Descripción
    driver.find_element(By.NAME, "descripcion").send_keys("Taladro de prueba creado con Selenium")
    
    # Rellenar Precio
    driver.find_element(By.NAME, "precio").send_keys("12345")
    
    # 6. Seleccionar de los dropdowns (Marca y Categoría)
    
    # Seleccionar Marca
    select_marca = Select(driver.find_element(By.NAME, "marca_id"))
    select_marca.select_by_index(1) # Selecciona la primera opción (ej. "Bosch")
    
    # Seleccionar Categoría
    select_categoria = Select(driver.find_element(By.NAME, "categoria_id"))
    select_categoria.select_by_index(1) # Selecciona la primera opción (ej. "Herramientas Eléctricas")
    
    print("Formulario rellenado.")
    time.sleep(2)

    # 7. Hacer clic en el botón "Crear"
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear')]").click()
    print("Botón 'Crear' presionado.")
    
    # 8. Comprobar el resultado
    # La prueba es exitosa si nos redirige de vuelta a la lista de productos
    wait.until(EC.url_contains("/productos")) # Espera a volver a la lista
    
    if "/productos/crear" in driver.current_url:
        print("PRUEBA FALLIDA: Seguimos en la página de creación.")
    else:
        print(f"PRUEBA EXITOSA: Producto creado y redirigido a {driver.current_url}")
        # (Verificación extra)
        print(f"Buscando el producto '{nombre_producto_nuevo}' en la página...")
        assert driver.page_source.find(nombre_producto_nuevo) != -1
        print("¡Producto encontrado en la tabla! Prueba verificada.")

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    # 9. Cerrar el navegador
    print("Prueba finalizada. Cerrando navegador en 5 segundos...")
    time.sleep(5) 
    driver.quit()