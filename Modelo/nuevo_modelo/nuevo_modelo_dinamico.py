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

# Simulación dinámica
years = 20
T = 2.5  # inicial
p_audit = 0.05  # inicial
evasion_rate_history = []

for year in range(years):
    # Simular 5 pasos de Monte Carlo por año
    for _ in range(5):
        spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)

    evasion = np.sum(spins == -1) / (L * L)
    evasion_rate_history.append(evasion)

    # 🔁 CAMBIOS DINÁMICOS (editables)
    if year == 5:
        p_audit += 0.02  # Aumento de auditorías
    if year == 10:
        T -= 0.5  # Mejora de moral social (menor temperatura)
    if year == 15:
        p_audit -= 0.01  # Relajación de auditorías

# Graficar resultados
plt.plot(range(years), np.array(evasion_rate_history) * 100, marker='o')
plt.title("Tasa de evasión fiscal con dinámica de políticas")
plt.xlabel("Año")
plt.ylabel("Tasa de evasión (%)")
plt.grid(True)
plt.show()
