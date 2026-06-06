from soa_lib import connect_to_bus, send_message, receive_message

def mostrar_pantalla_inicial():
    print("\n=========================================")
    print("     SODB - BÚSQUEDA DE INVENTARIO (SOA) ")
    print("=========================================")
    print("  [1] Buscar por Nombre")
    print("  [2] Buscar por Descripción")
    print("  [3] Buscar por Categoría")
    print("  [4] Ver todo el Inventario (Listar)")
    print("  [5] Salir del sistema")
    print("=========================================")

# Conexión inicial al BUS
sock = connect_to_bus()
nombre_servicio = "binve"

try:
    while True:
        mostrar_pantalla_inicial()
        opcion = input("Seleccione una acción (1-5): ").strip()

        # --- OPCIÓN 1: BUSCAR POR NOMBRE ---
        if opcion == "1":
            print("\n>>> PANTALLA: BUSCAR POR NOMBRE")
            valor = input("Ingrese el nombre a buscar: ").strip()
            if not valor:
                print("\n¡Error! El campo no puede estar vacío.")
                continue
            
            payload = f"BUSCAR;nombre;{valor}"
            send_message(sock, nombre_servicio, payload)
            
            print("Enviando al BUS, esperando resultados...")
            data = receive_message(sock)
            if data:
                print(f"\nResultados del Bus: {data[5:].decode()}")

        # --- OPCIÓN 2: BUSCAR POR DESCRIPCIÓN ---
        elif opcion == "2":
            print("\n>>> PANTALLA: BUSCAR POR DESCRIPCIÓN")
            valor = input("Ingrese texto de la descripción a buscar: ").strip()
            if not valor:
                print("\n¡Error! El campo no puede estar vacío.")
                continue
                
            payload = f"BUSCAR;descripcion;{valor}"
            send_message(sock, nombre_servicio, payload)
            
            data = receive_message(sock)
            if data:
                print(f"\nResultados del Bus: {data[5:].decode()}")

        # --- OPCIÓN 3: BUSCAR POR CATEGORÍA ---
        elif opcion == "3":
            print("\n>>> PANTALLA: BUSCAR POR CATEGORÍA")
            valor = input("Ingrese la categoría a buscar: ").strip()
            if not valor:
                print("\n¡Error! El campo no puede estar vacío.")
                continue
                
            payload = f"BUSCAR;categoria;{valor}"
            send_message(sock, nombre_servicio, payload)
            
            data = receive_message(sock)
            if data:
                print(f"\nResultados del Bus: {data[5:].decode()}")

        # --- OPCIÓN 4: LISTAR TODO ---
        elif opcion == "4":
            print("\n>>> PANTALLA: LISTADO COMPLETO DEL INVENTARIO")
            send_message(sock, nombre_servicio, "LISTAR")
            
            data = receive_message(sock)
            if data:
                print(data[5:].decode())

        # --- OPCIÓN 5: SALIR ---
        elif opcion == "5":
            print("\nSaliendo de la aplicación de búsqueda. ¡Hasta luego!")
            break
            
        else:
            print("\n¡Opción no válida! Por favor seleccione un número del 1 al 5.")

finally:
    print('Cerrando socket de conexión de forma segura...')
    sock.close()