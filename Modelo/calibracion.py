import numpy as np
import matplotlib.pyplot as plt
import random
import time
import csv
from datetime import datetime
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")

# ========================
# CONFIGURACIÓN INICIAL
# ========================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"registro_evasion_{timestamp}.csv"

with open(log_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Paso", "Temperatura", "Prob_auditoria", "%Evasion"])

def inicializar_lattice(N):
    return np.random.choice([-1, 1], size=(N, N))

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
# PARÁMETROS DE SIMULACIÓN
# ========================
N = 50
T = 2.5
beta = 1.0 / T
J = 1.0
p_a = 0.05
running = True
open_ = True

lattice = inicializar_lattice(N)

plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(lattice, cmap='gray')
ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

def on_key(event):
    global running, beta, T, J, p_a
    if event.key == " ":
        running = not running
    elif event.key == "up":
        T = min(T + 0.1, 5.0)
        beta = 1.0 / T
    elif event.key == "down":
        T = max(T - 0.1, 0.1)
        beta = 1.0 / T
    elif event.key == "right":
        p_a = min(p_a + 0.01, 1.0)
    elif event.key == "left":
        p_a = max(p_a - 0.01, 0.0)
    ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

def on_close(event):
    global open_
    open_ = False
    plt.close()

fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('close_event', on_close)

paso = 0
while open_:
    if running:
        metropolis(lattice, beta, J, p_a)
        im.set_array(lattice)
        porcentaje_evasion = np.count_nonzero(lattice == -1) / (N * N)
        with open(log_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([paso, T, p_a, porcentaje_evasion])
        paso += 1
        plt.draw()
    plt.pause(0.01)
    time.sleep(0.1)

# ========================
# CALIBRACIÓN AUTOMÁTICA
# ========================

print("\n🔍 Iniciando calibración automática...")

# Datos reales de evasión (% de evasión como proporción)
datos_reales = [
    0.074, 0.066, 0.061, 0.068, 0.064, 0.062, 0.060, 0.065, 0.069,
    0.060, 0.058, 0.054, 0.050, 0.050, 0.055, 0.050, 0.052, 0.048
]

def simular_modelo(T, p_a, pasos=1000):
    beta = 1.0 / T
    lattice = inicializar_lattice(N)
    evasiones = []
    for paso in range(pasos):
        metropolis(lattice, beta, J, p_a)
        porcentaje_evasion = np.count_nonzero(lattice == -1) / (N * N)
        evasiones.append(porcentaje_evasion)
    bloques = np.array_split(evasiones, len(datos_reales))
    promedio = [np.mean(bloque) for bloque in bloques]
    return promedio

def error(params):
    T, p_a = params
    if T <= 0 or not (0 <= p_a <= 1):
        return np.inf
    sim = simular_modelo(T, p_a)
    return np.mean((np.array(sim) - np.array(datos_reales))**2)

resultado = minimize(error, x0=[2.5, 0.05], bounds=[(0.1, 5.0), (0.0, 1.0)], method='L-BFGS-B')
T_opt, p_a_opt = resultado.x

print(f"\n📊 Parámetros óptimos:")
print(f"Temperatura social (T): {T_opt:.3f}")
print(f"Probabilidad de auditoría (p_a): {p_a_opt:.3f}")

evasiones_simuladas = simular_modelo(T_opt, p_a_opt)

# Graficar comparación
plt.ioff()
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
