from soa_lib import connect_to_bus, send_message, receive_message
import json
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Nueva función para pausar la pantalla
def pausar():
    input("\nPresiona ENTER para continuar...")

sock = None

try:
    sock = connect_to_bus()
    rol = None
    
    while not rol:
        limpiar_pantalla()
        opcion = input("¿Quiere iniciar sesión (1) o registrarse (2)? ('q' para salir): ")
        
        if opcion == 'q':
            print("Saliendo del programa.")
            break
            
        if opcion == "1":
            while True:
                limpiar_pantalla()
                rut = input("Ingrese el RUT del usuario ('q' para salir): ")
                if rut == 'q':
                    print("Saliendo del programa.")
                    break
                if not rut:
                    print("¡Error! El RUT no puede estar vacío.")
                    pausar()
                    continue
                if len(rut) < 7 or len(rut) > 9:
                    print("¡Error! El RUT debe tener entre 7 y 9 caracteres.")
                    pausar()
                    continue
                
                payload = f"consultar|{json.dumps({'rut': rut})}"
                send_message(sock, "users", payload)
                data = receive_message(sock)
                respuesta = data[5:].decode()
                
                if respuesta.startswith("OK"):
                    respuesta = respuesta[2:]
                
                print(f"Respuesta raw: {data}")
                print(f"Respuesta: {respuesta}")
                
                if "admin" in respuesta: # Ajustado para ignorar el OK|
                    contrasena = input("Ingrese la contraseña del usuario: ")
                    if not contrasena:
                        print("¡Error! La contraseña no puede estar vacía.")
                        pausar()
                        continue
                        
                    payload = f"login|{json.dumps({'rut': rut, 'contrasena': contrasena})}"
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
                            pausar()
                    else:  
                        print("Credenciales incorrectas.")
                        pausar()
                        
                elif "usuario" in respuesta:
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
                            pausar()
                    else:  
                        print("Credenciales incorrectas.")
                        pausar()
                else:
                    print("Usuario no encontrado, debe registrarse.")
                    pausar()
                    break # Rompe para volver al menu principal
                    
        elif opcion == "2":
            rut_nuevo = input("Ingrese el RUT del nuevo usuario: ")
            nombre_nuevo = input("Ingrese el nombre del nuevo usuario: ")
            email_nuevo = input("Ingrese el email del nuevo usuario: ")
            rol_nuevo = "usuario"
            contrasena_nuevo = ""
            datos_nuevo = {"rut": rut_nuevo, "nombre": nombre_nuevo, "email": email_nuevo, "rol": rol_nuevo, "contrasena": contrasena_nuevo}
            payload = f"registrar|{json.dumps(datos_nuevo)}"
            send_message(sock, "users", payload)
            data = receive_message(sock)
            respuesta = data[5:].decode()
            print(f"Respuesta: {respuesta}")
            if "agregado" in respuesta.lower():
                rut = rut_nuevo
                rol = "usuario"
                pausar()
            else:
                print(f"Error al registrarse: {respuesta}")
                pausar()
        else:
            print("Por favor seleccione una opción válida.")
            pausar()

    # --- MENÚ PRINCIPAL POST LOGIN ---
    if rol: 
        while True:
            limpiar_pantalla()
            if rol == "admin":
                print("\n=============================")
                print("       MENÚ ADMINISTRADOR    ")
                print("=============================")
                print("1. Gestión de usuarios")
                print("2. Gestión de inventario")
                print("3. Gestión de reportes")
                print("4. Gestión de multas")
                print("5. Gestión de préstamos")
                print("6. Búsqueda de inventario")
                print("0. Salir")
                print("=============================")
                opcionAdmin = input("Seleccione una opción: ")
                
                if opcionAdmin == '0':
                    break
                    
                elif opcionAdmin == '1':
                    print("\n1. Agregar usuario")
                    print("2. Listar usuarios")
                    print("3. Eliminar usuario")   
                    opcion = input("Seleccione una opción de gestión de usuario: ")   
                    
                    if opcion == '1':
                        rut_nuevo = input("Ingrese el RUT del nuevo usuario: ")
                        nombre_nuevo = input("Ingrese el nombre del nuevo usuario: ")
                        email_nuevo = input("Ingrese el email del nuevo usuario: ")
                        rol_nuevo = input("Ingrese el rol del nuevo usuario (admin/usuario): ")
                        if rol_nuevo not in ["admin", "usuario"]:
                            print("¡Error! El rol debe ser 'admin' o 'usuario'.")
                            pausar()
                            continue
                        if rol_nuevo == "admin" :
                            contrasena_nuevo = input("Ingrese la contraseña del nuevo usuario: ")
                        else:
                            contrasena_nuevo = ""
                        datos_nuevo = {"rut": rut_nuevo, "nombre": nombre_nuevo, "email": email_nuevo, "rol": rol_nuevo, "contrasena": contrasena_nuevo}
                        payload = f"registrar|{json.dumps(datos_nuevo)}"
                        send_message(sock, "users", payload)
                        data = receive_message(sock)
                        print(f"Respuesta: {data[5:].decode()}")
                        pausar()
                        
                    elif opcion == '2':
                        payload = f"listar|{json.dumps({})}"
                        send_message(sock, "users", payload)
                        data = receive_message(sock)
                        print(f"Respuesta: {data[5:].decode()}")
                        pausar()
                        
                    elif opcion == '3':
                        rut_eliminar = input("Ingrese el RUT del usuario a eliminar: ")
                        payload = f"eliminar|{json.dumps({'rut': rut_eliminar})}"
                        send_message(sock, "users", payload)
                        data = receive_message(sock)
                        print(f"Respuesta: {data[5:].decode()}")
                        pausar()

                elif opcionAdmin == '2':
                    while True:
                        limpiar_pantalla()
                        print("\n--- GESTIÓN DE INVENTARIO ---")
                        print("1. Agregar producto")
                        print("2. Quitar producto")
                        print("3. Listar Productos")
                        print("0. Volver")
                        opcion = input("Seleccione una opción: ")
                        if opcion == "0":
                            break
                        elif opcion == '1':
                            entrada = input('\nIngrese nombre del producto: ')
                            if not entrada:
                                print("¡Error! El nombre no puede estar vacío.")
                                pausar()
                                continue
                            stock = input('Ingrese stock: ')
                            if not stock.lstrip('-').isdigit():
                                print("¡Error! Por favor ingrese solo números.")
                                pausar()
                                continue
                            descripcion = input('Ingrese una descripción: ')
                            categoria = input('Ingrese la categoría del producto: ')
                            datos = {"nombre": entrada, "stock": stock, "descripcion": descripcion, "categoria": categoria}
                            payload = f"agregar|{json.dumps(datos)}"
                            send_message(sock, "inven", payload)
                            data = receive_message(sock)
                            print(f"Respuesta: {data[5:].decode()}")
                            pausar()

                        elif opcion == '2':
                            id_eliminar = input('Ingrese ID del producto a eliminar: ')
                            if not id_eliminar.isdigit():
                                print("¡Error! El ID debe ser un número.")
                                pausar()
                                continue
                            payload = f"eliminar|{json.dumps({'id': int(id_eliminar)})}"
                            send_message(sock, "inven", payload)
                            data = receive_message(sock)
                            print(f"Respuesta: {data[5:].decode()}")
                            pausar()

                        elif opcion == '3':
                            send_message(sock, "inven", "listar|{}")
                            data = receive_message(sock)
                            print(f"Respuesta:\n{data[5:].decode()}")
                            pausar()

                elif opcionAdmin == '3':
                    while True:
                        limpiar_pantalla()
                        print("\n--- GESTIÓN DE REPORTES ---")
                        print("1. Crear Reporte")
                        print("2. Listar reportes")
                        print("3. Modificar estados")
                        print("4. Eliminar reporte")
                        print("5. Volver")
                        opcion = input("Seleccione una opción: ")
                        if opcion == "1":
                            print("\n>>> PANTALLA: CREAR NUEVO REPORTE")
                            categoria = input("Categoría (pérdida / daño / mantenimiento): ").strip()
                            send_message(sock, "inven", "listar|{}")
                            data = receive_message(sock)
                            print(f"Inventario disponible:\n{data[5:].decode()}")
                            id_recurso = input("\nID del Recurso/Elemento: ").strip()
                            descripcion = input("Descripción del incidente: ").strip()
                            if not categoria or not id_recurso or not descripcion:
                                print("\n¡Error! Todos los campos son obligatorios.")
                                pausar()
                                continue
                            payload = f"CREAR;{categoria};{id_recurso};{descripcion}"
                            send_message(sock, "repor", payload)
                            data = receive_message(sock)
                            print(f"\nRespuesta del Bus: {data[5:].decode()}")
                            pausar()

                        elif opcion == "2":
                            print("\n>>> LISTADO DE REPORTES REGISTRADOS")
                            send_message(sock, "repor", "LISTAR")
                            data = receive_message(sock)
                            if data:
                                print(data[5:].decode())
                            pausar()

                        elif opcion == "3":
                            print("\n>>> MODIFICAR ESTADO DE REPORTE")
                            id_reporte = input("ID del reporte que desea cambiar: ").strip()
                            nuevo_estado = input("Nuevo estado (pendiente / en proceso / cerrado): ").strip()
                            if not id_reporte or not nuevo_estado:
                                print("\n¡Error! Faltan parámetros.")
                                pausar()
                                continue
                            payload = f"ESTADO;{id_reporte};{nuevo_estado}"
                            send_message(sock, "repor", payload)
                            data = receive_message(sock)
                            print(f"\nRespuesta del Bus: {data[5:].decode()}")
                            pausar()

                        elif opcion == "4":
                            print("\n>>> ELIMINAR REPORTE")
                            id_reporte = input("ID del reporte a eliminar: ").strip()
                            payload = f"ELIMINAR;{id_reporte};{rol}"
                            send_message(sock, "repor", payload)
                            data = receive_message(sock)
                            print(f"\nRespuesta del Bus: {data[5:].decode()}")
                            pausar()

                        elif opcion == "5":
                            break

                elif opcionAdmin == '4':
                    while True:
                        limpiar_pantalla()
                        print("\n--- GESTIÓN DE MULTAS ---")
                        print("1. Generar multa")
                        print("2. Actualizar estado de Multa")
                        print("3. Listado de multas")
                        print("4. Volver")
                        opcion = input("Seleccione una opción: ")
                    
                        if opcion == '1':
                            # 1. Mostramos la lista normal visualmente
                            send_message(sock, "loans", "listar|{}")
                            data_display = receive_message(sock)
                            print(f"Préstamos:\n{data_display[5:].decode()}")
                            
                            # 2. Pedimos el ID
                            entrada = input('Ingrese el ID del prestamo a multar: ') 
                            if not entrada.isdigit(): 
                                print("¡Error! ID inválido.")
                                pausar()
                                continue
                                
                            # 3. Buscamos el RUT silenciosamente usando JSON
                            send_message(sock, "loans", "listar_json|{}")
                            data_json = receive_message(sock)
                            respuesta_json = data_json[5:].decode()
                            
                            if respuesta_json.startswith("OK"):
                                respuesta_json = respuesta_json[2:]
                                
                            rut_multado = None
                            try:
                                prestamos = json.loads(respuesta_json)
                                for p in prestamos:
                                    if str(p['id']) == entrada: # Comparamos el ID
                                        rut_multado = p['rut_usuario']
                                        break
                            except json.JSONDecodeError:
                                pass # Si el JSON falla, rut_multado seguirá siendo None
                                
                            if not rut_multado:
                                print("¡Error! No se encontró un préstamo con ese ID o no se pudo extraer el RUT.")
                                pausar()
                                continue
                                
                            # 4. Pedimos el monto
                            monto = input('Ingrese el monto de la multa: ')
                            if not monto.replace('.', '', 1).isdigit():
                                print("Monto inválido, se asignará el monto por defecto de $500.")
                                monto = "500"
                                
                            # 5. Enviamos la solicitud con el RUT capturado automáticamente
                            print(f"\n=> Asignando multa automáticamente al RUT: {rut_multado} ...")
                            datos = {"id_prestamo": int(entrada), "monto": float(monto), "rut_usuario": rut_multado}
                            payload = f"generar|{json.dumps(datos)}"
                            send_message(sock, "multa", payload)   
                            data = receive_message(sock)        
                            
                            if data:
                                respuesta_multa = data[5:].decode()
                                print(f"Respuesta recibida: {data[5:].decode()}")

                                if "OK" in respuesta_multa or "generada" in respuesta_multa.lower():
                                    payload_prestamo = f"asignar_multa|{json.dumps({'id_prestamo': int(entrada)})}"
                                    send_message(sock, "loans", payload_prestamo)
                                    receive_message(sock) # Recibimos confirmación silenciosa
                                    print("=> Préstamo actualizado con estado de multa (true).")

                            pausar()
                            continue

                        elif opcion == '2':
                            send_message(sock, "multa", "listar|{}")
                            data = receive_message(sock)
                            print(f"Multas:\n{data[5:].decode()}")
                            id_multa = input('Ingrese el ID de la multa a actualizar a PAGADA: ')
                            if not id_multa.isdigit():
                                print("¡Error! El ID debe ser un número.")
                                pausar()
                                continue
                            payload = f"actualizar|{json.dumps({'id_prestamo': int(id_multa)})}"
                            send_message(sock, "multa", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            print(f"Respuesta: {respuesta}")
                            if "actualizada" in respuesta.lower():
                                payload = f"limpiar_multa|{json.dumps({'id_prestamo': int(id_multa)})}"
                                send_message(sock, "loans", payload)
                                print("La multa pasó de pendiente a pagada en préstamos.")
                            pausar()

                        elif opcion == "3":
                            send_message(sock, "multa", "listar|{}")
                            data = receive_message(sock)
                            print(f"Multas registradas:\n{data[5:].decode()}")
                            pausar()

                        elif opcion == '4':
                            break

                elif opcionAdmin == '5':
                    while True:
                        limpiar_pantalla()
                        print("\n--- GESTIÓN DE PRÉSTAMOS ---")
                        print("1. Ver todos los préstamos")
                        print("2. Registrar préstamo")
                        print("3. Registrar devolución")
                        print("0. Volver")
                        opcion = input("Seleccione una opción: ")
                        
                        if opcion == "0":
                            break
                        elif opcion == "1":
                            send_message(sock, "loans", "listar|{}") # Ajustado para listar normal si json daba problemas
                            data = receive_message(sock)
                            print(f"Préstamos:\n{data[5:].decode()}")
                            pausar()

                        elif opcion == "2":
                            rut_cliente = input("Ingrese el RUT del usuario: ")
                            payload = f"verificar|{json.dumps({'rut_usuario': rut_cliente})}"
                            send_message(sock, "multa", payload)
                            data = receive_message(sock)
                            respuesta = data[5:].decode()
                            if "ERROR" in respuesta:
                                print(f"No puedes solicitar un préstamo: {respuesta}")
                                pausar()
                            else:
                                send_message(sock, "inven", "listar|{}")
                                data = receive_message(sock)
                                print(f"Inventario disponible:\n{data[5:].decode()}")
                                producto_id = input("Ingrese el ID del producto que desea solicitar el usuario: ")
                                if not producto_id.isdigit():
                                    print("¡Error! El ID del producto debe ser un número.")
                                    pausar()
                                    continue
                                datos = {"rut_usuario": rut_cliente, "id_producto": int(producto_id)}
                                payload = f"solicitar|{json.dumps(datos)}"
                                send_message(sock, "loans", payload)
                                data = receive_message(sock)
                                respuesta = data[5:].decode()
                                print(f"Respuesta: {respuesta}")
                                if "solicitado" in respuesta.lower():
                                    payload = f"actualizar_stock|{json.dumps({ 'id': int(producto_id), 'cantidad': -1})}"
                                    send_message(sock, "inven", payload)
                                pausar()

                        elif opcion == "3":
                            send_message(sock,"loans", "listar|{}")
                            data = receive_message(sock)
                            print(f"Préstamos actuales:\n{data[5:].decode()}")
                            id_prestamo = input("Seleccione ID del préstamo que se devolvió: ")
                            if not id_prestamo.isdigit():
                                print("¡Error! El ID del préstamo debe ser un número.")
                                pausar()
                                continue
                            payload = f"devolver|{json.dumps({'id': int(id_prestamo)})}"
                            send_message(sock, "loans", payload)
                            data = receive_message(sock)
                            print(f"Respuesta: {data[5:].decode()}")
                            pausar()

                elif opcionAdmin == "6":
                    while True:
                        limpiar_pantalla()
                        print("\n=========================================")
                        print("    SODB - BÚSQUEDA DE INVENTARIO (SOA) ")
                        print("=========================================")
                        print("  [1] Buscar por Nombre")
                        print("  [2] Buscar por Descripción")
                        print("  [3] Buscar por Categoría")
                        print("  [4] Ver todo el Inventario (Listar)")
                        print("  [5] Volver")
                        print("=========================================")
                        opcion = input("Seleccione una acción (1-5): ").strip()
                        
                        if opcion in ["1", "2", "3"]:
                            tipo = "nombre" if opcion == "1" else ("descripcion" if opcion == "2" else "categoria")
                            valor = input(f"Ingrese {tipo} a buscar: ").strip()
                            if not valor:
                                print("\n¡Error! El campo no puede estar vacío.")
                                pausar()
                                continue
                            payload = f"BUSCAR;{tipo};{valor}"
                            send_message(sock, "binve", payload)
                            data = receive_message(sock)
                            print(f"\nResultados del Bus:\n{data[5:].decode()}")
                            pausar()

                        elif opcion == "4":
                            send_message(sock, "inven", "listar|{}")
                            data = receive_message(sock)
                            print(f"\nInventario completo:\n{data[5:].decode()}")
                            pausar()

                        elif opcion == "5":
                            break
                else:
                    print("Opción no válida. Por favor seleccione una opción del 1 al 6.")
                    pausar()

            elif rol == "usuario":   
                print("\n=============================")
                print("         MENÚ USUARIO        ")
                print("=============================")
                print("1. Ver inventario")
                print("2. Solicitar préstamo")
                print("3. Ver mis préstamos")
                print("0. Salir")
                print("=============================")
                opcion = input("Seleccione una opción: ")
                
                if opcion == '1':
                    send_message(sock, "inven", "listar_json|{}")
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if respuesta.startswith("OK"):
                        respuesta = respuesta[2:]
                    try:
                        inventario = json.loads(respuesta)
                        print("\n--- CATÁLOGO DISPONIBLE ---")
                        for p in inventario:
                            print(f"ID: {p['id']} | {p['nombre']} | Stock: {p['stock']} | {p['categoria']}")
                    except json.JSONDecodeError:
                        print(f"Inventario raw:\n{respuesta}")
                    pausar()

                elif opcion == '2':
                    payload = f"verificar|{json.dumps({'rut_usuario': rut})}"
                    send_message(sock, "multa", payload)
                    data = receive_message(sock)
                    respuesta = data[5:].decode()
                    if "ERROR" in respuesta:
                        print(f"No puedes solicitar un préstamo: {respuesta}")
                        pausar()
                    else:
                        send_message(sock, "inven", "listar|{}")
                        data = receive_message(sock)
                        print(f"\nCatálogo actual:\n{data[5:].decode()}")
                        producto_id = input("Ingrese el ID del producto que desea solicitar: ")
                        if not producto_id.isdigit():
                            print("¡Error! El ID del producto debe ser un número.")
                            pausar()
                            continue
                        datos = {"rut_usuario": rut, "id_producto": int(producto_id)}
                        payload = f"solicitar|{json.dumps(datos)}"
                        send_message(sock, "loans", payload)
                        data = receive_message(sock)
                        respuesta = data[5:].decode()
                        print(f"Respuesta: {respuesta}")
                        if "solicitado" in respuesta.lower():
                            payload = f"actualizar_stock|{json.dumps({ 'id': int(producto_id), 'cantidad': -1})}"
                            send_message(sock, "inven", payload)
                            receive_message(sock) 
                        pausar()

                elif opcion == '3':
                    datos = {"rut_usuario": rut}
                    payload = f"mis_prestamos|{json.dumps(datos)}"
                    send_message(sock, "loans", payload)
                    data = receive_message(sock)
                    print(f"\nTus préstamos:\n{data[5:].decode()}")
                    pausar()

                elif opcion == '0':
                    print("Cerrando sesión...")
                    break
                    
                else:
                    print("Opción inválida.")
                    pausar()

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando conexión con el bus...")
    if sock is not None:
        sock.close()