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
                print("6. Búsqueda de inventario")
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
                        print("2. Registrar préstamo")
                        print("3. Registrar devolución")
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
                            try:
                                inventario = json.loads(respuesta)
                                productos = {p["id"]: p["nombre"] for p in inventario}
                            except json.JSONDecodeError:
                                productos = {}
                                print("No se pudo encontrar inventario")

                            send_message(sock, "loans", "listar_json|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            try:
                                prestamos = json.loads(respuesta)
                                if not prestamos:
                                    print("No hay préstamos registrados")
                                else:
                                    for p in prestamos:
                                        nombre = productos.get(p["id_producto"], "Desconocido")
                                        print(f"ID: {p['id']} | Producto: {nombre} | RUT: {p['rut_usuario']} | Estado: {p['estado']} | Multa: {'Sí' if p['multa'] else 'No'}")
                            except json.JSONDecodeError:
                                print("No hay préstamos registrados")                 

                        if opcion == "2":
                            rut_cliente = input("Ingrese el RUT del usuario: ")
                            payload = f"verificar|{json.dumps({'rut_usuario': rut_cliente})}"
                            send_message(sock, "multa", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            if "ERROR" in respuesta:
                                print(f"No puedes solicitar un préstamo: {respuesta}")
                            else:
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
                    while True:
                        print("\n1. Generar multa")
                        print("2. Actualizar estado de Multa")
                        print("3. Listado de multas")
                        print("4. Volver")
                        opcion = input("Seleccione una opción: ")
                    
                        if not opcion.isdigit():
                            print("¡Error! Por favor ingrese solo números.")
                            continue
                        #cuando se crea una multa empieza con estado pendiente, luego se puede actualizar a pagada o cancelada, pero no se puede volver a pendiente
                        if opcion == '1':
                            entrada = input('Ingrese el Id del prestamo: ') # es suficiente para reconocer el caso ?
                            if not entrada.isdigit(): #nose si hace falta el id del user
                                print("¡Error!")
                                continue
                            monto = input('Ingrese el monto de la multa: ')
                            if not monto.replace('.', '', 1).isdigit():
                                print("Monto inválido, se asignará el monto por defecto de $500.")
                                monto = "500"
                            #    print("¡Error! Por favor ingrese un monto válido.")
                            #    continue
                            rut_multado = input("Ingrese el RUT del usuario multado: ")
                            datos = {"id_prestamo": int(entrada), "monto": float(monto), "rut_usuario": rut_multado}
                            payload = f"generar|{json.dumps(datos)}"
                            send_message(sock, "multa", payload)   
                            print(f"Esperando respuesta del servicio ({entrada}s)...")
                            data = receive_message(sock)        
                            if data:
                            # Mostrar el mensaje (quitando los 5 caracteres del nombre del servicio)
                                print(f"Respuesta recibida: {data[5:].decode()}")

                        if opcion == '2':
                            send_message(sock, "multa", "listar|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Multas:\n{respuesta}")
                            id_multa = input('Ingrese el ID de la multa a actualizar: ')
                            if not id_multa.isdigit():
                                print("¡Error! El ID debe ser un número.")
                                continue
                            payload = f"actualizar|{json.dumps({'id_prestamo': int(id_multa)})}"
                            send_message(sock, "multa", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            if "actualizada" in respuesta.lower():
                                id_prestamo = id_multa
                                payload = f"limpiar_multa|{json.dumps({'id_prestamo': int(id_prestamo)})}"
                                send_message(sock, "loans", payload)
                                data = receive_message(sock)
                                respuesta = data[5:].decode()
                                if respuesta.startswith("OK"):
                                    respuesta = respuesta[2:]
                                print(f"La multa pasó de pendiente a pagada.")
                        if opcion == "3":
                            send_message(sock, "multa", "listar|{}")
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if respuesta.startswith("OK"):
                                respuesta = respuesta[2:]
                            print(f"Multas:\n{respuesta}")
                        if opcion == '4':
                            break
                elif opcionAdmin == "3":
                    while True:
                        print("\n1. Crear Reporte")
                        print("2. Listar reportes")
                        print("3. Modificar estados")
                        print("4. Eliminar reporte")
                        print("5. Volver")
                        opcion = input("Seleccione una opción: ")
                        if opcion == "1":
                            print("\n>>> PANTALLA: CREAR NUEVO REPORTE")
                            categoria = input("Categoría (pérdida / daño / mantenimiento): ").strip()
                            id_recurso = input("ID del Recurso/Elemento: ").strip()
                            descripcion = input("Descripción del incidente: ").strip()
                            
                            if not categoria or not id_recurso or not descripcion:
                                print("\n¡Error! Todos los campos son obligatorios para crear un reporte.")
                                input("\nPresione Enter para volver a la pantalla inicial...")
                                continue
                            
                            payload = f"CREAR;{categoria};{id_recurso};{descripcion}"
                            send_message(sock, "repor", payload)
                            
                            print("Enviando datos al BUS, esperando confirmación...")
                            data = receive_message(sock)
                            if data:
                                print(f"\nRespuesta del Bus: {data[5:].decode()}")
                        if opcion == "2":
                            print("\n>>> PANTALLA: LISTADO DE REPORTES REGISTRADOS")
                            send_message(sock, "repor", "LISTAR")
                            data = receive_message(sock)
                            if data:
                                print(data[5:].decode())
                        if opcion == "3":
                            print("\n>>> PANTALLA: MODIFICAR ESTADO")
                            id_reporte = input("ID del reporte que desea cambiar: ").strip()
                            nuevo_estado = input("Nuevo estado (pendiente / en proceso / cerrado): ").strip()
                            
                            if not id_reporte or not nuevo_estado:
                                print("\n¡Error! Faltan parámetros.")
                                input("\nPresione Enter para volver a la pantalla inicial...")
                                continue
                                
                            payload = f"ESTADO;{id_reporte};{nuevo_estado}"
                            send_message(sock, "repor", payload)
                            
                            data = receive_message(sock)
                            if data:
                                print(f"\nRespuesta del Bus: {data[5:].decode()}")
                        if opcion == "4":
                            print("\n>>> PANTALLA: ELIMINAR REPORTE (Requiere privilegios)")
                            id_reporte = input("ID del reporte a eliminar: ").strip()
                            
                                
                            payload = f"ELIMINAR;{id_reporte};{rol}"
                            send_message(sock, "repor", payload)
                            
                            data = receive_message(sock)
                            if data:
                                print(f"\nRespuesta del Bus: {data[5:].decode()}")
                        if opcion == "5":
                            break
                elif opcionAdmin == 6:
                    opcion = input("Seleccione una acción (1-5): ").strip()
                    print("\n=========================================")
                    print("     SODB - BÚSQUEDA DE INVENTARIO (SOA) ")
                    print("=========================================")
                    print("  [1] Buscar por Nombre")
                    print("  [2] Buscar por Descripción")
                    print("  [3] Buscar por Categoría")
                    print("  [4] Ver todo el Inventario (Listar)")
                    print("  [5] Salir del sistema")
                    print("=========================================")
                    
                else:
                    print("Opción no válida. Por favor seleccione una opción del 1 al 6.")
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
                    payload = f"verificar|{json.dumps({'rut_usuario': rut})}"
                    send_message(sock, "multa", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    if "ERROR" in respuesta:
                        print(f"No puedes solicitar un préstamo: {respuesta}")
                    else:
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