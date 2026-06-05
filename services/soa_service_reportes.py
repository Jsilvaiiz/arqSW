import sys
sys.path.append('..')
from soa_lib import connect_to_bus, send_message, receive_message
import time
import os
import json

REPORTES_FILE = 'reportes.json'

# Función para cargar los reportes desde el archivo JSON
def cargar_reportes():
    if not os.path.exists(REPORTES_FILE):
        return {}  # Retorna un diccionario vacío si el archivo no existe
    with open(REPORTES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # IMPORTANTE: JSON convierte las llaves a string. 
        # Las transformamos de vuelta a int para mantener compatibilidad con tu código.
        return {int(k): v for k, v in data.items()}

# Función para guardar los reportes en el archivo JSON
def guardar_reportes(reportes):
    with open(REPORTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, indent=2, ensure_ascii=False)

# Se conecta al bus
sock = connect_to_bus()

try:
    nombre_servicio = "repor"
    print(f"Registrando servicio '{nombre_servicio}' en el BUS...")
    send_message(sock, "sinit", nombre_servicio)
    
    init_data = receive_message(sock)
    print(f"Confirmación de bus recibida: {init_data!r}")
    print("Servicio de Reportes listo para recibir transacciones.\n")
    
    base_datos_reportes = cargar_reportes()
    
    if base_datos_reportes:
        id_contador = max(base_datos_reportes.keys()) + 1
    else:
        id_contador = 1
    
    while True:
        data = receive_message(sock)
        if not data:
            print("Conexión cerrada por el bus.")
            break
            
        payload = data[5:].decode()
        print(f"Petición cruda recibida: '{payload}'")
        
        partes = payload.split(";")
        accion = partes[0].upper()
        
        # --- OPERACIÓN 1: CREAR REPORTE ---
        if accion == "CREAR":
            if len(partes) < 4:
                send_message(sock, nombre_servicio, "ERROR: Faltan parámetros (Uso: CREAR;categoria;id_recurso;descripcion)")
                continue
                
            categoria = partes[1].lower()
            id_recurso = partes[2]
            descripcion = partes[3]
            
            if categoria not in ["pérdida", "daño", "mantenimiento"]:
                send_message(sock, nombre_servicio, "ERROR: Categoría inválida (Debe ser: pérdida, daño o mantenimiento)")
                continue
            
            nuevo_reporte = {
                "id_reporte": id_contador,
                "categoria": categoria,
                "id_recurso": id_recurso,
                "descripcion": descripcion,
                "estado": "pendiente"
            }
            base_datos_reportes[id_contador] = nuevo_reporte
            
            guardar_reportes(base_datos_reportes)
            
            respuesta = f"OK: Reporte ID {id_contador} creado exitosamente con estado 'pendiente'"
            id_contador += 1
            send_message(sock, nombre_servicio, respuesta)
            
        # --- OPERACIÓN 2: MODIFICAR ESTADO ---
        elif accion == "ESTADO":
            if len(partes) < 3:
                send_message(sock, nombre_servicio, "ERROR: Faltan parámetros (Uso: ESTADO;id_reporte;nuevo_estado)")
                continue
                
            try:
                id_rep = int(partes[1])
                nuevo_estado = partes[2].lower()
                
                if nuevo_estado not in ["pendiente", "en proceso", "cerrado"]:
                    send_message(sock, nombre_servicio, "ERROR: Estado inválido (Debe ser: pendiente, en proceso o cerrado)")
                    continue
                    
                if id_rep in base_datos_reportes:
                    base_datos_reportes[id_rep]["estado"] = nuevo_estado
                    
                    guardar_reportes(base_datos_reportes)
                    
                    send_message(sock, nombre_servicio, f"OK: Estado del reporte {id_rep} cambiado a '{nuevo_estado}'")
                else:
                    send_message(sock, nombre_servicio, "ERROR: El ID de reporte no existe")
                    
            except ValueError:
                send_message(sock, nombre_servicio, "ERROR: El ID de reporte debe ser un número entero")

        # --- OPERACIÓN 3: ELIMINAR REPORTE ---
        elif accion == "ELIMINAR":
            if len(partes) < 3:
                send_message(sock, nombre_servicio, "ERROR: Faltan parámetros (Uso: ELIMINAR;id_reporte;rol_usuario)")
                continue
                
            try:
                id_rep = int(partes[1])
                rol_usuario = partes[2].lower()
                
                if rol_usuario != "administrador":
                    send_message(sock, nombre_servicio, "ERROR: Permiso denegado. Solo el 'administrador' puede eliminar reportes")
                    continue
                    
                if id_rep in base_datos_reportes:
                    del base_datos_reportes[id_rep]
                    
                    guardar_reportes(base_datos_reportes)
                    
                    send_message(sock, nombre_servicio, f"OK: Reporte {id_rep} eliminado de la base de datos")
                else:
                    send_message(sock, nombre_servicio, "ERROR: El ID de reporte no existe")
                    
            except ValueError:
                send_message(sock, nombre_servicio, "ERROR: El ID de reporte debe ser un número entero")
                
        # --- OPERACIÓN 4: VER TODOS LOS REPORTES ---
        elif accion == "LISTAR":
            if not base_datos_reportes:
                send_message(sock, nombre_servicio, "INFO: No hay reportes registrados en el sistema.")
                continue
            
            lineas = []
            for id_rep, info in base_datos_reportes.items():
                formato = f"[ID: {id_rep}] Cat: {info['categoria']} | Recurso ID: {info['id_recurso']} | Estado: {info['estado']} | Descripción: {info['descripcion']}"
                lineas.append(formato)
            
            respuesta = "\n" + "\n".join(lineas)
            send_message(sock, nombre_servicio, respuesta)
        
        else:
            send_message(sock, nombre_servicio, "ERROR: Comando no reconocido. Usa CREAR, ESTADO o ELIMINAR")

except Exception as e:
    print(f"Error crítico en el servicio de reportes: {e}")
finally:
    print("Cerrando socket de servicio...")
    sock.close()