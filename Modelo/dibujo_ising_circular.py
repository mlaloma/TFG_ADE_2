import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Código para dibujar las flechas de los spines en un círculo, orientadas verticalmente, y con una línea gris que las una
N = 8

# Generamos aleatoriamente los spins, -1 para abajo y 1 para arriba
spins = np.random.choice([-1, 1], size=N)

# Radio del círculo
radius = 1.5

# Ángulos para distribuir las flechas a lo largo del círculo
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

# Coordenadas de las flechas (convertidas a coordenadas cartesianas)
x_pos = radius * np.cos(angles)
y_pos = radius * np.sin(angles)

# Configuración de la gráfica
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')  # Aspecto de la gráfica
ax.set_xlim(-radius - 0.5, radius + 0.5)  # Ajustes de los límites del gráfico
ax.set_ylim(-radius - 0.5, radius + 0.5)

# Dibujo de la línea gris que une todas las flechas
ax.plot(np.append(x_pos, x_pos[0]), np.append(y_pos, y_pos[0]), color='gray', lw=1)  # Línea que conecta todas las flechas

# Dibujo de las flechas orientadas verticalmente en posiciones circulares
for i in range(N):
    if spins[i] == 1:
        # Flecha hacia arriba
        ax.add_patch(FancyArrowPatch((x_pos[i], y_pos[i] - 0.5), (x_pos[i], y_pos[i] + 0.5), mutation_scale=15, color='blue'))
    else:
        # Flecha hacia abajo
        ax.add_patch(FancyArrowPatch((x_pos[i], y_pos[i] + 0.5), (x_pos[i], y_pos[i] - 0.5), mutation_scale=15, color='red'))

# Ajustes de visualización
ax.get_yaxis().set_visible(False)  # Eliminar eje y
ax.get_xaxis().set_visible(False)  # Eliminar eje x
ax.spines['top'].set_visible(False)  # Eliminar recuadro (sin bordes adicionales)
ax.spines['right'].set_visible(False)
ax.grid(False)  # Eliminar cuadrícula

ax.set_title("Modelo de Ising en 1D\nDisposición Circular")

plt.show()
