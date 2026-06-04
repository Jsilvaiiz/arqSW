from soa_lib import connect_to_bus, send_message, receive_message
import time

sock = connect_to_bus()

#Alertas

try:
    # 1. Registro inicial (sinit)
    print("Registrando servicio 'servi'...")
    send_message(sock, "sinit", "alert") # nombre del servicio es "alertas"
    
    # 2. Procesar respuesta del sinit
    init_data = receive_message(sock)
    print(f"Confirmación de bus recibida: {init_data!r}")
    print("Servicio listo para recibir transacciones.\n")
    
    # 3. Bucle principal de trabajo
    while True:
        data = receive_message(sock)
        if not data:
            print("Conexión cerrada por el bus.")
            break
            
        # Extraer el payload (salta los 5 caracteres del nombre del servicio)
        
        #Parametros de entrada
        #id reporte
        #mensaje
        mensaje = data[5:].decode()
        print(f"Mensaje recibido del cliente: '{mensaje}'")
        try:
            #
            # Separar id y mensae
            mensaje = mensaje.split(";")
            id_reporte = mensaje[0]
            mensaje = mensaje[1]
            print(f"ID: {id_reporte}, Mensaje: {mensaje}")
            id_Alerta = 1 # Aqui se puede generar un ID unico para cada alerta, por simplicidad se usa un ID fijo
            send_message(sock,"alert", str(id_Alerta))
            print("Respuesta 'OK' enviada.")
            
        except ValueError:
            #escribir mensajes de error validos para el servicio
            print(f"Error: '{mensaje}' no es un número válido.")
            send_message(sock, "alert", "Error: Formato incorrecto")

except Exception as e:
    print(f"Error en el servicio: {e}")
finally:
    print('Cerrando socket del servicio')
    sock.close()
