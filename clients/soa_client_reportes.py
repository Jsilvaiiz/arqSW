from soa_lib import connect_to_bus, send_message, receive_message

def mostrar_pantalla_inicial():
    print("\n=========================================")
    print("     SODB - SISTEMA DE REPORTES (SOA)    ")
    print("=========================================")
    print("  [1] Crear un nuevo reporte")
    print("  [2] Ver todos los reportes (Listar)")
    print("  [3] Modificar estado de un reporte")
    print("  [4] Eliminar un reporte")
    print("  [5] Salir del sistema")
    print("=========================================")

# Conexión inicial al BUS
sock = connect_to_bus()
nombre_servicio = "repor"

try:
    while True:
        mostrar_pantalla_inicial()
        opcion = input("Seleccione una acción (1-5): ").strip()

        # --- OPCIÓN 1: CREAR REPORTE ---
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
            send_message(sock, nombre_servicio, payload)
            
            print("Enviando datos al BUS, esperando confirmación...")
            data = receive_message(sock)
            if data:
                print(f"\nRespuesta del Bus: {data[5:].decode()}")
            

        # --- OPCIÓN 2: LISTAR REPORTES ---
        elif opcion == "2":
            print("\n>>> PANTALLA: LISTADO DE REPORTES REGISTRADOS")
            send_message(sock, nombre_servicio, "LISTAR")
            
            data = receive_message(sock)
            if data:
                print(data[5:].decode())
            

        # --- OPCIÓN 3: MODIFICAR ESTADO ---
        elif opcion == "3":
            print("\n>>> PANTALLA: MODIFICAR ESTADO")
            id_reporte = input("ID del reporte que desea cambiar: ").strip()
            nuevo_estado = input("Nuevo estado (pendiente / en proceso / cerrado): ").strip()
            
            if not id_reporte or not nuevo_estado:
                print("\n¡Error! Faltan parámetros.")
                input("\nPresione Enter para volver a la pantalla inicial...")
                continue
                
            payload = f"ESTADO;{id_reporte};{nuevo_estado}"
            send_message(sock, nombre_servicio, payload)
            
            data = receive_message(sock)
            if data:
                print(f"\nRespuesta del Bus: {data[5:].decode()}")
            

        # --- OPCIÓN 4: ELIMINAR REPORTE ---
        elif opcion == "4":
            print("\n>>> PANTALLA: ELIMINAR REPORTE (Requiere privilegios)")
            id_reporte = input("ID del reporte a eliminar: ").strip()
            rol = input("Ingrese su rol de usuario: ").strip()
            
            if not id_reporte or not rol:
                print("\n¡Error! Faltan parámetros.")
                input("\nPresione Enter para volver a la pantalla inicial...")
                continue
                
            payload = f"ELIMINAR;{id_reporte};{rol}"
            send_message(sock, nombre_servicio, payload)
            
            data = receive_message(sock)
            if data:
                print(f"\nRespuesta del Bus: {data[5:].decode()}")
            

        # --- OPCIÓN 5: SALIR ---
        elif opcion == "5":
            print("\nSaliendo de la aplicación de reportes. ¡Hasta luego!")
            break
            
        else:
            print("\n¡Opción no válida! Por favor seleccione un número del 1 al 5.")

finally:
    print('Cerrando socket de conexión de forma segura...')
    sock.close() #