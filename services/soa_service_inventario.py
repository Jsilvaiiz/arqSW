import sys
sys.path.append('..')
from soa_lib import connect_to_bus, send_message, receive_message
import json
import os

def cargar_inventario():
    INVENTARIO_FILE = 'inventario.json'
    if not os.path.exists(INVENTARIO_FILE):
        return []
    with open(INVENTARIO_FILE, 'r') as f:
        return json.load(f)
def guardar_inventario(inventario):
    INVENTARIO_FILE = 'inventario.json'
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump(inventario, f, indent=2)
try:
    sock = connect_to_bus()

    send_message(sock, "sinit", "inven")
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
            mensaje = mensaje.split("|")
            accion = mensaje[0] 
            datos = json.loads(mensaje[1])
            print(f"Acción recibida: '{accion}' longitud: {len(accion)}")
            print(f"Acción: {accion}, Datos: {datos}")
            
            if accion == "agregar":
                inventario = cargar_inventario()
               
                if any(p["nombre"] == datos["nombre"] for p in inventario):
                    send_message(sock, "inven", "ERROR: ya existe un producto con ese nombre")
                else:
                    nuevo_id = 1 if not inventario else max(item["id"] for item in inventario) + 1
                    datos["id"] = nuevo_id
                    inventario.append(datos)
                    guardar_inventario(inventario)
                    send_message(sock, "inven", "Producto agregado")
                    print("Producto agregado al inventario.")
            elif accion == "listar":
                inventario = cargar_inventario()
                if not inventario:
                    send_message(sock, "inven", "Inventario vacío")
                else:    
                    print("Inventario listado.")
                    resultado = ""
                    for item in inventario:
                        resultado += f"ID: {item['id']} | {item['nombre']} | stock: {item['stock']} | {item['descripcion']} | {item['categoria']}\n"
                    send_message(sock, "inven", resultado)
                    print("Inventario listado.")
            elif accion == "eliminar":
                inventario = cargar_inventario()
                if not inventario:
                    send_message(sock, "inven", "Inventario vacío")
                else:
                    id_eliminar = datos["id"]
                    if not any(p["id"] == id_eliminar for p in inventario):
                        send_message(sock, "inven", "ERROR: ID no encontrado")
                    else:                        
                        nuevo_inventario = [item for item in inventario if item["id"] != id_eliminar]
                        guardar_inventario(nuevo_inventario)
                        send_message(sock, "inven", "Producto eliminado")
                        print("Producto eliminado del inventario.")
            elif accion == "listar_json":
                inventario = cargar_inventario()
                send_message(sock, "inven", json.dumps(inventario))
            elif accion == "actualizar_stock":
                inventario = cargar_inventario()
                producto = next((p for p in inventario if p["id"] == datos["id"]), None)
                if producto:
                    producto["stock"] = int(producto["stock"]) + datos["cantidad"]
                    guardar_inventario(inventario)
                    send_message(sock, "inven", "Stock actualizado")
            else:
                send_message(sock, "inven", "Acción no reconocida")
                print("Acción no reconocida.")
        except Exception as e:
            print(f"Error procesando mensaje: {e}")
            send_message(sock, "inven", f"Error: {e}")

finally:
    print('Cerrando conexión')
    sock.close()