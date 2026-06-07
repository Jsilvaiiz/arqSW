from soa_lib import connect_to_bus, send_message, receive_message
import json
sock = connect_to_bus()

try:
    while True:
        print("\n1. Generar multa")
        print("2. Actualizar estado de Multa")
        print("3. Volver")
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
                print("¡Error! Por favor ingrese un monto válido.")
                continue
            datos = {"id_prestamo": int(entrada), "monto": float(monto)}
            payload = f"generar|{json.dumps(datos)}"
            send_message(sock, "multa", payload)   
            print(f"Esperando respuesta del servicio ({entrada}s)...")
            data = receive_message(sock)        
            if data:
            # Mostrar el mensaje (quitando los 5 caracteres del nombre del servicio)
                print(f"Respuesta recibida: {data[5:].decode()}")

        if opcion == '2':
            id_multa = input('Ingrese el ID de la multa a actualizar: ')
            if not id_multa.isdigit():
                print("¡Error! El ID debe ser un número.")
                continue
            payload = f"actualizar|{json.dumps({'id_prestamo': int(id_multa)})}"
            send_message(sock, "multa", payload)
            data = receive_message(sock)
            if data:
                print(f"Respuesta recibida: {data[5:].decode()}")   
        if opcion == '3':
            break
finally:
    print('Cerrando conexión')
    sock.close()
