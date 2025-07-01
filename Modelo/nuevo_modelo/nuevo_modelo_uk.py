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

# Datos reales del tax gap UK (%)
uk_tax_gap_real = [
    7.4, 6.6, 6.1, 6.8, 6.4, 6.2, 6.0, 6.5, 6.9,
    6.0, 5.8, 5.4, 5.0, 5.0, 5.5, 5.0, 5.2, 4.8
]

# Simulación
years = len(uk_tax_gap_real)
evasion_rate_history = []

# Condiciones iniciales (clima fiscal débil y baja fiscalización)
T = 2.34
p_audit = 0.035

pre_years = 10
for _ in range(pre_years * 5):  # 5 pasos Monte Carlo por año
    spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)

for year in range(years):
    # Simular 5 pasos de Monte Carlo por año
    for _ in range(5):
        spins, penalty_counters = metropolis_step(spins, penalty_counters, T, p_audit)

    evasion = np.sum(spins == -1) / (L * L)
    evasion_rate_history.append(evasion * 100)

    # Eventos de mejora progresiva
    if year in [2, 5, 8]:  # 2007-08, 2010-11, 2013-14
        T -= 0.05  # Mejora social: educación fiscal, OCDE-G20 cooperación
    if year in [4, 7, 10]:  # 2009-10, 2012-13, 2015-16
        p_audit += 0.005  # Mejora tecnológica y foco sectorial
    if year == 12:  # 2017-18
        T -= 0.05  # Refuerzo de sanciones y transparencia
        p_audit += 0.01
    if year == 15:  # 2020-21
        T -= 0.05  # Pandemia, pero no tan marcado como en el VAT Gap

# Gráfico comparativo
plt.plot(range(2005, 2005 + years), evasion_rate_history, marker='o', label='Simulación')
plt.plot(range(2005, 2005 + years), uk_tax_gap_real, marker='s', linestyle='--', label='Tax Gap Real UK')
plt.title("Simulación del Tax Gap del Reino Unido (2005–2023)")
plt.xlabel("Año fiscal")
plt.ylabel("Tax Gap (%)")
plt.grid(True)
plt.legend()

xticks = list(range(2005, 2005 + years + 1, 2))
plt.xticks(xticks)

plt.show()
