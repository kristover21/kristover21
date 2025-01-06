import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


restaurant_name = "Restoran Cristover"


speed = ctrl.Antecedent(np.arange(0, 11, 1), 'speed')  
food_quality = ctrl.Antecedent(np.arange(0, 11, 1), 'food_quality')  
ambience = ctrl.Antecedent(np.arange(0, 11, 1), 'ambience')  
happiness = ctrl.Consequent(np.arange(0, 11, 1), 'happiness')  


speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 5])
speed['medium'] = fuzz.trimf(speed.universe, [0, 5, 10])
speed['fast'] = fuzz.trimf(speed.universe, [5, 10, 10])

ambience['poor'] = fuzz.trimf(ambience.universe, [0, 0, 5])
ambience['decent'] = fuzz.trimf(ambience.universe, [0, 5, 10])
ambience['excellent'] = fuzz.trimf(ambience.universe, [5, 10, 10])


food_quality['bad'] = fuzz.gaussmf(food_quality.universe, 0, 2)  
food_quality['average'] = fuzz.gaussmf(food_quality.universe, 5, 2)  
food_quality['good'] = fuzz.gaussmf(food_quality.universe, 10, 2)  


happiness['unhappy'] = fuzz.trimf(happiness.universe, [0, 0, 5])
happiness['neutral'] = fuzz.trimf(happiness.universe, [0, 5, 10])
happiness['happy'] = fuzz.trimf(happiness.universe, [5, 10, 10])


rule1 = ctrl.Rule(speed['slow'] & food_quality['bad'] & ambience['poor'], happiness['unhappy'])
rule2 = ctrl.Rule(speed['medium'] & food_quality['average'] & ambience['decent'], happiness['neutral'])
rule3 = ctrl.Rule(speed['fast'] & food_quality['good'] & ambience['excellent'], happiness['happy'])


happiness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
happiness_simulation = ctrl.ControlSystemSimulation(happiness_ctrl)



def get_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 10:
                return value
            else:
                print("Masukkan angka antara 0-10.")
        except ValueError:
            print("Masukkan angka yang valid.")

# Input Nilai dari Pengguna
print(f"Selamat datang di {restaurant_name}!")
print("Masukkan Nilai Input (0-10):")
speed_value = get_input("Kecepatan Pelayanan: ")
food_quality_value = get_input("Kualitas Makanan: ")
ambience_value = get_input("Suasana Restoran: ")

# Berikan Input ke Sistem Fuzzy
happiness_simulation.input['speed'] = speed_value
happiness_simulation.input['food_quality'] = food_quality_value
happiness_simulation.input['ambience'] = ambience_value

# Hitung Hasil Fuzzy
happiness_simulation.compute()

# Tampilkan Output
output_happiness = happiness_simulation.output['happiness']
if output_happiness <= 3:
    happiness_level = "Unhappy"
elif output_happiness <= 7:
    happiness_level = "Neutral"
else:
    happiness_level = "Happy"

print(f"\nTingkat Kebahagiaan Pelanggan di {restaurant_name}: {output_happiness:.2f} (0-10)")
print(f"Kategori: {happiness_level}")

# ------------------------------------------
# Visualisasi Hasil Keanggotaan
# ------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

speed.view(ax=axs[0, 0])
axs[0, 0].set_title("Fungsi Keanggotaan: Speed")

food_quality.view(ax=axs[0, 1])
axs[0, 1].set_title("Fungsi Keanggotaan: Food Quality")

ambience.view(ax=axs[1, 0])
axs[1, 0].set_title("Fungsi Keanggotaan: Ambience")

happiness.view(sim=happiness_simulation, ax=axs[1, 1])
axs[1, 1].set_title("Hasil Keanggotaan: Happiness")

plt.tight_layout()
plt.show()
