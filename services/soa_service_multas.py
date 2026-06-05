import sys
sys.path.append('..')
from soa_lib import connect_to_bus, send_message, receive_message
import json
import os
sock = connect_to_bus()

def guardar_multa(id_prestamo, monto):
    MULTAS_FILE = 'multas.json'
    multa = {"id_prestamo": id_prestamo, "monto": monto, "estado": "pendiente"}
    #if not os.path.exists(MULTAS_FILE):
    multas = cargar_multas()
    multas.append(multa)
    with open(MULTAS_FILE, 'w') as f:
        json.dump(multas, f, indent=2)

def cargar_multas():
    MULTAS_FILE = 'multas.json'
    if not os.path.exists(MULTAS_FILE):
        return []
    with open(MULTAS_FILE, 'r') as f:
        return json.load(f)

def actualizar_multa(id_prestamo, monto):
    MULTAS_FILE = 'multas.json'
    if not os.path.exists(MULTAS_FILE):
        return [] #puede enviarse un error aqui
    with open(MULTAS_FILE, 'r') as f:
        multas = json.load(f)
    for multa in multas:
        if multa["id_prestamo"] == id_prestamo:
            multa["estado"] = "pagada"
            break
    with open(MULTAS_FILE, 'w') as f:                
        json.dump(multas, f, indent=2)
try:
    # 1. Registro inicial (sinit)
    print("Registrando servicio 'Multas'...")
    send_message(sock, "sinit", "multa")
    
    # 2. Procesar respuesta del sinit
    init_data = receive_message(sock)
    print(f"Confirmación de bus recibida: {init_data!r}")
    print("Servicio listo para recibir transacciones.\n")
    # 3. Bucle principal de trabajo
    while True:
        data = receive_message(sock)
        if not data:
            print("Conexión cerrada por el bus.")
            break
        # Extraer el payload (salta los 5 caracteres del nombre del servicio)
        mensaje = data[5:].decode()
        print(f"Mensaje recibido del cliente: '{mensaje}'")
        try:
            send_message(sock, "multa", "OK")
            print("Respuesta 'OK' enviada.")     
            payload = mensaje.split("|")
            print(f"Payload dividido: {payload}")
            accion = payload[0]
            datos = json.loads(payload[1])
            id_prestamo = datos.get("id_prestamo")
            monto = datos.get("monto")
            if accion == "generar":
                #generar multa
                guardar_multa(id_prestamo, monto)
                print(f"Multa generada")
            elif accion == "actualizar":
                #actualizar estado de multa
                actualizar_multa(id_prestamo, monto)
                print(f"Multa actualizada")


        except ValueError:
            send_message(sock, "multa", "Error: Formato incorrecto")

except Exception as e:
    print(f"Error en el servicio: {e}")
finally:
    print('Cerrando socket del servicio')
    sock.close()
