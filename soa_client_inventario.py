from soa_lib import connect_to_bus, send_message, receive_message
import json

try:
    sock = connect_to_bus()

    while True:
        print("\n1. Agregar producto")
        print("2. Quitar producto")
        print("3. Listar Productos")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

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

        elif opcion == '4':
            break
        else:
            print("Opción no válida. Por favor seleccione una opción del 1 al 4.")

finally:
    print('Cerrando conexión')
    sock.close()