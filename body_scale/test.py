def calculate_composition(weight, height, impedance, age, sex):
    # Convert height to meters for BMI calculation
    height_m = height / 100

    # Calculate LBM using a formula that includes impedance
    lbm = (0.32810 * weight + 0.33929 * height - 29.5336) - (impedance * 0.0068)

    # Calculate Fat Percentage
    fat_percentage = 100 * (1 - (lbm / weight))

    # Calculate Water Percentage
    water_percentage = 0.7 * (1 - fat_percentage / 100)

    # Calculate Muscle Mass
    muscle_mass = weight - (weight * fat_percentage / 100)

    # Calculate Fat Mass
    fat_mass = weight * fat_percentage / 100

    return {
        'Fat Percentage': fat_percentage,
        'Water Percentage': water_percentage,
        'Muscle Mass': muscle_mass,
        'Fat Mass': fat_mass
    }

# Input values
weight = 75.9
height = 169
impedance = 441
age = 19
sex = 'male'

# Calculate composition
composition = calculate_composition(weight, height, impedance, age, sex)
print(composition)