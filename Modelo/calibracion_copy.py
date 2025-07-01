import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")

# ========================
# FUNCIONES DEL MODELO
# ========================

def inicializar_lattice(N):
    return np.random.choice([-1, 1], size=(N, N), p=[0.2, 0.8])  # 80% cumplimiento

def energia_intercambio(lattice, i, j, J):
    N = lattice.shape[0]
    S = lattice[i, j]
    vecinos = (
        lattice[(i+1)%N, j] + lattice[(i-1)%N, j] +
        lattice[i, (j+1)%N] + lattice[i, (j-1)%N]
    )
    dE = -J * S * vecinos
    return dE

def metropolis(lattice, beta, J, p_a):
    N = lattice.shape[0]
    for _ in range(N*N):
        i, j = random.randint(0, N-1), random.randint(0, N-1)
        dE = energia_intercambio(lattice, i, j, J)
        if dE < 0 or random.random() < np.exp(-dE * beta):
            lattice[i, j] *= -1
        if lattice[i, j] == -1 and random.random() < p_a:
            lattice[i, j] = 1

# ========================
# PARÁMETROS GENERALES
# ========================
N = 50
J = 1.0

# Datos reales de evasión (% de evasión como proporción)
datos_reales = [
    0.074, 0.066, 0.061, 0.068, 0.064, 0.062, 0.060, 0.065, 0.069,
    0.060, 0.058, 0.054, 0.050, 0.050, 0.055, 0.050, 0.052, 0.048
]

# ========================
# SIMULACIÓN Y CALIBRACIÓN
# ========================

def simular_modelo(T, p_a, pasos=200):
    beta = 1.0 / T
    lattice = inicializar_lattice(N)
    evasiones = []
    for _ in range(pasos):
        metropolis(lattice, beta, J, p_a)
        porcentaje_evasion = np.count_nonzero(lattice == -1) / (N * N)
        evasiones.append(porcentaje_evasion)
    bloques = np.array_split(evasiones, len(datos_reales))
    promedio = [np.mean(bloque) for bloque in bloques]
    return promedio

def error(params):
    T, p_a = params
    sim = simular_modelo(T, p_a)
    sim = np.array(sim)
    reales = np.array(datos_reales)
    sim_norm = sim / np.max(sim)
    reales_norm = reales / np.max(reales)
    return np.mean((sim_norm - reales_norm)**2)


# ========================
# OPTIMIZACIÓN
# ========================
print("\n🔍 Iniciando calibración automática...")

resultado = minimize(error, x0=[2.5, 0.05], bounds=[(0.1, 10.0), (0.0, 1.0)])
T_opt, p_a_opt = resultado.x

print(f"\n📊 Parámetros óptimos:")
print(f"Temperatura social (T): {T_opt:.3f}")
print(f"Probabilidad de auditoría (p_a): {p_a_opt:.3f}")

# ========================
# COMPARACIÓN DE RESULTADOS
# ========================
evasiones_simuladas = simular_modelo(T_opt, p_a_opt)

plt.figure(figsize=(10, 5))
plt.plot(datos_reales, label="Datos reales (UK)", marker='o')
plt.plot(evasiones_simuladas, label="Simulación calibrada", marker='x')
plt.title("Comparación de evasión fiscal: Simulación vs Reino Unido")
plt.xlabel("Años simulados (equivalente)")
plt.ylabel("% Evasión fiscal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
