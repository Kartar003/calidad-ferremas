import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# --- Configuración ---
RUTA_DRIVER = "chromedriver.exe" 
URL_LOGIN = "http://127.0.0.1:8000/" 

# --- Inicializar el Driver ---
service = Service(executable_path=RUTA_DRIVER)
driver = webdriver.Chrome(service=service)

print("Iniciando prueba de LOGIN...")

try:
    # 1. Abrir la página de INICIO
    driver.get(URL_LOGIN)
    print(f"Página abierta: {driver.title}")
    time.sleep(2) 

    boton_ir_a_login = driver.find_element(By.LINK_TEXT, "Iniciar Sesión")
    boton_ir_a_login.click()
    print("Botón 'Iniciar Sesión' presionado. Navegando a la página de login...")
    
    time.sleep(2) 
    
    # Encontramos 'name="email"'
    campo_usuario = driver.find_element(By.NAME, "email") 
    
    # Encontramos 'name="password"'
    campo_password = driver.find_element(By.NAME, "password") 

    campo_usuario.send_keys("an.salcedo@duocuc.cl") 
    campo_password.send_keys("Admin.123456789")    
    print("Texto escrito en los campos.")
    time.sleep(2)

    #Encontrar y hacer clic en el botón "Login"
    
    # Encontramos el texto "Login"
    boton_login = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]") 
    boton_login.click()
    print("Botón de 'Login' presionado.")

    # 6. Comprobar el resultado
    time.sleep(3) # Esperar a que la página cargue
    
    print(f"URL actual: {driver.current_url}")
    
    if "login" in driver.current_url:
        print("PRUEBA FALLIDA: Seguimos en la página de login (probablemente la contraseña es incorrecta).")
    else:
        print(f"PRUEBA EXITOSA: Redirigidos a {driver.current_url}")

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    print("Prueba finalizada. Cerrando navegador en 5 segundos...")
    time.sleep(5) 
    driver.quit()