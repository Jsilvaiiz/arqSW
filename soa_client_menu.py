from soa_lib import connect_to_bus, send_message, receive_message
import json

try:
    sock = connect_to_bus()
    rol = None

    while True:
        rut = input("Ingrese el RUT del usuario ('q' para salir): ")
        if rut == 'q':
            print("Saliendo del programa.")
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
    if rol: 
        while True:
            if rol == "admin":
                print("\n0. Salir")
                print("1. Gestión de usuarios:")
                print("2. Gestión de inventario")
                print("3. Gestión de reportes")
                print("4. Gestión de multas")
                print("5. Gestión de préstamos")
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
                    while True:
                        print("0. Salir")
                        print("\n1. Agregar producto")
                        print("2. Quitar producto")
                        print("3. Listar Productos")
                        opcion = input("Seleccione una opción: ")
                        if opcion == "0":
                            break
                        if opcion == '1':
                            entrada = input('\nIngrese nombre del producto:')
                            if not entrada:
                                print("¡Error! El nombre del producto no puede estar vacío.")
                                continue
                            stock = input('Ingrese stock: ')
                            if not stock.lstrip('-').isdigit():
                                print("¡Error! Por favor ingrese solo números.")
                                continue
                            descripcion = input('Ingrese una descripción: ')
                            if not descripcion:
                                print("¡Error! La descripción no puede estar vacía.")
                                continue
                            categoria = input('Ingrese la categoría del producto: ')
                            if not categoria:
                                print("¡Error! La categoría no puede estar vacía.")
                                continue
                            datos = {"nombre": entrada, "stock": stock, "descripcion": descripcion, "categoria": categoria}
                            payload = f"agregar|{json.dumps(datos)}"
                            send_message(sock, "inven", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")

                        elif opcion == '2':
                            id_eliminar = input('Ingrese ID del producto a eliminar: ')
                            if not id_eliminar.isdigit():
                                print("¡Error! El ID debe ser un número.")
                                continue
                            payload = f"eliminar|{json.dumps({'id': int(id_eliminar)})}"
                            send_message(sock, "inven", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")

                        elif opcion == '3':
                            send_message(sock, "inven", "listar|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")
                elif opcionAdmin == '5':
                    while True:
                        print("\n1. Ver todos los préstamos")
                        print("2. Registra préstamo")
                        print("3. Registra devolución")
                        print("0. Volver")
                        opcion = input("Seleccione una opción: ")
                        if opcion == "0":
                            break
                        if opcion == "1":
                            send_message(sock, "inven", "listar_json|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            inventario = json.loads(respuesta)
                            productos = {p["id"]: p["nombre"] for p in inventario}

                            send_message(sock, "loans", "listar_json|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            prestamos = json.loads(respuesta)

                            for p in prestamos:
                                nombre = productos.get(p["id_producto"], "Desconocido")
                                print(f"ID: {p['id']} | Producto: {nombre} | RUT: {p['rut_usuario']} | Estado: {p['estado']} | Multa: {'Sí' if p['multa'] else 'No'}")
                        if opcion == "2":
                            send_message(sock, "inven", "listar|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")
                            producto_id = input("Ingrese el ID del producto que desea solicitar el usuario: ")
                            if not producto_id.isdigit():
                                print("¡Error! El ID del producto debe ser un número.")
                                continue
                            rut_cliente = input("Ingrese el rut del usuario que quiere registrar el préstamo: ")
                            datos = {"rut_usuario": rut_cliente, "id_producto": int(producto_id)}
                            payload = f"solicitar|{json.dumps(datos)}"
                            send_message(sock, "loans", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")
                            if "solicitado" in respuesta.lower():
                                payload = f"actualizar_stock|{json.dumps({ 'id': int(producto_id), 'cantidad': -1})}"
                                send_message(sock, "inven", payload)
                                data = receive_message(sock) 

                        if opcion == "3":
                            send_message(sock,"loans", "listar|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")
                            id_prestamo = input("Seleccione prestamo que se devolvió")
                            if not id_prestamo.isdigit():
                                print("¡Error! El ID del producto debe ser un número.")
                                continue
                            payload = f"devolver|{json.dumps({'id': int(id_prestamo)})}"
                            send_message(sock, "loans", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Respuesta: {respuesta}")

                elif opcionAdmin == '4':
                    pass
                else:
                    print("Opción no válida. Por favor seleccione una opción del 1 al 5.")
            else:   
                print("0. Salir")
                print("\n1. Ver inventario")
                print("2. Solicitar préstamo")
                print("3. Ver mis préstamos")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    send_message(sock, "inven", "listar_json|{}")
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    inventario = json.loads(respuesta)
                    for p in inventario:
                        print(f"ID: {p['id']} | {p['nombre']} | Stock: {p['stock']} | {p['categoria']}")

                    
                elif opcion == '2':
                    send_message(sock, "inven", "listar|{}")
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    print(f"Respuesta: {respuesta}")
                    producto_id = input("Ingrese el ID del producto que desea solicitar: ")
                    if not producto_id.isdigit():
                        print("¡Error! El ID del producto debe ser un número.")
                        continue
                    datos = {"rut_usuario": rut, "id_producto": int(producto_id)}
                    payload = f"solicitar|{json.dumps(datos)}"
                    send_message(sock, "loans", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    print(f"Respuesta: {respuesta}")
                    if "solicitado" in respuesta.lower():
                        payload = f"actualizar_stock|{json.dumps({ 'id': int(producto_id), 'cantidad': -1})}"
                        send_message(sock, "inven", payload)
                        data = receive_message(sock) 
                elif opcion == '3':
                    datos = {"rut_usuario": rut}
                    payload = f"mis_prestamos|{json.dumps(datos)}"
                    send_message(sock, "loans", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    print(f"respuesta: {respuesta}")
                elif opcion == '0':
                    break
            
finally:
    print("Cerrando conexión con el bus...")
    sock.close()