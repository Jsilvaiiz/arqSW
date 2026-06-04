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
            print("\n0. Salir")
            print("1. Gestión de usuarios:")
            print("2. Gestión de inventario")
            print("3. Gestión de reportes")
            print("4. Gestión de multas")
            opcionAdmin = input("Seleccione una opción: ")
            if opcionAdmin == '1':
                print("1. agregar usuario")
                print("2. listar usuarios")        
                opcion = input("Seleccione una opción de gestión de usuario: ")
                
                if opcion == '1':
                    pass
                elif opcion == '2':
                    pass
                elif opcion == '0':
                    break
            elif opcionAdmin == '2':
                pass
            elif opcionAdmin == '3':
                pass
            elif opcionAdmin == '4':
                pass
        else:
            print("\n1. Ver inventario")
            print("2. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                pass
            elif opcion == '2':
                break
finally:
    print("Cerrando conexión con el bus...")
    sock.close()