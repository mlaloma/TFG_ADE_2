import numpy as np
import matplotlib.pyplot as plt

# Parámetros fijos
L = 50
steps = 100
J = 1.0
penalty_time = 10

# Rango de parámetros a explorar
T_values = np.linspace(1.0, 6.0, 10)
p_audit_values = np.linspace(0.0, 1.0, 10)

# Funciones auxiliares (mismas que en tu código original)
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

# Simulación en el espacio de parámetros
heatmap = np.zeros((len(p_audit_values), len(T_values)))

for i, p_audit in enumerate(p_audit_values):
    for j, T in enumerate(T_values):
        spins = np.ones((L, L), dtype=int)
        penalty_counters = np.zeros((L, L), dtype=int)
        evasion_history = []
        for _ in range(steps):
            spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)
            evasion_rate = np.sum(spins == -1) / (L * L)
            evasion_history.append(evasion_rate)
        heatmap[i, j] = np.mean(evasion_history)

# Visualización del mapa de calor
plt.figure(figsize=(10, 8))
plt.imshow(heatmap, origin='lower', cmap='viridis', aspect='auto',
           extent=[T_values[0], T_values[-1], p_audit_values[0], p_audit_values[-1]])
plt.colorbar(label='Tasa promedio de evasión')
plt.xlabel('Temperatura (T)')
plt.ylabel('Probabilidad de auditoría (p_audit)')
plt.title('Mapa de calor: Evasión fiscal promedio según T y p_audit')
plt.grid(False)
plt.show()
