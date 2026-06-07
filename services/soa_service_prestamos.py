import sys
sys.path.append('..')
from soa_lib import connect_to_bus, send_message, receive_message
import json
import os
import datetime

def cargar_prestamos():
    prestamos_file = 'prestamos.json'
    if not os.path.exists(prestamos_file):
        return []
    with open(prestamos_file, 'r') as f:
        return json.load(f)
def guardar_prestamos(prestamos):
    prestamos_file = 'prestamos.json'
    with open(prestamos_file, 'w') as f:
        json.dump(prestamos, f, indent=2)

try:
    sock = connect_to_bus()
    send_message(sock, "sinit", "loans")
    init_data = receive_message(sock)
    print(f"Confirmación: {init_data!r}")
    
    while True:
        data = receive_message(sock)
        if not data:
            print("Conexión cerrada por el bus.")
            break
        mensaje = data[5:].decode()
        print(f"Mensaje recibido del cliente: '{mensaje}'")
        try:
            mensaje = mensaje.split("|", 1)
            accion = mensaje[0]
            datos = json.loads(mensaje[1])
            print(f"Acción recibida: '{accion}' longitud: {len(accion)}")

            if accion == "solicitar":
                prestamos = cargar_prestamos()
                nuevo_id = 1 if not prestamos else max(p["id"] for p in prestamos) + 1
                datos["id"] = nuevo_id
                datos["fecha_solicitud"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                datos["fecha_devolucion"] = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
                datos["estado"] = "activo"
                datos["multa"] = False
                prestamos.append(datos)
                guardar_prestamos(prestamos)
                send_message(sock, "loans", "Préstamo solicitado")
                print("Préstamo solicitado.")
            elif accion == "devolver":
                prestamos = cargar_prestamos()
                id_prestamos = datos["id"]
                prestamo = next((p for p in prestamos if p["id"] == id_prestamos), None)
                if not prestamo:
                    send_message(sock, "loans", "ERROR: préstamo no encontrado")
                else:
                    prestamo["estado"] = "devuelto"
                    guardar_prestamos(prestamos)
                    send_message(sock, "loans", "Préstamo devuelto")
                    print("Préstamo devuelto.")
            elif accion == "listar":
                prestamos = cargar_prestamos()
                if not prestamos:
                    send_message(sock, "loans", "No hay préstamos registrados")
                else:
                    resultado = ""
                    for p in prestamos:
                        if p["estado"] == "activo" and datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") > p["fecha_devolucion"]:
                            p["multa"] = True
                        resultado += f"ID: {p['id']} | Rut usuario: {p['rut_usuario']} | id producto: {p['id_producto']} | Fecha Solicitud: {p['fecha_solicitud']} | Fecha Devolución: {p['fecha_devolucion']} | Estado: {p['estado']} | Multa: {'Sí' if p['multa'] else 'No'}\n"
                    
                    guardar_prestamos(prestamos)
                    send_message(sock, "loans", resultado)
                    print("Préstamos listados.")
        except Exception as e:
            print(f"Error al procesar el mensaje: {e}")
            send_message(sock, "loans", f"ERROR: {str(e)}")

finally:
    sock.close()
    print("Conexión cerrada.")