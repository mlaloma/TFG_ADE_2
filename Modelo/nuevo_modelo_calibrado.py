import numpy as np
import matplotlib.pyplot as plt

# Parámetros base
L = 50
penalty_time = 10
p_audit = 0.05  # fijo para control de variables
steps_per_year = 5
years = list(range(2005, 2024))
target_evasion = np.array([7.4, 6.6, 6.1, 6.8, 6.4, 6.2, 6.0, 6.5, 6.9,
                           6.0, 5.8, 5.4, 5.0, 5.0, 5.5, 5.0, 5.2, 5.2, 4.8]) / 100

# Inicializar red
spins = np.ones((L, L), dtype=int)
penalty_counters = np.zeros((L, L), dtype=int)

def delta_energy(spins, i, j):
    L = spins.shape[0]
    s = spins[i, j]
    neighbors = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
    dE = 2 * J * s * neighbors
    return dE

def metropolis_step(spins, penalty_counters, T, p_audit):
    L = spins.shape[0]
    for _ in range(L * L):
        i = np.random.randint(0, L)
        j = np.random.randint(0, L)
        if penalty_counters[i, j] > 0:
            penalty_counters[i, j] -= 1
            spins[i, j] = 1
            continue
        dE = delta_energy(spins, i, j)
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            spins[i, j] *= -1
        if spins[i, j] == -1 and np.random.rand() < p_audit:
            penalty_counters[i, j] = penalty_time
            spins[i, j] = 1
    return spins, penalty_counters

# Calibración automática
J = 1
calibrated_T = []
simulated_evasion = []

for year_idx, ev_target in enumerate(target_evasion):
    best_diff = float('inf')
    best_T = None

    for T_try in np.linspace(0.5, 5.0, 50):
        # Clonar el estado anterior para pruebas (no modificar real)
        test_spins = np.copy(spins)
        test_penalties = np.copy(penalty_counters)

        for _ in range(steps_per_year):
            test_spins, test_penalties = metropolis_step(test_spins, test_penalties, T_try, p_audit)
        ev_rate = np.sum(test_spins == -1) / (L * L)
        diff = abs(ev_rate - ev_target)
        if diff < best_diff:
            best_diff = diff
            best_T = T_try

    # Aplicamos mejor temperatura al sistema real
    calibrated_T.append(best_T)
    for _ in range(steps_per_year):
        spins, penalty_counters = metropolis_step(spins, penalty_counters, best_T, p_audit)
    ev_real = np.sum(spins == -1) / (L * L)
    simulated_evasion.append(ev_real)

# Graficar resultados
plt.figure(figsize=(10,5))
plt.plot(years, np.array(simulated_evasion)*100, marker='o', label='Simulado (calibrado)')
plt.plot(years, target_evasion*100, linestyle='--', marker='x', label='Real HMRC')
plt.title("Tasa de evasión calibrada año por año")
plt.xlabel("Año")
plt.ylabel("Tasa de evasión (%)")
plt.legend()
plt.grid(True)
plt.show()
