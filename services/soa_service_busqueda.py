from soa_lib import connect_to_bus, send_message, receive_message
import time
import os
import json

INVENTARIO_FILE = 'inventario.json'

def cargar_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        return [] 
    with open(INVENTARIO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Se conecta al bus
sock = connect_to_bus()

try:
    nombre_servicio = "binve"
    print(f"Registrando servicio '{nombre_servicio}' en el BUS...")
    send_message(sock, "sinit", nombre_servicio)
    
    init_data = receive_message(sock)
    print(f"Confirmación de bus recibida: {init_data!r}")
    print("Servicio de Búsqueda de Inventario listo.\n")
    
    while True:
        data = receive_message(sock)
        if not data:
            print("Conexión cerrada por el bus.")
            break
            
        payload = data[5:].decode()
        print(f"Petición cruda recibida: '{payload}'")
        
        partes = payload.split(";")
        accion = partes[0].upper()
        
        base_datos_inventario = cargar_inventario()
        
        # --- OPERACIÓN 1: FILTRAR / BUSCAR RECURSO ---
        if accion == "BUSCAR":
            if len(partes) < 3:
                send_message(sock, nombre_servicio, "ERROR: Faltan parámetros (Uso: BUSCAR;campo;valor)")
                continue
                
            campo = partes[1].lower()  
            valor_buscado = partes[2].lower()
            
            lineas = []
            for info in base_datos_inventario:
                if campo in info and valor_buscado in str(info[campo]).lower():
                    formato = f"[ID: {info.get('id')}] Nombre: {info.get('nombre')} | Cat: {info.get('categoria')} | Stock: {info.get('stock')} | Desc: {info.get('descripcion')}"
                    lineas.append(formato)
            
            if not lineas:
                send_message(sock, nombre_servicio, f"INFO: No se encontraron recursos con {campo} que contenga '{partes[2]}'")
            else:
                respuesta = "\n" + "\n".join(lineas)
                send_message(sock, nombre_servicio, respuesta)
            
        # --- OPERACIÓN 2: VER TODO EL INVENTARIO ---
        elif accion == "LISTAR":
            if not base_datos_inventario:
                send_message(sock, nombre_servicio, "INFO: El inventario se encuentra vacío.")
                continue
            
            lineas = []
            for info in base_datos_inventario:
                formato = f"[ID: {info.get('id')}] Nombre: {info.get('nombre')} | Cat: {info.get('categoria')} | Stock: {info.get('stock')} | Desc: {info.get('descripcion')}"
                lineas.append(formato)
            
            respuesta = "\n" + "\n".join(lineas)
            send_message(sock, nombre_servicio, respuesta)
        
        else:
            send_message(sock, nombre_servicio, "ERROR: Comando no reconocido. Usa BUSCAR o LISTAR")

except Exception as e:
    print(f"Error crítico en el servicio de búsqueda: {e}")
finally:
    print("Cerrando socket de servicio...")
    sock.close()