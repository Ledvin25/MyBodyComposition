from math import floor
import sys
from body_scales import bodyScales

class bodyMetrics:
    def __init__(self, weight, height, age, sex, impedance):
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex
        self.impedance = impedance
        self.scales = bodyScales(age, height, sex, weight)

        # Check for potential out of boundaries
        if self.height > 220:
            print("Height is too high (limit: >220cm) or scale is sleeping")
            sys.stderr.write('Height is over 220cm\n')
            exit()
        elif weight < 10 or weight > 200:
            print("Weight is either too low or too high (limits: <10kg and >200kg)")
            sys.stderr.write('Weight is below 10kg or above 200kg\n')
            exit()
        elif age > 99:
            print("Age is too high (limit >99 years)")
            sys.stderr.write('Age is above 99 years\n')
            exit()
        elif impedance > 3000:
            print("Impedance is above 3000 Ohm")
            sys.stderr.write('Impedance is above 3000 Ohm\n')
            exit()

    # Set the value to a boundary if it overflows
    def checkValueOverflow(self, value, minimum, maximum):
        if value < minimum:
            return minimum
        elif value > maximum:
            return maximum
        else:
            return value

    # Get LBM coefficient (with impedance)
    def getLBMCoefficient(self):
        if self.sex == 'female':
            lbm = (0.252 * self.weight) + (0.473 * self.height) - (0.48 * self.impedance/100) + 10.05
        else:  # male
            lbm = (0.407 * self.weight) + (0.267 * self.height) - (0.47 * self.impedance/100) + 19.2
        
        # Ajuste basado en la edad
        lbm -= (self.age - 20) * 0.1  # Reduce LBM ligeramente a medida que aumenta la edad
        
        return max(lbm, self.weight * 0.5)  # Aseguramos que LBM no sea menor que el 50% del peso

    # Get BMR
    def getBMR(self):
        if self.sex == 'female':
            bmr = 864.6 + self.weight * 10.2036
            bmr -= self.height * 0.39336
            bmr -= self.age * 6.204
        else:
            bmr = 877.8 + self.weight * 14.916
            bmr -= self.height * 0.726
            bmr -= self.age * 8.976

        # Capping
        if self.sex == 'female' and bmr > 2996:
            bmr = 5000
        elif self.sex == 'male' and bmr > 2322:
            bmr = 5000
        return self.checkValueOverflow(bmr, 500, 10000)

    # Get fat percentage
    def getFatPercentage(self):
        bmi = self.getBMI()
        age = self.age
        
        if self.sex == 'male':
            fat_percentage = (1.20 * bmi) + (0.23 * age) - 16.2
            fat_percentage *= 0.80  
        else:  # female
            fat_percentage = (1.20 * bmi) + (0.23 * age) - 5.4

        # Ajuste basado en la impedancia
        impedance_factor = (self.impedance - 400) / 50  
        fat_percentage += impedance_factor * 0.22

        return self.checkValueOverflow(fat_percentage, 5, 75)
    # Get water percentage
    def getWaterPercentage(self):
        # Factores base según sexo
        if self.sex == 'male':
            base_water = 62.5  
        else:
            base_water = 57

        # Ajuste por edad
        if self.age < 30:
            age_factor = 1.01  
        elif 30 <= self.age < 55:
            age_factor = 1
        else:
            age_factor = 0.98

        # Ajuste por IMC
        bmi = self.getBMI()
        if bmi < 18.5:
            bmi_factor = 1.05
        elif 18.5 <= bmi < 25:
            bmi_factor = 1.01  # Reducimos ligeramente
        elif 25 <= bmi < 30:
            bmi_factor = 1
        else:
            bmi_factor = 0.98

        # Ajuste por porcentaje de grasa
        fat_percentage = self.getFatPercentage()
        water_percentage = base_water * age_factor * bmi_factor

        # Inversa relación con el porcentaje de grasa
        water_percentage -= (fat_percentage - 15) * 0.27  # Ajustamos ligeramente

        # Ajuste fino basado en impedancia
        impedance_factor = (self.impedance - 400) / 100  # Normalizado alrededor de 400 ohm
        water_percentage += impedance_factor * 0.25  # Reducimos ligeramente el impacto

        return self.checkValueOverflow(water_percentage, 35, 75)

    # Get bone mass
    def getBoneMass(self):
        if self.sex == 'female':
            base = 0.245691014
        else:
            base = 0.18016894

        boneMass = (base - (self.getLBMCoefficient() * 0.05158)) * -1

        if boneMass > 2.2:
            boneMass += 0.1
        else:
            boneMass -= 0.1

        # Capping boneMass
        if self.sex == 'female' and boneMass > 5.1:
            boneMass = 8
        elif self.sex == 'male' and boneMass > 5.2:
            boneMass = 8
        return self.checkValueOverflow(boneMass, 0.5 , 8)

    # Get muscle mass
    def getMuscleMass(self):
        # Factor base según sexo
        if self.sex == 'male':
            base_factor = 0.375  # Reducido ligeramente
        else:
            base_factor = 0.23

        # Cálculo basado en la fórmula de masa libre de grasa
        height_m = self.height / 100
        lbm = (base_factor * self.weight) + (0.24 * height_m * height_m) - (0.52 * self.impedance / 100) + 18.3

        # Ajuste por edad
        age_factor = max(1 - ((self.age - 20) * 0.002), 0.85)

        # Ajuste por actividad (asumiendo actividad moderada)
        activity_factor = 1.03

        # Cálculo final de la masa muscular
        muscle_mass = lbm * age_factor * activity_factor

        # Ajuste fino
        muscle_mass -= self.getBoneMass()
        muscle_mass *= 0.92  # Reducción del 8% para compensar otros tejidos

        # Ajuste adicional basado en el porcentaje de grasa
        fat_percentage = self.getFatPercentage()
        if fat_percentage > 20:
            muscle_mass *= 0.97
        elif fat_percentage < 10:
            muscle_mass *= 1.02

        # Ajuste final basado en el IMC
        bmi = self.getBMI()
        if bmi > 25:
            muscle_mass *= 0.98
        elif bmi < 18.5:
            muscle_mass *= 1.02

        return self.checkValueOverflow(muscle_mass, 10, 120)

    # Get Visceral Fat
    def getVisceralFat(self):
        bmi = self.getBMI()
        body_fat_percentage = self.getFatPercentage()
        
        # Base calculation
        if self.sex == 'male':
            vfal = (bmi - 15) * 0.3 + (body_fat_percentage - 10) * 0.2
        else:
            vfal = (bmi - 15) * 0.2 + (body_fat_percentage - 15) * 0.1
        
        # Age adjustment
        vfal += max(self.age - 20, 0) * 0.07
        
        # Waist-to-height ratio estimation (since we don't have waist measurement)
        waist_height_ratio = bmi * 0.011  # adjusted estimation
        vfal += (waist_height_ratio - 0.4) * 15
        
        # Activity level adjustment (assuming moderate activity)
        vfal *= 0.95
        
        # Final adjustments
        vfal = max(vfal, 1)  # Ensure it's not negative
        vfal *= 1.2  # General scaling factor to bring values up
        
        return self.checkValueOverflow(vfal, 1, 50)

    # Get BMI
    def getBMI(self):
        return self.checkValueOverflow(self.weight/((self.height/100)*(self.height/100)), 10, 90)

    # Get ideal weight (just doing a reverse BMI, should be something better)
    

    # Get fat mass to ideal (guessing mi fit formula)
    def getFatMassToIdeal(self):
        mass = (self.weight * (self.getFatPercentage() / 100)) - (self.weight * (self.scales.getFatPercentageScale()[2] / 100))
        if mass < 0:
            return {'type': 'to_gain', 'mass': mass*-1}
        else:
            return {'type': 'to_lose', 'mass': mass}

    # Get protetin percentage (warn: guessed formula)
    def getProteinPercentage(self):
        muscle_mass = self.getMuscleMass()
        body_fat_percentage = self.getFatPercentage()
        water_percentage = self.getWaterPercentage()
        
        # Base calculation from muscle mass
        protein_percentage = (muscle_mass / self.weight) * 100 * 0.185  # Aumentado ligeramente de 0.18 a 0.185
        
        # Adjustments based on other factors
        protein_percentage += (100 - body_fat_percentage - water_percentage) * 0.26  # Aumentado ligeramente de 0.25 a 0.26
        
        # Age adjustment
        age_factor = max(1 - ((self.age - 20) * 0.001), 0.95)
        protein_percentage *= age_factor
        
        # Sex-based adjustment
        if self.sex == 'male':
            protein_percentage *= 1.09  # Aumentado ligeramente de 1.08 a 1.09
        else:
            protein_percentage *= 0.98
        
        # Activity level adjustment (assuming moderate activity)
        protein_percentage *= 1.035  # Aumentado ligeramente de 1.03 a 1.035
        
        # BMI adjustment
        bmi = self.getBMI()
        if bmi > 25:
            protein_percentage *= 0.97
        elif bmi < 18.5:
            protein_percentage *= 1.01
        
        # Final scaling
        protein_percentage *= 1.06  # Aumentado ligeramente de 1.05 a 1.06
        
        return self.checkValueOverflow(protein_percentage, 5, 32)

    # Get body type (out of nine possible)
    def getBodyType(self):
        if self.getFatPercentage() > self.scales.getFatPercentageScale()[2]:
            factor = 0
        elif self.getFatPercentage() < self.scales.getFatPercentageScale()[1]:
            factor = 2
        else:
            factor = 1

        if self.getMuscleMass() > self.scales.getMuscleMassScale()[1]:
            return 2 + (factor * 3)
        elif self.getMuscleMass() < self.scales.getMuscleMassScale()[0]:
            return (factor * 3)
        else:
            return 1 + (factor * 3)

    # Get Metabolic Age
    def getMetabolicAge(self):
        if self.sex == 'female':
            metabolicAge = (self.height * -1.1165) + (self.weight * 1.5784) + (self.age * 0.4615) + (self.impedance * 0.0415) + 83.2548
        else:
            metabolicAge = (self.height * -0.7471) + (self.weight * 0.9161) + (self.age * 0.4184) + (self.impedance * 0.0517) + 54.2267
        return self.checkValueOverflow(metabolicAge, 15, 80)

    def saveMetricsToFile(self, filename):
        metrics = {
            "LBM Coefficient": self.getLBMCoefficient(),
            "BMR": self.getBMR(),
            "Fat Percentage": self.getFatPercentage(),
            "Water Percentage": self.getWaterPercentage(),
            "Bone Mass": self.getBoneMass(),
            "Muscle Mass": self.getMuscleMass(),
            "Visceral Fat": self.getVisceralFat(),
            "BMI": self.getBMI(),
            "Protein Percentage": self.getProteinPercentage(),
        }

        with open(filename, 'w') as file:
            for key, value in metrics.items():
                file.write(f"{key}: {value}\n")

# Ejemplo de uso:
# Crear un objeto de bodyMetrics
bm = bodyMetrics(weight=74.9, height=168, age=19, sex='male', impedance=411)
# Guardar los datos en un archivo .txt
bm.saveMetricsToFile('body_metrics.txt')
