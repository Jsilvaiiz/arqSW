from soa_lib import connect_to_bus, send_message, receive_message

sock = connect_to_bus()

try:
    while True:
        entrada = input('\nIngrese ID_Reporte y mensaje: ')
        
        if entrada.lower() == 'q': #q para salir
            break
            
        if not entrada.isdigit():
            print("¡Error! Por favor ingrese solo números.")
            continue
        
        # Enviar el número como string al servicio "Alertas"
        send_message(sock, "alert", entrada)
        
        print(f"Esperando respuesta del servicio ({entrada}s)...")
        data = receive_message(sock)
        
        if data:
            # Mostrar el mensaje (quitando los 5 caracteres del nombre del servicio)
            print(f"Respuesta recibida: {data[5:].decode()}")
finally:
    print('Cerrando conexión')
    sock.close()

