import matplotlib

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')

fig, ax = plt.subplots(figsize=(8, 5))

fotogramas = np.arange(1, 21)
np.random.seed(7)
det_persona = np.random.poisson(5, 20)
det_coche = np.random.poisson(3, 20)

ax.plot(fotogramas, det_persona, marker='o', label='persona', color='teal', linewidth=2)
ax.plot(fotogramas, det_coche, marker='s', label='coche', color='coral', linewidth=2, linestyle='--')

# Elementos minimos de comunicacion (responde D5):
ax.set_title("Evolución de detecciones por fotograma y clase", fontsize=13, pad=12)
ax.set_xlabel("Fotograma", fontsize=11)
ax.set_ylabel("N.º de detecciones", fontsize=11)
ax.legend(title="Clase de objeto", fontsize=10)
ax.set_xlim(1, 20)
ax.set_xticks(fotogramas[::2])
ax.grid(True, alpha=0.4)

# Anotacion de un punto de interes
pico = np.argmax(det_persona)
ax.annotate(f"pico: {det_persona[pico]}",
            xy=(fotogramas[pico], det_persona[pico]),
            xytext=(fotogramas[pico] + 1, det_persona[pico] + 0.5),
            arrowprops=dict(arrowstyle="->", color="gray"), fontsize=9)

fig.tight_layout()
fig.show()
