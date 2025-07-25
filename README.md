# 🏃‍♂️ MyBodyComposition - Sistema Avanzado de Análisis Corporal

Sistema de análisis de composición corporal que utiliza básculas Xiaomi Mi Body Composition Scale y fórmulas científicas validadas contra DEXA, RMN y otros métodos de referencia.

## 🚀 Características

- **Fórmulas científicas validadas**: Utiliza ecuaciones de Wu et al. (2015), Janssen et al. (2000), Kushner & Schoeller, y Liu et al. (2022)
- **Soporte para básculas Xiaomi**: Compatible con V1 y V2 de Mi Body Composition Scale
- **Análisis completo**: BMI, grasa corporal, masa muscular, agua corporal, metabolismo basal, grasa visceral
- **Datos antropométricos opcionales**: Mejora la precisión con medidas de cintura, cuello, cadera y muslo
- **Reportes detallados**: Guarda resultados en archivos con referencias científicas

## 📊 Métricas Calculadas

### Básicas
- **IMC (BMI)**: Índice de masa corporal
- **% Grasa corporal**: Basado en FFM de Wu et al. (2015)
- **Masa libre de grasa (FFM)**: Fórmula Wu validada contra DEXA
- **Masa muscular esquelética**: Ecuación Janssen et al. (2000)

### Agua Corporal
- **Agua corporal total (TBW)**: Kushner & Schoeller
- **Agua extracelular (ECW)** e **intracelular (ICW)**
- **Porcentaje de hidratación**

### Metabolismo
- **Tasa metabólica basal (TMB)**: Cunningham (1980)

### Grasa Visceral (opcional)
- **Área de grasa visceral**: Liu et al. (2022) - requiere medidas de cintura y cuello

## 🛠️ Instalación

1. **Clona o descarga** este repositorio
2. **Instala dependencias**:
   ```bash
   pip install bleak
   ```

## ⚙️ Configuración

1. **Edita `user_config.py`** con tus datos:
   ```python
   USER_HEIGHT = 175      # Tu altura en cm
   USER_AGE = 30         # Tu edad
   USER_SEX = 'male'     # 'male' o 'female'
   MISCALE_MAC = "xx:xx:xx:xx:xx:xx"  # MAC de tu báscula
   
   # Opcionales para mayor precisión
   USER_WAIST = 85       # Circunferencia de cintura en cm
   USER_NECK = 40        # Circunferencia de cuello en cm
   ```

2. **Encuentra la MAC de tu báscula**:
   - Android: Apps como "BLE Scanner"
   - iOS: Apps como "LightBlue"
   - Windows: Configuración > Bluetooth > Dispositivos

## 🏃‍♂️ Uso

### Análisis con Báscula
```bash
python body_scan.py
```

1. Ejecuta el script
2. Asegúrate de que la báscula esté encendida
3. Sube a la báscula para activar la medición
4. Espera a que se capturen peso e impedancia
5. Los resultados se guardan automáticamente

### Pruebas sin Báscula
```bash
python test_enhanced_metrics.py
```

## 📁 Archivos Generados

- **`my_body_metrics.txt`**: Reporte completo de tu análisis
- **Archivos de prueba**: `perfil_atletico.txt`, `perfil_mujer.txt`, etc.

## 📝 Ejemplo de Reporte

```
=== REPORTE DE COMPOSICIÓN CORPORAL ===
Fecha: 2025-01-25 14:30:15

--- DATOS BÁSICOS ---
Peso: 75.5 kg
Altura: 178 cm
Edad: 28 años
Sexo: male
Impedancia: 485 ohm

--- COMPOSICIÓN CORPORAL ---
Masa libre de grasa (FFM Wu): 58.6 kg
Porcentaje de grasa: 22.5%
Masa grasa: 17.0 kg
Masa muscular esquelética (Janssen): 33.1 kg

--- AGUA CORPORAL ---
Agua corporal total (TBW): 32.5 L
Agua extracelular (ECW): 12.4 L
Agua intracelular (ICW): 20.1 L
Porcentaje de agua: 43.1%

--- METABOLISMO ---
Tasa metabólica basal (Cunningham): 1634 kcal/día
```

## 🔬 Referencias Científicas

- **Wu et al. (2015)**: FFM validation against DEXA
- **Janssen et al. (2000)**: Skeletal muscle mass estimation
- **Kushner & Schoeller**: Total body water via BIA
- **Cunningham (1980)**: Basal metabolic rate
- **Liu et al. (2022)**: Visceral fat area estimation

## 🔧 Personalización

### Agregar Nuevas Fórmulas
Edita `enhanced_body_metrics.py` y agrega métodos siguiendo el patrón:

```python
def get_nueva_metrica(self) -> float:
    """Descripción de la nueva métrica"""
    resultado = # tu fórmula aquí
    return self._check_bounds(resultado, min_val, max_val)
```

### Modificar Rangos de Validación
Ajusta los límites en el método `_check_bounds()` según tus necesidades.

## ⚠️ Limitaciones

- **Precisión**: Las fórmulas son aproximaciones; para diagnósticos médicos consulta profesionales
- **Bluetooth**: Requiere conectividad Bluetooth funcional
- **Compatibilidad**: Probado con básculas Xiaomi Mi Body Composition Scale V1 y V2

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Especialmente:
- Nuevas fórmulas científicas validadas
- Soporte para otras básculas
- Mejoras en la interfaz de usuario
- Optimizaciones de precisión

## 📄 Licencia

Este proyecto es de código abierto. Úsalo responsablemente y siempre consulta profesionales de la salud para interpretación médica de los resultados.
