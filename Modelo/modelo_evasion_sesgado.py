import numpy as np
import matplotlib.pyplot as plt
import random
import time
import csv
from datetime import datetime

h = -0.5  # Campo externo que favorece evasión fiscal (-1)

# Crear nombre de archivo con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"registro_evasion_{timestamp}.csv"

# Crear archivo y escribir encabezados
with open(log_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Paso", "Temperatura", "Prob_auditoria", "%Evasion"])

# Inicializar la cuadrícula de espines aleatoriamente
def inicializar_lattice(N):
    return np.random.choice([-1, 1], size=(N, N))  # -1: evasión fiscal, 1: cumplimiento fiscal

# Cálculo de la variación de energía al cambiar un espín
def energia_intercambio(lattice, i, j, J, h):
    N = lattice.shape[0]
    S = lattice[i, j]
    vecinos = (
        lattice[(i+1)%N, j] + lattice[(i-1)%N, j] + 
        lattice[i, (j+1)%N] + lattice[i, (j-1)%N]
    )
    dE = -J * S * vecinos + h * S  # Campo externo h favorece evasión si es negativo
    return dE

# Algoritmo de Metropolis con probabilidad de auditoría
def metropolis(lattice, beta, J, p_a):
    N = lattice.shape[0]
    for _ in range(N*N):  # Un "paso de Monte Carlo"
        i, j = random.randint(0, N-1), random.randint(0, N-1)
        dE = energia_intercambio(lattice, i, j, J, h)
        if dE < 0 or random.random() < np.exp(-dE * beta):
            lattice[i, j] *= -1
        
        # Simulación de auditoría: Si el espín es de evasión fiscal, existe una probabilidad de ser detectado y revertir a cumplimiento
        if lattice[i, j] == -1 and random.random() < p_a:
            lattice[i, j] = 1  # Cambio a cumplimiento debido a la auditoría

# Parámetros de simulación
N = 50      # Tamaño de la cuadrícula
T = 2.5     # Temperatura social inicial
beta = 1.0 / T  # Inverso de la temperatura social
J = 1.0     # Intensidad de la interacción entre contribuyentes
p_a = 0.05  # Probabilidad de auditoría (pequeña en este caso)
running = True  # Control de ejecución
open_ = True

lattice = inicializar_lattice(N) # Inicializar la cuadrícula

# Configurar la figura
plt.ion()  # Modo interactivo
fig, ax = plt.subplots()
im = ax.imshow(lattice, cmap='gray')
ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

# Función para manejar el teclado
def on_key(event):
    global running, beta, T, J, p_a

    if event.key == " ":  # Pausar/Reanudar con la barra espaciadora
        running = not running
        print("Pausado" if not running else "Reanudado")

    elif event.key == "up":  # Aumentar temperatura
        T = min(T + 0.5, 100.0)
        beta = 1.0 / T
        ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

    elif event.key == "down":  # Disminuir temperatura
        T = max(T - 0.5, 0.01)
        beta = 1.0 / T
        ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

    elif event.key == "right":  # Aumentar probabilidad de auditoría
        p_a = min(p_a + 0.05, 1.0)  # Aumentar hasta un máximo de 1
        ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

    elif event.key == "left":  # Disminuir probabilidad de auditoría
        p_a = max(p_a - 0.05, 0.0)  # Disminuir hasta un mínimo de 0
        ax.set_title(f"Modelo de Evasión Fiscal 2D\nTemperatura social: {T:.2f}\nProbabilidad de auditoría: {p_a:.2f}")

# Evento para detectar el cierre de la ventana y detener el bucle
def on_close(event):
    global open_
    open_ = False
    plt.close()

fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('close_event', on_close)

paso = 0
# Bucle de simulación
while open_:
    if running:
        metropolis(lattice, beta, J, p_a)  # Aplicar el algoritmo de Metropolis con auditoría
        im.set_array(lattice)  # Actualizar la imagen

        # Calcular % de evasores
        porcentaje_evasion = np.count_nonzero(lattice == -1) / (N * N) #* 100
        # Guardar en archivo CSV
        with open(log_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([paso, T, p_a, porcentaje_evasion])
        paso += 1

        plt.draw()
    
    plt.pause(0.01)  # Pausa para permitir interacción
    time.sleep(0.1)  # Retraso de 0.1 segundos entre cada paso
