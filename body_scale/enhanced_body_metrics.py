from math import floor
import sys
from datetime import datetime

class EnhancedBodyMetrics:
    """
    Clase mejorada para cálculo de composición corporal usando fórmulas validadas
    contra DEXA, RMN, dilución, etc., y datos opcionales de antropometría.
    """
    def __init__(self,
                 weight: float,
                 height: float,
                 age: int,
                 sex: str,
                 impedance: float,
                 waist: float = None,
                 neck: float = None,
                 hip: float = None,
                 thigh: float = None):
        # Valores básicos
        self.weight = weight            # kg
        self.height = height            # cm
        self.age = age                  # años
        self.sex = sex.lower()          # 'male' o 'female'
        self.impedance = impedance      # ohm
        # Datos opcionales antropométricos
        self.waist = waist              # cm
        self.neck = neck                # cm
        self.hip = hip                  # cm
        self.thigh = thigh              # cm

        # Validaciones iniciales
        if not (10 <= self.weight <= 300):
            raise ValueError("Weight debe estar entre 10 y 300 kg")
        if not (100 <= self.height <= 250):
            raise ValueError("Height debe estar entre 100 y 250 cm")
        if not (5 <= self.age <= 120):
            raise ValueError("Age debe estar entre 5 y 120 años")
        if self.sex not in ('male', 'female'):
            raise ValueError("Sex debe ser 'male' o 'female'")

    def _check_bounds(self, value: float, minimum: float, maximum: float) -> float:
        """Asegura que el valor quede dentro de sus límites"""
        return max(minimum, min(maximum, value))

    def get_ffm_wu(self) -> float:
        """
        Calcula FFM (Free Fat Mass) según Wu et al. (2015) validado contra DEXA:
        FFM = 13.055 + 0.204*W + 0.394*(H^2/R) - 0.136*A + 8.125*Sexo
        Sexo: male=1, female=0
        """
        sex_flag = 1 if self.sex == 'male' else 0
        ffm = (
            13.055
            + 0.204 * self.weight
            + 0.394 * ((self.height ** 2) / self.impedance)
            - 0.136 * self.age
            + 8.125 * sex_flag
        )
        # Garantizar FFM mínimo 50% del peso
        return self._check_bounds(ffm, self.weight * 0.5, self.weight)

    def get_fat_percentage(self) -> float:
        """
        % de grasa corporal derivado de FFM Wu:
        %Fat = 100 * (weight - FFM) / weight
        """
        ffm = self.get_ffm_wu()
        fat_pct = 100 * (self.weight - ffm) / self.weight
        return self._check_bounds(fat_pct, 2.0, 60.0)

    def get_muscle_mass_janssen(self) -> float:
        """
        Masa muscular esquelética según Janssen et al. (2000):
        SM = 0.401*(H^2/R) + 3.825*Sexo - 0.071*Edad + 5.102
        """
        sex_flag = 1 if self.sex == 'male' else 0
        sm = (
            0.401 * ((self.height ** 2) / self.impedance)
            + 3.825 * sex_flag
            - 0.071 * self.age
            + 5.102
        )
        return self._check_bounds(sm, 10.0, 200.0)

    def get_tbw_kushner(self) -> float:
        """
        Agua corporal total (TBW) usando ecuación linear BIA (Kushner & Schoeller):
        TBW ≈ 2.447 + 0.336*(H^2/R) + 0.1074*W  (valores para varones)
        Para mujeres podría ajustarse coeficientes.
        """
        # Usamos coeficientes de Watson aproximados
        tbw = (
            2.447
            + 0.336 * ((self.height ** 2) / self.impedance)
            + 0.1074 * self.weight
        )
        return self._check_bounds(tbw, 10.0, 80.0)

    def get_ecw_icw(self) -> tuple:
        """
        Estima ECW e ICW asumiendo proporciones típicas:
        ECW = frac_ecw * TBW, ICW = TBW - ECW
        Ajuste ligero según %grasa corporal.
        """
        tbw = self.get_tbw_kushner()
        fat_pct = self.get_fat_percentage()
        # Base fisiológica
        frac_ecw = 0.38
        if fat_pct > 25:
            frac_ecw = 0.40
        elif fat_pct < 10:
            frac_ecw = 0.36
        ecw = tbw * frac_ecw
        icw = tbw - ecw
        return ecw, icw

    def get_bmr_cunningham(self) -> float:
        """
        Tasa metabólica basal usando Cunningham (1980):
        BMR = 370 + 21.6 * FFM
        """
        ffm = self.get_ffm_wu()
        bmr = 370 + 21.6 * ffm
        return self._check_bounds(bmr, 800.0, 6000.0)

    def get_visceral_fat_liu(self) -> float:
        """
        Estima área visceral (VFA, cm²) según Liu et al. (2022):
        Hombres: 3.7*A + 2.4*Waist + 5.5*Neck - 443.6
        Mujeres: 2.8*A + 1.7*Waist + 6.5*Neck - 367.3
        Requiere Waist y Neck.
        """
        if self.waist is None or self.neck is None:
            raise ValueError("Waist y neck necesarios para estimar grasa visceral con Liu2022")
        if self.sex == 'male':
            vfa = 3.7 * self.age + 2.4 * self.waist + 5.5 * self.neck - 443.6
        else:
            vfa = 2.8 * self.age + 1.7 * self.waist + 6.5 * self.neck - 367.3
        return self._check_bounds(vfa, 0.0, 500.0)

    def get_bmi(self) -> float:
        """Calcula el índice de masa corporal"""
        height_m = self.height / 100
        return self.weight / (height_m ** 2)

    def get_bmi_category(self) -> str:
        """Categoría de BMI según OMS"""
        bmi = self.get_bmi()
        if bmi < 18.5:
            return "Bajo peso"
        elif bmi < 25:
            return "Peso normal"
        elif bmi < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"

    def save_metrics_to_file(self, filename: str = 'enhanced_body_metrics.txt'):
        """
        Guarda todas las métricas calculadas en un archivo con formato legible
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== REPORTE DE COMPOSICIÓN CORPORAL ===\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Datos básicos
                f.write("--- DATOS BÁSICOS ---\n")
                f.write(f"Peso: {self.weight:.1f} kg\n")
                f.write(f"Altura: {self.height:.0f} cm\n")
                f.write(f"Edad: {self.age} años\n")
                f.write(f"Sexo: {self.sex}\n")
                f.write(f"Impedancia: {self.impedance:.0f} ohm\n")
                
                if self.waist:
                    f.write(f"Cintura: {self.waist:.1f} cm\n")
                if self.neck:
                    f.write(f"Cuello: {self.neck:.1f} cm\n")
                if self.hip:
                    f.write(f"Cadera: {self.hip:.1f} cm\n")
                if self.thigh:
                    f.write(f"Muslo: {self.thigh:.1f} cm\n")
                
                # BMI
                f.write(f"\n--- ÍNDICE DE MASA CORPORAL ---\n")
                f.write(f"BMI: {self.get_bmi():.1f} kg/m²\n")
                f.write(f"Categoría: {self.get_bmi_category()}\n")
                
                # Composición corporal
                f.write(f"\n--- COMPOSICIÓN CORPORAL ---\n")
                f.write(f"Masa libre de grasa (FFM Wu): {self.get_ffm_wu():.1f} kg\n")
                f.write(f"Porcentaje de grasa: {self.get_fat_percentage():.1f}%\n")
                f.write(f"Masa grasa: {(self.weight * self.get_fat_percentage() / 100):.1f} kg\n")
                f.write(f"Masa muscular esquelética (Janssen): {self.get_muscle_mass_janssen():.1f} kg\n")
                
                # Agua corporal
                f.write(f"\n--- AGUA CORPORAL ---\n")
                f.write(f"Agua corporal total (TBW): {self.get_tbw_kushner():.1f} L\n")
                ecw, icw = self.get_ecw_icw()
                f.write(f"Agua extracelular (ECW): {ecw:.1f} L\n")
                f.write(f"Agua intracelular (ICW): {icw:.1f} L\n")
                f.write(f"Porcentaje de agua: {(self.get_tbw_kushner() / self.weight * 100):.1f}%\n")
                
                # Metabolismo
                f.write(f"\n--- METABOLISMO ---\n")
                f.write(f"Tasa metabólica basal (Cunningham): {self.get_bmr_cunningham():.0f} kcal/día\n")
                
                # Grasa visceral (si hay datos)
                if self.waist and self.neck:
                    f.write(f"\n--- GRASA VISCERAL ---\n")
                    f.write(f"Área de grasa visceral (Liu): {self.get_visceral_fat_liu():.1f} cm²\n")
                
                f.write(f"\n--- REFERENCIAS ---\n")
                f.write("FFM: Wu et al. (2015) - validado contra DEXA\n")
                f.write("Masa muscular: Janssen et al. (2000)\n")
                f.write("TBW: Kushner & Schoeller\n")
                f.write("BMR: Cunningham (1980)\n")
                if self.waist and self.neck:
                    f.write("Grasa visceral: Liu et al. (2022)\n")
            
            print(f"Métricas guardadas en: {filename}")
            
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def print_summary(self):
        """Imprime un resumen de las métricas principales"""
        print("\n=== RESUMEN DE COMPOSICIÓN CORPORAL ===")
        print(f"BMI: {self.get_bmi():.1f} kg/m² ({self.get_bmi_category()})")
        print(f"Grasa corporal: {self.get_fat_percentage():.1f}%")
        print(f"Masa muscular: {self.get_muscle_mass_janssen():.1f} kg")
        print(f"Agua corporal: {self.get_tbw_kushner():.1f} L ({(self.get_tbw_kushner() / self.weight * 100):.1f}%)")
        print(f"TMB: {self.get_bmr_cunningham():.0f} kcal/día")
        if self.waist and self.neck:
            print(f"Grasa visceral: {self.get_visceral_fat_liu():.1f} cm²")

# Ejemplo de uso:
if __name__ == '__main__':
    em = EnhancedBodyMetrics(
        weight=75.0,
        height=180,
        age=25,
        sex='male',
        impedance=500,
        waist=85,
        neck=40
    )
    em.print_summary()
    em.save_metrics_to_file()
