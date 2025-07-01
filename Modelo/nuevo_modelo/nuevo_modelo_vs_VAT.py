import numpy as np
import matplotlib.pyplot as plt

# Inicialización
L = 50
spins = np.ones((L, L), dtype=int)
penalty_counters = np.zeros((L, L), dtype=int)
penalty_time = 10

def delta_energy(spins, i, j):
    s = spins[i, j]
    neighbors = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
    return 2 * s * neighbors

def metropolis_step(spins, penalty_counters, T, p_audit):
    for _ in range(L * L):
        i, j = np.random.randint(0, L), np.random.randint(0, L)
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

# Datos reales de VAT Gap España para comparación
vat_gap_real = [6.5, 7.9, 6.1, 4.1, 4.6, 7.1]

# Simulación basada en eventos reales
years = len(vat_gap_real)
evasion_rate_history = []

# Inicializar condiciones sociales y fiscales
T = 2.3
p_audit = 0.05

for year in range(years):
    # Simular 5 pasos de Monte Carlo por año
    for _ in range(5):
        spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)

    evasion = np.sum(spins == -1) / (L * L)
    evasion_rate_history.append(evasion * 100)

    # Cambios basados en contexto histórico
    if year == 2:  # 2020
        T -= 0.3  # Pandemia: menos oportunidades de evasión
    if year == 3:  # 2021
        #T -= 0.2  # Campañas y digitalización (SII)
        p_audit += 0.02
    if year == 4:  # 2023
        T += 0.3  # Recuperación económica

# Graficar simulación vs datos reales
plt.plot(range(2018, 2018 + years), evasion_rate_history, marker='o', label='Simulación')
plt.plot(range(2018, 2018 + years), vat_gap_real, marker='s', linestyle='--', label='VAT Gap Real')
plt.title("Simulación del VAT Gap en España (2018–2023)")
plt.xlabel("Año")
plt.ylabel("VAT Gap (%)")
plt.grid(True)
plt.legend()
plt.show()
