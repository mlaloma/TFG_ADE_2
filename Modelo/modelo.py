import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Parámetros de simulación
N = 50          # Tamaño de la cuadrícula
T = 2.5         # Temperatura inicial
beta = 1.0 / T
running = True  # Control de ejecución

# Inicializar la cuadrícula de espines aleatoriamente
def inicializar_lattice(N):
    return np.random.choice([-1, 1], size=(N, N))

lattice = inicializar_lattice(N) # Inicializar la cuadrícula

# Cálculo de la variación de energía al cambiar un espín
def energia_intercambio(lattice, i, j):
    N = lattice.shape[0]
    S = lattice[i, j]
    vecinos = (
        lattice[(i+1)%N, j] + lattice[(i-1)%N, j] + 
        lattice[i, (j+1)%N] + lattice[i, (j-1)%N]
    )
    return 2 * S * vecinos

# Algoritmo de Metropolis
def metropolis(lattice, beta):
    N = lattice.shape[0]
    for _ in range(N*N):  # Un "paso de Monte Carlo"
        i, j = random.randint(0, N-1), random.randint(0, N-1)
        dE = energia_intercambio(lattice, i, j)
        if dE < 0 or random.random() < np.exp(-dE * beta):
            lattice[i, j] *= -1

# Configurar la figura
plt.ion()  # Modo interactivo
fig, ax = plt.subplots()
im = ax.imshow(lattice, cmap='gray')
ax.set_title(f"Modelo de Ising 2D (T={T:.2f})")

# Función para manejar el teclado
def on_key(event):
    global running, beta, T

    if event.key == " ":  # Pausar/Reanudar con el espacio
        running = not running
        print("Pausado" if not running else "Reanudado")

    elif event.key == "up":  # Aumentar temperatura
        T = min(T + 0.1, 5.0)
        beta = 1.0 / T
        ax.set_title(f"Modelo de Ising 2D (T={T:.2f})")

    elif event.key == "down":  # Disminuir temperatura
        T = max(T - 0.1, 0.1)
        beta = 1.0 / T
        ax.set_title(f"Modelo de Ising 2D (T={T:.2f})")

fig.canvas.mpl_connect('key_press_event', on_key)

# Bucle de simulación
while True:
    if running:
        metropolis(lattice, beta)  # Aplicar el algoritmo de Metropolis
        im.set_array(lattice)  # Actualizar la imagen
        plt.draw()
    
    plt.pause(0.01)  # Pausa para permitir interacción
    time.sleep(0.1)  # Delay entre saltos