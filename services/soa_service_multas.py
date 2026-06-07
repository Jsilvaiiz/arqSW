import sys
sys.path.append('..')
from soa_lib import connect_to_bus, send_message, receive_message
import json
import os
sock = connect_to_bus()

def guardar_multa(id_prestamo, monto, rut_usuario):
    MULTAS_FILE = 'multas.json'
    multa = {"rut_usuario":rut_usuario, "id_prestamo": id_prestamo, "monto": monto, "estado": "pendiente"}
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
            payload = mensaje.split("|")
            print(f"Payload dividido: {payload}")
            accion = payload[0]
            datos = json.loads(payload[1])
            id_prestamo = datos.get("id_prestamo")
            monto = datos.get("monto")
            if accion == "generar":
                #generar multa
                guardar_multa(id_prestamo, monto, datos.get("rut_usuario"))
                print(f"Multa generada")
                send_message(sock, "multa", "Multa generada")
            elif accion == "actualizar":
                #actualizar estado de multa
                actualizar_multa(id_prestamo, monto)
                print(f"Multa actualizada")
                send_message(sock, "multa", "Multa Actualizada")
            elif accion == "verificar":
                multas = cargar_multas()
                rut_usuario = datos["rut_usuario"]
                tiene_multa = any(m for m in multas if m["rut_usuario"] == rut_usuario and m["estado"] == "pendiente")
                if tiene_multa:
                    send_message(sock, "multa", "ERROR: tiene una multa pendiente")
                else:
                    send_message(sock, "multa", "OK")
            elif accion == "listar":
                listar = cargar_multas()
                if not listar:
                    send_message(sock, "multa", "No hay multas")
                else:
                    resultado = ""
                    for m in multas:
                        resultado += f"ID prestamo: {m['id_prestamo']} | RUT: {m['rut_usuario']} | Monto: {m['monto']} | Estado: {m['estado']}\n"
                    send_message(sock, "multa", resultado)
        except ValueError:
            send_message(sock, "multa", "Error: Formato incorrecto")

except Exception as e:
    print(f"Error en el servicio: {e}")
finally:
    print('Cerrando socket del servicio')
    sock.close()
