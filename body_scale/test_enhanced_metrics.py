#!/usr/bin/env python3
"""
Script de prueba para simular datos de la báscula y probar EnhancedBodyMetrics
"""

from enhanced_body_metrics import EnhancedBodyMetrics

def test_enhanced_metrics():
    """Prueba la nueva clase con diferentes perfiles de usuario"""
    
    print("=== PRUEBAS DE ENHANCED BODY METRICS ===\n")
    
    # Perfil 1: Hombre joven atlético
    print("--- PERFIL 1: Hombre joven atlético ---")
    em1 = EnhancedBodyMetrics(
        weight=75.0,
        height=180,
        age=25,
        sex='male',
        impedance=450,  # Impedancia típica de persona atlética (menor resistencia)
        waist=80,
        neck=38
    )
    em1.print_summary()
    em1.save_metrics_to_file('perfil_atletico.txt')
    
    print("\n" + "="*50 + "\n")
    
    # Perfil 2: Mujer adulta promedio
    print("--- PERFIL 2: Mujer adulta promedio ---")
    em2 = EnhancedBodyMetrics(
        weight=65.0,
        height=165,
        age=35,
        sex='female',
        impedance=550,  # Impedancia típica de mujer
        waist=75,
        neck=32
    )
    em2.print_summary()
    em2.save_metrics_to_file('perfil_mujer.txt')
    
    print("\n" + "="*50 + "\n")
    
    # Perfil 3: Hombre con sobrepeso
    print("--- PERFIL 3: Hombre con sobrepeso ---")
    em3 = EnhancedBodyMetrics(
        weight=95.0,
        height=175,
        age=45,
        sex='male',
        impedance=600,  # Mayor impedancia por mayor grasa corporal
        waist=100,
        neck=42
    )
    em3.print_summary()
    em3.save_metrics_to_file('perfil_sobrepeso.txt')
    
    print("\n" + "="*50 + "\n")
    
    # Perfil 4: Sin datos antropométricos (solo báscula)
    print("--- PERFIL 4: Solo datos de báscula ---")
    em4 = EnhancedBodyMetrics(
        weight=70.0,
        height=170,
        age=30,
        sex='male',
        impedance=500
        # Sin waist, neck, etc.
    )
    em4.print_summary()
    em4.save_metrics_to_file('perfil_basico.txt')

def simulate_scale_reading():
    """Simula una lectura de la báscula con datos realistas"""
    
    print("\n=== SIMULACIÓN DE LECTURA DE BÁSCULA ===\n")
    
    # Datos simulados de la báscula
    simulated_weight = 75.5  # kg
    simulated_impedance = 485  # ohm
    
    print(f"Datos recibidos de la báscula:")
    print(f"Peso: {simulated_weight} kg")
    print(f"Impedancia: {simulated_impedance} ohm")
    print()
    
    # Crear métricas con los datos simulados
    bm = EnhancedBodyMetrics(
        weight=simulated_weight,
        height=178,  # Altura del usuario (configurable)
        age=28,      # Edad del usuario (configurable)
        sex='male',  # Sexo del usuario (configurable)
        impedance=simulated_impedance
    )
    
    print("Análisis de composición corporal:")
    bm.print_summary()
    bm.save_metrics_to_file('lectura_simulada.txt')

if __name__ == "__main__":
    test_enhanced_metrics()
    simulate_scale_reading()
