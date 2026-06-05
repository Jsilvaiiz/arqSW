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
        datos = {"rut": rut}

        payload = f"consultar|{json.dumps({'rut': rut})}"
        send_message(sock, "users", payload)
        data = receive_message(sock)
        respuesta = data[5:].decode()
        if respuesta.startswith("OK"):
            respuesta = respuesta[2:]
        print(f"Respuesta raw: {data}")
        print(f"Respuesta: {respuesta}")
        if respuesta.startswith("OK|admin"):
            rol = respuesta.split("|")[1]
            contrasena = input("Ingrese la contraseña del usuario: ")
            payload = f"login|{json.dumps({'rut': rut, 'contrasena': contrasena})}"
            if not contrasena:
                print("¡Error! La contraseña no puede estar vacía.")
                continue
            send_message(sock, "users", payload)
            data = receive_message(sock)
            respuesta = data[5:].decode()
            if respuesta.startswith("OK"):
                respuesta = respuesta[2:]
                if "|" in respuesta:
                    rol = respuesta.split("|")[1]
                    break
                else:  
                    print("Credenciales incorrectas.")
            else:  
                print("Credenciales incorrectas.")
        elif respuesta.startswith("OK|usuario"):
            rol = respuesta.split("|")[1]
            nombre_usuario = input("Ingrese el nombre del usuario: ")
            payload = f"login|{json.dumps({'rut': rut, 'nombre': nombre_usuario})}"
            send_message(sock, "users", payload)
            data = receive_message(sock)
            respuesta = data[5:].decode()
            print(f"Respuesta: {respuesta}")
            if respuesta.startswith("OK"):
                respuesta = respuesta[2:]
                if "|" in respuesta:
                    rol = respuesta.split("|")[1]
                    break
                else:  
                    print("Credenciales incorrectas.")
            else:  
                print("Credenciales incorrectas.")
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
            if opcionAdmin == '0':
                break
            if opcionAdmin == '1':
                print("1. agregar usuario")
                print("2. listar usuarios")
                print("3. eliminar usuario")   
                opcion = input("Seleccione una opción de gestión de usuario: ")   
                if opcion == '1':
                    rut_nuevo = input("Ingrese el RUT del nuevo usuario: ")
                    nombre_nuevo = input("Ingrese el nombre del nuevo usuario: ")
                    email_nuevo = input("Ingrese el email del nuevo usuario: ")
                    rol_nuevo = input("Ingrese el rol del nuevo usuario (admin/usuario): ")
                    if rol_nuevo not in ["admin", "usuario"]:
                        print("¡Error! El rol debe ser 'admin' o 'usuario'.")
                        continue
                    if rol_nuevo == "admin" :
                        contrasena_nuevo = input("Ingrese la contraseña del nuevo usuario: ")
                    else:
                        contrasena_nuevo = ""
                    datos_nuevo = {"rut": rut_nuevo, "nombre": nombre_nuevo, "email": email_nuevo, "rol": rol_nuevo, "contrasena": contrasena_nuevo}
                    payload = f"registrar|{json.dumps(datos_nuevo)}"
                    send_message(sock, "users", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    print(f"Respuesta: {respuesta}")
                elif opcion == '2':
                    payload = f"listar|{json.dumps({})}"
                    send_message(sock, "users", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    print(f"Respuesta: {respuesta}")
                elif opcion == '3':
                    rut_eliminar = input("Ingrese el RUT del usuario a eliminar: ")
                    payload = f"eliminar|{json.dumps({'rut': rut_eliminar})}"
                    send_message(sock, "users", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    print(f"Respuesta: {respuesta}")
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