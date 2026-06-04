from soa_lib import connect_to_bus, send_message, receive_message
import json

try:
    sock = connect_to_bus()

    while True:
        rut = input("Ingrese el RUT del usuario ('q' para salir): ")
        if rut == 'q':
            break
        if not rut:
            print("¡Error! El RUT no puede estar vacío.")
            continue
        if len(rut) < 7 or len(rut) > 9:
            print("¡Error! El RUT debe tener entre 7 y 9 caracteres.")
            continue
        nombre = input("Ingrese el nombre del usuario: ")
        if not nombre:
            print("¡Error! El nombre no puede estar vacío.")
            continue
        datos = {"rut": rut, "nombre": nombre}
        payload = f"login|{json.dumps(datos)}"
        send_message(sock, "users", payload)
        data = receive_message(sock)
        respuesta = data[5:].decode()
        if respuesta.startswith("OK|"):
            rol = respuesta.split("|")[1]
            break
        else:
            print("Usuario no encontrado, debe registrarse.")
    while True:
        if rol == "admin":
            print("\n1. agregar usuario")
            print("2. listar usuarios")
            print("4. Salir")
        else:
            print("\n1. Ver inventario")
            print("2. Salir")
finally:
    print("Cerrando conexión con el bus...")
    sock.close()