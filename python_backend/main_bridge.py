import sys
import json
import os

# Asegurar que reconozca el directorio backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import database_handler as db
    import procesador as proc
except Exception as e:
    print(json.dumps({"status": "error", "message": f"Error importando módulos: {str(e)}"}))
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Faltan argumentos"}))
        return

    comando = sys.argv[1]

    try:
        # 1. REGISTRO
        if comando == "registrar" and len(sys.argv) >= 4:
            usr, pwd = sys.argv[2], sys.argv[3]
            res = db.registrar_usuario(usr, pwd)
            if res:
                print(json.dumps({"status": "ok", "message": "Registrado"}))
            else:
                print(json.dumps({"status": "error", "message": "Usuario existente"}))

        # 2. LOGIN
        elif comando == "login" and len(sys.argv) >= 4:
            usr, pwd = sys.argv[2], sys.argv[3]
            res = db.validar_login(usr, pwd)
            if res:
                print(json.dumps({"status": "ok", "message": "Login exitoso"}))
            else:
                print(json.dumps({"status": "error", "message": "Credenciales incorrectas"}))

        # 3. CAPTURAR FOTO CÁMARA
        elif comando == "capturar_foto" and len(sys.argv) >= 3:
            ruta_salida = sys.argv[2]
            res = proc.capturar_foto_camara(ruta_salida)
            if res:
                print(json.dumps({"status": "ok", "message": "Foto capturada"}))
            else:
                print(json.dumps({"status": "error", "message": "Error al abrir cámara"}))

        # 4. PROCESAR FILTRO (GRISES, GAMMA, NEGATIVO, HISTOGRAMA, HSV)
        elif comando == "procesar" and len(sys.argv) >= 5:
            ruta_in = sys.argv[2]
            filtro = sys.argv[3]
            ruta_out = sys.argv[4]
            gamma_val = float(sys.argv[5]) if len(sys.argv) >= 6 else 1.0

            if filtro == "Grises":
                res = proc.convertir_grises_formula(ruta_in, ruta_out)
            elif filtro == "Gamma":
                res = proc.aplicar_gamma(ruta_in, ruta_out, gamma_val)
            elif filtro == "Negativo":
                res = proc.aplicar_negativo(ruta_in, ruta_out)
            elif filtro == "Histograma":
                res = proc.ecualizar_histograma(ruta_in, ruta_out)
            elif filtro in ["SegmentarRojo", "SegmentarVerde", "SegmentarAzul"]:
                color = filtro.replace("Segmentar", "").lower()
                res = proc.segmentar_color_hsv(ruta_in, ruta_out, color)
            else:
                res = False

            if res:
                print(json.dumps({"status": "ok", "message": "Procesado correctamente"}))
            else:
                print(json.dumps({"status": "error", "message": "Fallo al procesar imagen en OpenCV"}))

        # 5. GUARDAR MATRIZ EN BASE DE DATOS
        elif comando == "guardar_bd" and len(sys.argv) >= 4:
            ruta_img = sys.argv[2]
            tipo_filtro = sys.argv[3]
            res = db.guardar_imagen_pixeles(ruta_img, tipo_filtro)
            if res:
                print(json.dumps({"status": "ok", "message": "Guardado en BD"}))
            else:
                print(json.dumps({"status": "error", "message": "Fallo al guardar matriz"}))

        # 6. SEPARACIÓN DE CAPAS
        elif comando == "separar_capas" and len(sys.argv) >= 4:
            ruta_in = sys.argv[2]
            carpeta_out = sys.argv[3]
            res = proc.generar_separacion_capas(ruta_in, carpeta_out)
            if res:
                print(json.dumps({"status": "ok", "message": "Capas separadas"}))
            else:
                print(json.dumps({"status": "error", "message": "Fallo al generar capas"}))

        else:
            print(json.dumps({"status": "error", "message": f"Comando desconocido o faltan argumentos: {comando}"}))

    except Exception as ex:
        print(json.dumps({"status": "error", "message": f"Excepción en Python: {str(ex)}"}))

if __name__ == "__main__":
    main()