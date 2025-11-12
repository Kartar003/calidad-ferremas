import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuración ---
RUTA_DRIVER = "chromedriver.exe" 
URL_LOGIN = "http://127.0.0.1:8000/" 

# --- Inicializar el Driver ---
service = Service(executable_path=RUTA_DRIVER)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15) # Espera máxima de 15 segundos

print("Iniciando prueba de REGISTRO DE USUARIO...")

try:
    # ==================================================================
    # PARTE 1: INICIAR SESIÓN
    # ==================================================================
    driver.get(URL_LOGIN)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar Sesión"))).click()
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("an.salcedo@duocuc.cl")
    driver.find_element(By.NAME, "password").send_keys("Admin.123456789")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    print("Login de Administrador exitoso. Navegando al dashboard...")

    # ==================================================================
    # PARTE 2: REGISTRAR EL NUEVO USUARIO
    # ==================================================================
    
    # 1. Esperar y hacer clic en "Registrar Usuario"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Registrar Usuario"))).click()
    print("Navegando a la página de registro...")
    
    # !! ---- LA CORRECCIÓN DEFINITIVA ---- !!
    # 1. Esperamos a que la URL del navegador cambie a la página de registro
    wait.until(EC.url_contains("/register/"))
    print("Página de registro cargada.")
    # 2. AHORA SÍ, esperamos a que el campo "name" esté listo
    # (Usamos element_to_be_clickable porque es la espera más segura)
    campo_nombre = wait.until(EC.element_to_be_clickable((By.NAME, "name")))
    # !! ---------------------------------- !!

    # 2. Rellenar el formulario (Usamos send_keys, es más fiable si funciona)
    campo_nombre.send_keys("Usuario Prueba Selenium")
    driver.find_element(By.NAME, "email").send_keys("selenium_user@correo.com")
    driver.find_element(By.NAME, "password").send_keys("Selenium123")
    driver.find_element(By.NAME, "rut").send_keys("1111111-1")
    
    # 3. Seleccionar el Rol del dropdown
    dropdown_rol = driver.find_element(By.NAME, "rol")
    select = Select(dropdown_rol)
    select.select_by_visible_text("Cliente") 
    
    print("Formulario rellenado.")
    time.sleep(2)

    # 4. Hacer clic en el botón "Registrarse"
    boton_registrar = driver.find_element(By.XPATH, "//button[contains(text(), 'Registrarse')]")
    boton_registrar.click()
    print("Botón 'Registrarse' presionado.")
    
    # 5. Comprobar el resultado
    time.sleep(3) 
    
    print(f"URL actual: {driver.current_url}")
    if "register" in driver.current_url:
        print("PRUEBA FALLIDA: Seguimos en la página de registro (quizás el RUT o email ya existen).")
    else:
        print(f"PRUEBA EXITOSA: Usuario registrado y redirigido a {driver.current_url}")

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    # 6. Cerrar el navegador
    print("Prueba finalizada. Cerrando navegador en 5 segundos...")
    time.sleep(5) 
    driver.quit()