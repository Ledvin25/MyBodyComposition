# Configuración del usuario para análisis de composición corporal
# Modifica estos valores según tus datos personales

# DATOS BÁSICOS (OBLIGATORIOS)
USER_HEIGHT = 170      # Altura en centímetros
USER_AGE = 20         # Edad en años
USER_SEX = 'male'     # 'male' o 'female'

# DIRECCIÓN MAC DE LA BÁSCULA
MISCALE_MAC = "d8:e7:2f:a6:39:a6"

# DATOS ANTROPOMÉTRICOS OPCIONALES (para cálculos más precisos)
# Deja en None si no tienes estos datos
USER_WAIST = 87     # Circunferencia de cintura en cm
USER_NECK = 43      # Circunferencia de cuello en cm  
USER_HIP = 91       # Circunferencia de cadera en cm
USER_THIGH = 65     # Circunferencia de muslo en cm

# CONFIGURACIÓN DE ARCHIVOS
OUTPUT_FILENAME = 'my_body_metrics.txt'

# CONFIGURACIÓN DE BLUETOOTH
SCAN_TIMEOUT = 30     # Tiempo máximo de escaneo en segundos
READ_DURATION = 10    # Duración de lectura después de encontrar datos válidos
