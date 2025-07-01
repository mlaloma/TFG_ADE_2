import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
L = 50  # Tamaño de la red LxL
steps = 100  # Número de pasos de tiempo (Monte Carlo sweeps)
J = 1.0  # Constante de acoplamiento
T = 100  # Temperatura (presión social)
p_audit = 0  # Probabilidad de auditoría
penalty_time = 10  # Tiempo que un agente debe cumplir si es auditado

# Inicialización de la red de agentes
spins = np.ones((L, L), dtype=int)  # Todos cumplidores al inicio
penalty_counters = np.zeros((L, L), dtype=int)

# Función para calcular la energía local (vecinos en red cuadrada 2D con condiciones periódicas)
def delta_energy(spins, i, j):
    L = spins.shape[0]
    s = spins[i, j]
    neighbors = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
    dE = 2 * J * s * neighbors
    return dE

# Paso de Monte Carlo usando el algoritmo de Metropolis
def metropolis_step(spins, penalty_counters, T, p_audit):
    L = spins.shape[0]
    for _ in range(L * L):  # LxL intentos por paso
        i = np.random.randint(0, L)
        j = np.random.randint(0, L)

        if penalty_counters[i, j] > 0:
            penalty_counters[i, j] -= 1
            spins[i, j] = 1  # cumplimiento forzado
            continue

        dE = delta_energy(spins, i, j)
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            spins[i, j] *= -1  # cambiar estado

        # Auditoría aleatoria
        if spins[i, j] == -1 and np.random.rand() < p_audit:
            penalty_counters[i, j] = penalty_time
            spins[i, j] = 1  # obligado a cumplir
    return spins, penalty_counters

# Simulación
history = []

for step in range(steps):
    spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)
    tax_evasion_rate = np.sum(spins == -1) / (L * L)
    history.append(tax_evasion_rate)

# Visualización
plt.figure(figsize=(10, 5))
plt.plot(history, label=f'T={T}, p_audit={p_audit}')
plt.title("Evasión Fiscal usando el algoritmo de Metropolis")
plt.xlabel("Paso de Monte Carlo")
plt.ylabel("Tasa de evasión")
plt.grid(True)
plt.legend()
plt.show()
