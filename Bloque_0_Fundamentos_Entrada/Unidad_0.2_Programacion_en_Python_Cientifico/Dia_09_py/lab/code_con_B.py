import matplotlib

import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# 1) Gráfico de línea: evolución de detecciones por fotograma
fotogramas = np.arange(1, 11)
n_det = np.array([3, 5, 4, 7, 6, 8, 5, 9, 7, 6])
axes[0, 0].plot(fotogramas, n_det, marker='o', color='teal', label='detecciones')
axes[0, 0].set_title("Detecciones por fotograma")
axes[0, 0].set_xlabel("Fotograma");
axes[0, 0].set_ylabel("N.º detecciones")
axes[0, 0].legend()

# 2) Gráfico de dispersión: confianza vs tamaño del objeto
np.random.seed(42)
conf = np.random.uniform(0.5, 1.0, 50)
tamano = conf * 100 + np.random.normal(0, 10, 50)
axes[0, 1].scatter(tamano, conf, alpha=1, color='steelblue')
axes[0, 1].set_title("Confianza vs tamaño del objeto")
axes[0, 1].set_xlabel("Tamaño (px^2)");
axes[0, 1].set_ylabel("Confianza")

# 3) Gráfico de barras horizontales: detecciones por clase
clases = ["persona", "coche", "bici", "perro"]
conteos = [42, 27, 15, 8]
axes[1, 0].barh(clases, conteos, color=['teal', 'steelblue', 'coral', 'gold'])
axes[1, 0].set_title("Detecciones por clase");
axes[1, 0].set_xlabel("N.º detecciones")

# 4) Histograma: distribución de la confianza
todas_conf = np.random.beta(8, 2, 200)
axes[1, 1].hist(todas_conf, bins=20, color='teal', edgecolor='white', alpha=0.8)
axes[1, 1].axvline(todas_conf.mean(), color='red', linestyle='--',
                   label=f'media={todas_conf.mean():.2f}')
axes[1, 1].set_title("Distribución de confianza")
axes[1, 1].set_xlabel("Confianza");
axes[1, 1].set_ylabel("Frecuencia")
axes[1, 1].legend()

fig.suptitle("Análisis visual del detector de VizionarIA", fontsize=13, fontweight='bold')
fig.tight_layout()
fig.show()


