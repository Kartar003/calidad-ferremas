import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# --- Configuración ---
RUTA_DRIVER = "chromedriver.exe" 
URL_LOGIN = "http://127.0.0.1:8000/" 

# --- Inicializar el Driver ---
service = Service(executable_path=RUTA_DRIVER)
driver = webdriver.Chrome(service=service)
# Definimos nuestra espera "inteligente" (máximo 15 segundos)
wait = WebDriverWait(driver, 15) 

print("Iniciando prueba de CARRITO (Casos 003 y 004)...")

try:
    # ==================================================================
    # PARTE 1: INICIAR SESIÓN (COMO CLIENTE) - MODO SEGURO
    # ==================================================================
    driver.get(URL_LOGIN)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar Sesión"))).click()
    
    # Usamos las credenciales del CLIENTE
    
    # ¡CORREGIDO! Esperamos por CADA elemento
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("cliente@ferremas.cl")
    
    # ¡CORREGIDO! Esperamos por CADA elemento
    wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("Admin.123456789")
    
    # ¡CORREGIDO! Esperamos por CADA elemento
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))).click()
    
    # Verificamos que el login fue exitoso esperando por el enlace "Cerrar sesión"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cerrar sesión")))
    print("Login de Cliente exitoso.")

    # ==================================================================
    # PARTE 2: CASO 003 - AÑADIR PRODUCTO AL CARRITO
    # ==================================================================
    
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Catálogo de Productos"))).click()
    wait.until(EC.url_contains("/productos")) 
    print("Navegando al catálogo de productos...")

    # Esperamos a que la lista de botones "Agregar" esté presente
    botones_anadir = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Agregar')]")))
    botones_anadir[0].click() # Clic en el primer producto
    
    # Esperamos a que aparezca el mensaje de éxito
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Producto agregado al pedido')]")))
    print("CASO 003 EXITOSO: Producto añadido al carrito.")
    
    # ==================================================================
    # PARTE 3: CASO 004 - EDITAR Y CREAR PEDIDO
    # ==================================================================
    
    # Esperamos a que el enlace "Mi Pedido (1)" esté listo
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Mi Pedido"))).click()
    
    wait.until(EC.url_contains("/pedidos/crear"))
    print("Navegando a la página de 'Crear Pedido' (Carrito)...")

    # 3. Rellenar el formulario de edición
    
    # a. Seleccionar Sucursal
    select_sucursal_element = wait.until(EC.element_to_be_clickable((By.NAME, "sucursal_id")))
    select_sucursal = Select(select_sucursal_element)
    select_sucursal.select_by_index(1) 
    
    # b. Seleccionar Método de Pago
    select_pago_element = wait.until(EC.element_to_be_clickable((By.NAME, "metodo_pago")))
    select_pago = Select(select_pago_element)
    select_pago.select_by_visible_text("Débito")
    
    # c. Editar Cantidad
    campo_cantidad = wait.until(EC.element_to_be_clickable((By.NAME, "productos")))
    campo_cantidad.clear()
    campo_cantidad.send_keys("3")
    
    print("Formulario de pedido (carrito) rellenado.")
    time.sleep(2)

    # 4. Hacer clic en "Crear Pedido"
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Crear Pedido')]"))).click()
    print("Botón 'Crear Pedido' presionado.")
    
    # 5. Comprobar el resultado (Resultado Esperado)
    wait.until(EC.url_contains("/pedidos/"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Pedido creado exitosamente')]")))
    
    print("CASO 004 EXITOSO: Pedido creado exitosamente.")

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    # 6. Cerrar el navegador
    print("Prueba finalizada. Cerrando navegador en 5 segundos...")
    time.sleep(5) 
    driver.quit()