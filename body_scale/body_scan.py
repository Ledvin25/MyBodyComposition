import asyncio
import binascii
from bleak import BleakScanner
from datetime import datetime
from enhanced_body_metrics import EnhancedBodyMetrics
from user_config import (
    USER_HEIGHT, USER_AGE, USER_SEX, MISCALE_MAC,
    USER_WAIST, USER_NECK, USER_HIP, USER_THIGH,
    OUTPUT_FILENAME, SCAN_TIMEOUT, READ_DURATION
)

async def main(MISCALE_MAC):
    stop_event = asyncio.Event()
    globalImpedance = 0
    globalWeight = 0

    # Variable para indicar si ya se han encontrado datos válidos
    valid_data_found = False

    def callback(device, advertising_data):
        nonlocal valid_data_found, globalImpedance, globalWeight
        if device.address.lower() == MISCALE_MAC:
            try:
                ### Xiaomi V2 Scale ###
                data = binascii.b2a_hex(advertising_data.service_data['0000181b-0000-1000-8000-00805f9b34fb']).decode('ascii')
                data = "1b18" + data
                data2 = bytes.fromhex(data[4:])
                ctrlByte1 = data2[1]
                isStabilized = ctrlByte1 & (1<<5)
                hasImpedance = ctrlByte1 & (1<<1)
                measunit = data[4:6]
                measured = int((data[28:30] + data[26:28]), 16) * 0.01
                unit = ''
                if measunit == "03": unit = 'lbs'
                if measunit == "02": unit = 'kg' ; measured = measured / 2
                miimpedance = str(int((data[24:26] + data[22:24]), 16))
                if unit and isStabilized:
                    if measured != 0 and int(miimpedance) != 0:
                        valid_data_found = True
                        globalImpedance = int(miimpedance)
                        globalWeight = measured
                        print(f"Weight: {measured} {unit}, Impedance: {miimpedance}")
            except KeyError:
                pass
            try:
                ### Xiaomi V1 Scale ###
                data = binascii.b2a_hex(advertising_data.service_data['0000181d-0000-1000-8000-00805f9b34fb']).decode('ascii')
                data = "1d18" + data
                measunit = data[4:6]
                measured = int((data[8:10] + data[6:8]), 16) * 0.01
                unit = ''
                if measunit.startswith(('03', 'a3')): unit = 'lbs'
                if measunit.startswith(('12', 'b2')): unit = 'jin'
                if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
                if unit:
                    if measured != 0:
                        valid_data_found = True
                        globalWeight = measured
                        print(f"Weight: {measured} {unit}")
            except KeyError:
                pass

    async with BleakScanner(
        callback,
        device="hci0"
        ) as scanner:
        while not valid_data_found:
            await asyncio.sleep(1)  # Esperar hasta que se encuentren datos válidos

        # Leer datos durante el tiempo configurado después de encontrar los primeros datos válidos
        for _ in range(READ_DURATION):
            await asyncio.sleep(1)

        stop_event.set()  # Detener la lectura de datos

        print(f"Final Impedance: {globalImpedance}")
        print(f"Final Weight: {globalWeight}")  

        # Crear instancia de EnhancedBodyMetrics con datos del usuario
        print("\nCalculando composición corporal...")
        
        # Crear diccionario con argumentos básicos
        metrics_args = {
            'weight': globalWeight,
            'height': USER_HEIGHT,
            'age': USER_AGE,
            'sex': USER_SEX,
            'impedance': globalImpedance
        }
        
        # Agregar datos antropométricos si están disponibles
        if USER_WAIST is not None:
            metrics_args['waist'] = USER_WAIST
        if USER_NECK is not None:
            metrics_args['neck'] = USER_NECK
        if USER_HIP is not None:
            metrics_args['hip'] = USER_HIP
        if USER_THIGH is not None:
            metrics_args['thigh'] = USER_THIGH
        
        # Crear instancia de métricas
        bm = EnhancedBodyMetrics(**metrics_args)
        
        # Mostrar resumen en consola
        bm.print_summary()
        
        # Guardar métricas completas en archivo
        bm.save_metrics_to_file(OUTPUT_FILENAME)
        
        print(f"\n✅ Análisis completado. Resultados guardados en: {OUTPUT_FILENAME}")
        
        return bm  # Retornar la instancia para uso posterior

if __name__ == "__main__":
    print("🏃‍♂️ Iniciando escáner de composición corporal...")
    print(f"📡 Buscando báscula: {MISCALE_MAC}")
    print(f"👤 Usuario: {USER_AGE} años, {USER_HEIGHT}cm, {USER_SEX}")
    if USER_WAIST or USER_NECK:
        print("📏 Datos antropométricos adicionales configurados")
    print("⚖️  Asegúrate de que la báscula esté encendida y sube a ella para obtener mediciones...")
    print()
    
    try:
        result = asyncio.run(main(MISCALE_MAC))
    except KeyboardInterrupt:
        print("\n❌ Medición cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la medición: {e}")
