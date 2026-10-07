import sys
import os
import cv2
import json
from database_handler import registrar_usuario, validar_login, guardar_imagen_pixeles
from procesador import (
    convertir_grises_formula,
    aplicar_gamma,
    aplicar_negativo,
    ecualizar_histograma,
    segmentar_color_hsv,
    generar_separacion_capas,
    capturar_foto_camara
)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No se proporcionó ningún comando"}))
        return

    comando = sys.argv[1]

    # 1. Comandos de Usuario / Login
    if comando == "registrar":
        # Argumentos: comando, nombre, ap_pat, ap_mat, usuario, contrasena
        if len(sys.argv) >= 7:
            exito = registrar_usuario(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            print(json.dumps({"status": "ok" if exito else "error"}))
        else:
            print(json.dumps({"status": "error", "message": "Faltan datos de registro"}))

    elif comando == "login":
        # Argumentos: comando, usuario, contrasena
        if len(sys.argv) >= 4:
            exito = validar_login(sys.argv[2], sys.argv[3])
            print(json.dumps({"status": "ok" if exito else "error"}))
        else:
            print(json.dumps({"status": "error", "message": "Faltan credenciales"}))

    # 2. Comando para Captura de Foto de Cámara Web
    elif comando == "capturar_foto":
        # Argumentos: comando, ruta_salida
        ruta_salida = sys.argv[2] if len(sys.argv) >= 3 else "captura_temp.jpg"
        exito = capturar_foto_camara(ruta_salida)
        print(json.dumps({"status": "ok" if exito else "error", "ruta": ruta_salida}))

    # 3. Comandos de Procesamiento de Visión Artificial
    elif comando == "procesar":
        # Argumentos: comando, ruta_entrada, tipo_proceso, ruta_salida, [parametro_extra]
        if len(sys.argv) < 5:
            print(json.dumps({"status": "error", "message": "Faltan parametros de procesamiento"}))
            return

        ruta_in = sys.argv[2]
        tipo = sys.argv[3]
        ruta_out = sys.argv[4]

        imagen = cv2.imread(ruta_in)
        if imagen is None:
            print(json.dumps({"status": "error", "message": "No se pudo leer la imagen"}))
            return

        img_resultado = None

        if tipo == "Grises":
            img_resultado = convertir_grises_formula(imagen)
        elif tipo == "Gamma":
            gamma_val = float(sys.argv[5]) if len(sys.argv) >= 6 else 0.8
            img_resultado = aplicar_gamma(imagen, gamma=gamma_val)
        elif tipo == "Negativo":
            img_resultado = aplicar_negativo(imagen)
        elif tipo == "Histograma":
            img_resultado = ecualizar_histograma(imagen)
        elif tipo == "SegmentarRojo":
            img_resultado = segmentar_color_hsv(imagen, 'Rojo')
        elif tipo == "SegmentarVerde":
            img_resultado = segmentar_color_hsv(imagen, 'Verde')
        elif tipo == "SegmentarAzul":
            img_resultado = segmentar_color_hsv(imagen, 'Azul')
        else:
            img_resultado = imagen

        cv2.imwrite(ruta_out, img_resultado)
        print(json.dumps({"status": "ok", "ruta_resultado": ruta_out}))

    # 4. Guardado final de Matriz de Píxeles en la Base de Datos
    elif comando == "guardar_bd":
        # Argumentos: comando, ruta_imagen, tipo_proceso
        if len(sys.argv) >= 4:
            exito = guardar_imagen_pixeles(sys.argv[2], sys.argv[3])
            print(json.dumps({"status": "ok" if exito else "error"}))
        else:
            print(json.dumps({"status": "error", "message": "Faltan parametros para guardar en BD"}))

    # 5. Generar Separación de Capas (R, G, B, M, Y, C)
    elif comando == "separar_capas":
        # Argumentos: comando, ruta_imagen, carpeta_destino
        if len(sys.argv) >= 4:
            ruta_in = sys.argv[2]
            carpeta_out = sys.argv[3]
            os.makedirs(carpeta_out, exist_ok=True)
            
            imagen = cv2.imread(ruta_in)
            if imagen is not None:
                capas = generar_separacion_capas(imagen)
                rutas_capas = {}
                for nombre_capa, img_capa in capas.items():
                    r_out = os.path.join(carpeta_out, f"capa_{nombre_capa}.jpg")
                    cv2.imwrite(r_out, img_capa)
                    rutas_capas[nombre_capa] = r_out
                print(json.dumps({"status": "ok", "capas": rutas_capas}))
            else:
                print(json.dumps({"status": "error", "message": "No se pudo leer la imagen"}))
        else:
            print(json.dumps({"status": "error", "message": "Faltan parametros para separacion de capas"}))

if __name__ == "__main__":
    main()