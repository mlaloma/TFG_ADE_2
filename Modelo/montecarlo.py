import random
import matplotlib.pyplot as plt

def estimar_pi_visual(num_puntos):
    dentro_circulo = 0
    puntos_x_dentro, puntos_y_dentro = [], []
    puntos_x_fuera, puntos_y_fuera = [], []
    
    for _ in range(num_puntos):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            dentro_circulo += 1
            puntos_x_dentro.append(x)
            puntos_y_dentro.append(y)
        else:
            puntos_x_fuera.append(x)
            puntos_y_fuera.append(y)
    
    pi_estimado = (dentro_circulo / num_puntos) * 4
    
    # Graficar los puntos
    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(puntos_x_dentro, puntos_y_dentro, color='blue', s=1, label='Dentro del círculo')
    ax.scatter(puntos_x_fuera, puntos_y_fuera, color='red', s=1, label='Fuera del círculo')
    
    # Dibujar el círculo
    circle = plt.Circle((0, 0), 1, color='black', fill=False)
    ax.add_patch(circle)
    
    # Configuración de la gráfica
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.set_title(f'Estimación de π con {num_puntos} puntos: {pi_estimado:.5f}\n', fontsize=14)
    
    # Ajustar la leyenda para que no se corte
    fig.subplots_adjust(bottom=0.25)  # Aumentar el margen inferior
    plt.legend(loc='lower center', bbox_to_anchor=(0.8, -0.2), ncol=1, frameon=False)

    plt.grid()
    plt.show()
    
    return pi_estimado


num_puntos = 10000
pi_estimado = estimar_pi_visual(num_puntos)
print(f"Estimación de π con {num_puntos} puntos: {pi_estimado}")
