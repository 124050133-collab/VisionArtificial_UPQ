import cv2
import numpy as np
import os

def cargar_imagen_segura(ruta):
    try:
        # Lee la imagen correctamente en Windows aunque la ruta tenga espacios o caracteres especiales
        img = cv2.imdecode(np.fromfile(ruta, dtype=np.uint8), cv2.IMREAD_COLOR)
        return img
    except Exception:
        return cv2.imread(ruta)

def guardar_imagen_segura(ruta, img):
    try:
        ext = os.path.splitext(ruta)[1]
        is_success, buffer = cv2.imencode(ext, img)
        if is_success:
            with open(ruta, "wb") as f:
                f.write(buffer)
            return True
        return False
    except Exception:
        return cv2.imwrite(ruta, img)

# 1. Escala de grises por fórmula de luminancia ponderada
def convertir_grises_formula(ruta_in, ruta_out):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    # Luminancia: Gray = 0.2989*R + 0.5870*G + 0.1140*B
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray = np.clip(gray, 0, 255).astype(np.uint8)
    return guardar_imagen_segura(ruta_out, gray)

# 2. Corrección Gamma
def aplicar_gamma(ruta_in, ruta_out, gamma=1.0):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    inv_gamma = 1.0 / gamma
    tabla = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    img_gamma = cv2.LUT(img, tabla)
    return guardar_imagen_segura(ruta_out, img_gamma)

# 3. Negativo fotográfico
def aplicar_negativo(ruta_in, ruta_out):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    negativo = 255 - img
    return guardar_imagen_segura(ruta_out, negativo)

# 4. Ecualización de histograma (CORREGIDA: Acepta ruta_in y ruta_out)
def ecualizar_histograma(ruta_in, ruta_out):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    
    # Si es imagen a color BGR, ecualizamos cada canal por separado
    if len(img.shape) == 3:
        b, g, r = cv2.split(img)
        eb = cv2.equalizeHist(b)
        eg = cv2.equalizeHist(g)
        er = cv2.equalizeHist(r)
        img_eq = cv2.merge((eb, eg, er))
    else:
        img_eq = cv2.equalizeHist(img)
        
    return guardar_imagen_segura(ruta_out, img_eq)

# 5. Segmentación por color HSV
def segmentar_color_hsv(ruta_in, ruta_out, color='rojo'):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    if color == 'rojo':
        lower1 = np.array([0, 70, 50])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 70, 50])
        upper2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = mask1 | mask2
    elif color == 'verde':
        lower = np.array([36, 25, 25])
        upper = np.array([86, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color == 'azul':
        lower = np.array([94, 80, 2, np.uint8])
        upper = np.array([126, 255, 255, np.uint8])
        mask = cv2.inRange(hsv, lower, upper)
    else:
        return False

    res = cv2.bitwise_and(img, img, mask=mask)
    return guardar_imagen_segura(ruta_out, res)

# 6. Separación de 6 Capas (RGB + CMY)
def generar_separacion_capas(ruta_in, carpeta_out):
    img = cargar_imagen_segura(ruta_in)
    if img is None:
        return False
    
    if not os.path.exists(carpeta_out):
        os.makedirs(carpeta_out)
        
    b, g, r = cv2.split(img)
    zeros = np.zeros_like(b)

    # Primarios (RGB)
    rojo = cv2.merge([zeros, zeros, r])
    verde = cv2.merge([zeros, g, zeros])
    azul = cv2.merge([b, zeros, zeros])

    # Sustractivos / Secundarios (CMY)
    magenta = cv2.merge([b, zeros, r])
    amarillo = cv2.merge([zeros, g, r])
    cian = cv2.merge([b, g, zeros])

    guardar_imagen_segura(f"{carpeta_out}/capa_Rojo.jpg", rojo)
    guardar_imagen_segura(f"{carpeta_out}/capa_Verde.jpg", verde)
    guardar_imagen_segura(f"{carpeta_out}/capa_Azul.jpg", azul)
    guardar_imagen_segura(f"{carpeta_out}/capa_Magenta.jpg", magenta)
    guardar_imagen_segura(f"{carpeta_out}/capa_Amarillo.jpg", amarillo)
    guardar_imagen_segura(f"{carpeta_out}/capa_Cian.jpg", cian)

    return True

# 7. Captura de Cámara Web
def capturar_foto_camara(ruta_out):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
    ret, frame = cap.read()
    cap.release()
    if ret:
        return guardar_imagen_segura(ruta_out, frame)
    return False