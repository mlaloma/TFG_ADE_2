import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Código para dibujar las flechas de los spines en 1D
N = 10

# Generamos aleatoriamente los spins, -1 para abajo y 1 para arriba
spins = np.random.choice([-1, 1], size=N)

# Coordenadas de las flechas -> centradas en y = 0.5
y_pos = np.ones(N) * 0.5  

# Configuración de la gráfica
fig, ax = plt.subplots(figsize=(8, 2))

# Dibujo de las flechas
for i in range(N):
    if spins[i] == 1:
        ax.add_patch(FancyArrowPatch((i, 0), (i, 1), mutation_scale=15, color='blue'))
    else:
        ax.add_patch(FancyArrowPatch((i, 1), (i, 0), mutation_scale=15, color='red'))


# Ajustes de visualización
ax.set_xlim(-0.5, N - 0.5)
ax.set_ylim(-0.5, 1.5)  # Elimina la distancia vertical entre 0 y -1
ax.set_xticks(np.arange(N))  # Añadir ejes con medidas
ax.set_xticklabels(np.arange(N))  # Etiquetas de los ejes x (posiciones de los spins)
ax.get_yaxis().set_visible(False) # Eliminar eje y
ax.spines['top'].set_visible(False) # Eliminar recuadro (sin bordes adicionales)
ax.spines['right'].set_visible(False)
ax.set_aspect('equal') # Aspecto de la gráfica
ax.grid(False)  # Eliminar cuadrícula
ax.plot([-0.5, N-0.5], [0.5, 0.5], color='gray', lw=1) # linea gris que cruza las flechas
ax.set_title("Modelo de Ising en 1D\n")

plt.show()
