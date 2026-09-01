import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, os


def guardar_figura(fig, nombre, carpeta="/tmp/figuras", dpi=150):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    plt.close(fig)  # libera la memoria: esencial en pipelines
    return ruta


fig, ax = plt.subplots(figsize=(7, 4))
np.random.seed(3)
datos = np.random.beta(8, 2, 300)
ax.hist(datos, bins=25, color="teal", edgecolor="white", alpha=0.8)
ax.set_title("Distribución de confianza del detector")  # descriptivo, sin rutas internas
ax.set_xlabel("Confianza (0-1)");
ax.set_ylabel("Frecuencia de detecciones")
ax.axvline(datos.mean(), color="red", linestyle="--", label=f"media={datos.mean():.2f}")
ax.legend()
ruta = guardar_figura(fig, "distribucion_confianza.png")
print(f"guardado: {ruta}")
