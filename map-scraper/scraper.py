from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import time
import json

# Configuración
URL = "https://www.waze.com/es-419/live-map/"
CHROMEDRIVER_PATH = "C:/SeleniumDrivers/chromedriver.exe"
BODY_CHAR_LIMIT = 100000
GRID_HORIZONTAL_STEPS = 3
GRID_VERTICAL_STEPS = 3
PIXELS_PER_MOVE = 200

def main():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    time.sleep(5)

    try:
        acknowledge_button = driver.find_element(By.CLASS_NAME, "waze-tour-tooltip__acknowledge")
        acknowledge_button.click()
        print("✅ Se hizo clic en el botón correctamente.")
    except Exception as e:
        print(f"⚠️ No se pudo hacer clic en el botón: {e}")

    # Esperamos que todo se cargue bien
    time.sleep(2)

    screenWidth, screenHeight = pyautogui.size()
    center_x = screenWidth // 2
    center_y = screenHeight // 2
    print(f"🖱️ Click en el centro del mapa realizado en ({center_x}, {center_y})")
    pyautogui.click(center_x, center_y)
    time.sleep(1)

    print(f"🗺️ Moviendo el mapa arrastrando con el mouse real (grid {GRID_HORIZONTAL_STEPS}x{GRID_VERTICAL_STEPS})...")

    for y in range(GRID_VERTICAL_STEPS):
        for x in range(GRID_HORIZONTAL_STEPS):
            try:
                dx = PIXELS_PER_MOVE if y % 2 == 0 else -PIXELS_PER_MOVE
                dy = -PIXELS_PER_MOVE

                # Arrastrar el mouse desde el centro hacia una nueva posición
                pyautogui.moveTo(center_x, center_y)
                pyautogui.mouseDown()
                pyautogui.moveRel(dx, dy, duration=0.5)
                pyautogui.mouseUp()
                print(f"➡️ Mapa arrastrado con mouse real a ({x}, {y})")
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Error al mover el mapa: {e}")

    print("\n📡 Analizando solicitudes de red...")
    alertas = []

    for request in driver.requests:
        if request.response and request.url.split('?')[0].endswith("georss"):
            print("=" * 60)
            print(f"🔗 URL: {request.url}")
            print(f"🔁 Status: {request.response.status_code}")
            try:
                body = request.response.body.decode('utf-8')
                print("📦 Body (primeros caracteres):")
                print(body[:BODY_CHAR_LIMIT])

                data = json.loads(body)
                if 'alerts' in data:
                    for alerta in data['alerts']:
                        alerta.pop('comments', None)
                        alertas.append(alerta)
            except Exception as e:
                print(f"⚠️ No se pudo decodificar el cuerpo de la respuesta: {e}")

    driver.quit()

    if alertas:
        with open("alertas.json", "w", encoding="utf-8") as f:
            json.dump(alertas, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Se guardaron {len(alertas)} alertas en 'alertas.json'")
    else:
        print("⚠️ No se encontraron alertas para guardar.")

    print("✅ Navegación finalizada.")

if __name__ == "__main__":
    main()
