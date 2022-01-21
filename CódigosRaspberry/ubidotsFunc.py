import requests
import time

def build_payload(variable_1, variable_2, acceso):
#Creación de payload vacío, si se ha permitido acceso se manda un 1 en la variable asociada 
#al acceso y un 0 a la de acceso denegado, si se ha denegado el acceso ocurre al contrario.
    payload = {}
    if (acceso):
      payload = {variable_1: 1}
    else:
      payload = {variable_2: 1}
    return payload

def post_request(payload,TOKEN,DEVICE_LABEL):
    # Creación de request HTTP
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    # Se realiza request HTTP
    status = 400
    attempts = 0
    #Se intenta envío de datos mientras se obtengan errores y con máximo 5 intentos.
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(0.1)
    #Mensaje según estado de envío.
    if status >= 400:
        print("[ERROR] Error en envio de datos.")
        return False
    print("[INFO] Envio exitoso.")
    return True
    
def send_Ubidots(TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1, VARIABLE_LABEL_2,acceso):
#Envío de datos hacia Ubidots.
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, acceso)
    print("[INFO] Intentando enviar datos.")
    post_request(payload,TOKEN,DEVICE_LABEL)
    print("[INFO] Envio finalizado.")
