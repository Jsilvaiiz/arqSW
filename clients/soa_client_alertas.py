from soa_lib import connect_to_bus, send_message, receive_message

sock = connect_to_bus()

try:
    while True:
        print("\n1. Cambiar estado de alerta")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            id_reporte = input('\nIngrese el ID_Reporte: ')
            if not id_reporte.isdigit():
                print("¡Error! Por favor ingrese solo números.")
                continue
            estado = input('Ingrese el nuevo estado de la alerta: (entregada/leída/recibida)')
            if estado not in ['entregada', 'leída', 'recibida']:
                print("¡Error! El estado debe ser 'entregada', 'leída' o 'recibida'.")
                continue
            payload = f"cambiar_estado|{id_reporte}|{estado}"
            send_message(sock, "alert", payload)
            data = receive_message(sock)
            print(f"Respuesta: {data[5:].decode()}") 


        elif opcion == '2':
            break
        else:
            print("Opción no válida. Por favor seleccione una opción del 1 al 2.")
finally:
    print('Cerrando conexión')
    sock.close()