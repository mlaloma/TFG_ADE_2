import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Código para dibujar las flechas de los spines en 2D
M, N = 5, 5

# Generamos aleatoriamente los spins, -1 para abajo y 1 para arriba
spins = np.random.choice([-1, 1], size=(M, N))

# Configuración de la gráfica
fig, ax = plt.subplots(figsize=(8, 8))

# Dibuja las flechas
for i in range(M):
    for j in range(N):
        if spins[i, j] == 1:
            ax.add_patch(FancyArrowPatch((j, M-i-1), (j, M-i), mutation_scale=15, color='blue'))
        else:
            ax.add_patch(FancyArrowPatch((j, M-i), (j, M-i-1), mutation_scale=15, color='red'))

# Ajustes de visualización
ax.set_xlim(-0.5, N-0.5)
ax.set_ylim(-0.5, M)  # Se cambió el límite superior del eje y a M (para evitar corte)
ax.set_xticks(np.arange(N))  # Añadir ejes con medidas
ax.set_xticklabels(np.arange(N))  # Etiquetas de los ejes x (posiciones de los spins)
ax.set_yticks(np.arange(M))
ax.set_yticklabels(np.arange(M))  # Etiquetas de los ejes y (posiciones de los spins)
ax.spines['top'].set_visible(False) # Eliminar recuadro (sin bordes adicionales)
ax.spines['right'].set_visible(False)
ax.set_aspect('equal') # Aspecto de la gráfica
ax.grid(False)  # Eliminar la cuadrícula
ax.set_title("Modelo de Ising en 2D\n")

plt.show()
