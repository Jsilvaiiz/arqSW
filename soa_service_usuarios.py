from soa_lib import connect_to_bus, send_message, receive_message
import json
import os

def cargar_usuarios():
    usuarios_file = 'usuarios.json'
    if not os.path.exists(usuarios_file):
        return []
    with open(usuarios_file, 'r') as f:
        return json.load(f)
def guardar_usuarios(usuarios):
    usuarios_file = 'usuarios.json'
    with open(usuarios_file, 'w') as f:
        json.dump(usuarios, f, indent=2)
try:
    sock = connect_to_bus()
    send_message(sock, "sinit", "users")
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

            if accion == "registrar":
                usuarios = cargar_usuarios()
                if any(u["rut"] == datos["rut"] for u in usuarios):
                    send_message(sock, "users", "ERROR: ya existe un usuario con ese rut")
                else:
                    nuevo_id = 1 if not usuarios else max(u["id"] for u in usuarios) + 1
                    datos["id"] = nuevo_id
                    usuarios.append(datos)
                    guardar_usuarios(usuarios)
                    send_message(sock, "users", "Usuario agregado")
                    print("Usuario agregado.")
            elif accion == "listar":
                usuarios = cargar_usuarios()
                if not usuarios:
                    send_message(sock, "users", "No hay usuarios registrados")
                else:
                    resultado = ""
                    for u in usuarios:
                        resultado += f"ID: {u['id']} | {u['nombre']} | {u['email']} |  {u['rut']} | {u['rol']}\n"
                    send_message(sock, "users", resultado)
                    print("Usuarios listados.")
            elif accion == "login":
                usuarios = cargar_usuarios()
                usuario = next((u for u in usuarios if u["nombre"] == datos["nombre"] and u["rut"] == datos["rut"]), None)
                if usuario:
                    send_message(sock, "users", f"OK|{usuario['rol']}")
                    print("Usuario autenticado.")
                else:
                    send_message(sock, "users", "ERROR: credenciales inválidas")
                    print("Intento de login fallido.")
        except Exception as e:
            print(f"Error al procesar el mensaje: {e}")
            send_message(sock, "users", f"ERROR: {str(e)}")
        
finally:
    print("Cerrando conexión con el bus.")
    sock.close()