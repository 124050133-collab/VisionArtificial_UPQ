import cv2
import numpy as np

def convertir_grises_formula(imagen_bgr):
    
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    cRojo = imagen_rgb[:, :, 0]
    cVerde = imagen_rgb[:, :, 1]
    cAzul = imagen_rgb[:, :, 2]
    
    gray_image = 0.2989 * cRojo + 0.5870 * cVerde + 0.1140 * cAzul
    return gray_image.astype(np.uint8)

def aplicar_gamma(imagen, gamma=0.8):
   
    img_norm = imagen / 255.0
    img_gamma = np.power(img_norm, gamma)
    return np.uint8(img_gamma * 255)

def aplicar_negativo(imagen_bgr):
    
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    R = imagen_rgb[:, :, 0]
    G = imagen_rgb[:, :, 1]
    B = imagen_rgb[:, :, 2]
    
    R_Neg = 255 - R
    G_Neg = 255 - G
    B_Neg = 255 - B
    
    img_rgb_neg = cv2.merge((R_Neg, G_Neg, B_Neg))
    return cv2.cvtColor(img_rgb_neg, cv2.COLOR_RGB2BGR)

def ecualizar_histograma(imagen_bgr):
   
    B, G, R = cv2.split(imagen_bgr)
    b_eq = cv2.equalizeHist(B)
    g_eq = cv2.equalizeHist(G)
    r_eq = cv2.equalizeHist(R)
    return cv2.merge((b_eq, g_eq, r_eq))

def segmentar_color_hsv(imagen_bgr, color='Rojo'):
   
    hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)
    
    # Definición de rangos según el color solicitado
    if color == 'Rojo':
        lower1 = np.array([0, 100, 20], dtype=np.uint8)
        upper1 = np.array([10, 255, 255], dtype=np.uint8)
        lower2 = np.array([175, 100, 20], dtype=np.uint8)
        upper2 = np.array([180, 255, 255], dtype=np.uint8)
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mascara = cv2.add(mask1, mask2)
    elif color == 'Verde':
        lower = np.array([36, 100, 20], dtype=np.uint8)
        upper = np.array([70, 255, 255], dtype=np.uint8)
        mascara = cv2.inRange(hsv, lower, upper)
    elif color == 'Azul':
        lower = np.array([100, 100, 20], dtype=np.uint8)
        upper = np.array([130, 255, 255], dtype=np.uint8)
        mascara = cv2.inRange(hsv, lower, upper)
    else:
        return imagen_bgr

    # Aplicar la máscara sobre la imagen original BGR
    resultado = cv2.bitwise_and(imagen_bgr, imagen_bgr, mask=mascara)
    return resultado

def generar_separacion_capas(imagen_bgr):
    
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    
    cRojo = imagen_rgb[:, :, 0]
    cVerde = imagen_rgb[:, :, 1]
    cAzul = imagen_rgb[:, :, 2]
    
    cRojoAzul = imagen_rgb[:, :, [0, 2]]
    cRojoVerde = imagen_rgb[:, :, [0, 1]]
    cVerdeAzul = imagen_rgb[:, :, [1, 2]]
    
    # Creación de matrices aisladas
    R = np.zeros_like(imagen_rgb)
    R[:, :, 0] = cRojo
    
    G = np.zeros_like(imagen_rgb)
    G[:, :, 1] = cVerde
    
    B = np.zeros_like(imagen_rgb)
    B[:, :, 2] = cAzul
    
    M = np.zeros_like(imagen_rgb)
    M[:, :, [0, 2]] = cRojoAzul
    
    Y = np.zeros_like(imagen_rgb)
    Y[:, :, [0, 1]] = cRojoVerde
    
    C = np.zeros_like(imagen_rgb)
    C[:, :, [1, 2]] = cVerdeAzul
    
    # Convertir todas de regreso a BGR para guardar o mostrar correctamente
    return {
        "Rojo": cv2.cvtColor(R, cv2.COLOR_RGB2BGR),
        "Verde": cv2.cvtColor(G, cv2.COLOR_RGB2BGR),
        "Azul": cv2.cvtColor(B, cv2.COLOR_RGB2BGR),
        "Magenta": cv2.cvtColor(M, cv2.COLOR_RGB2BGR),
        "Amarillo": cv2.cvtColor(Y, cv2.COLOR_RGB2BGR),
        "Cian": cv2.cvtColor(C, cv2.COLOR_RGB2BGR)
    }

def capturar_foto_camara(nombre_salida="captura_temp.jpg"):
    
    captura = cv2.VideoCapture(0)
    if not captura.isOpened():
        return False
    
    ret, imagen = captura.read()
    captura.release()
    
    if ret:
        imagen = cv2.flip(imagen, 1)  # Efecto espejo
        cv2.imwrite(nombre_salida, imagen)
        return True
    return False

if __name__ == "__main__":
    print("Módulo de procesamiento cargado correctamente.")