import asyncio
import binascii
from bleak import BleakScanner
from datetime import datetime
from body_metrics import bodyMetrics

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

        # Leer datos durante 10 segundos después de encontrar los primeros datos válidos
        for _ in range(10):
            await asyncio.sleep(1)

        stop_event.set()  # Detener la lectura de datos

        print(f"Final Impedance: {globalImpedance}")
        print(f"Final Weight: {globalWeight}")  

        bm = bodyMetrics(weight=globalWeight, height=168, age=19, sex='male', impedance=globalImpedance)
        bm.saveMetricsToFile('body_metrics.txt')

if __name__ == "__main__":
    MISCALE_MAC = "d8:e7:2f:a6:39:a6"  # Reemplaza con la dirección MAC de tu báscula
    asyncio.run(main(MISCALE_MAC))
