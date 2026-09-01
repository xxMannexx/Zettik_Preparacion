import matplotlib


import pandas as pd, numpy as np, matplotlib.pyplot as plt

np.random.seed(0)
df = pd.DataFrame({
    "objeto": np.random.choice(["persona", "coche", "bici", "perro"], 200),
    "confianza": np.random.beta(7, 2, 200),
    "fotograma": np.random.randint(1, 21, 200),
})

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1) Barras desde groupby (Día 8)
df.groupby("objeto")["confianza"].count().sort_values(ascending=False).plot(
    kind="barh", ax=axes[0], color="teal")
axes[0].set_title("Detecciones por clase");
axes[0].set_xlabel("N.º detecciones")

# 2) Evolución temporal desde groupby
df.groupby("fotograma").size().plot(
    kind="line", ax=axes[1], marker="o", color="steelblue")
axes[1].set_title("Detecciones por fotograma")
axes[1].set_xlabel("Fotograma");
axes[1].set_ylabel("N.º detecciones")

# 3) Histograma de confianza con .plot()
df["confianza"].plot(kind="hist", ax=axes[2], bins=20, color="coral", edgecolor="white")
axes[2].set_title("Distribución de confianza")
axes[2].set_xlabel("Confianza");
axes[2].set_ylabel("Frecuencia")

fig.suptitle("Análisis EDA con Pandas.plot()", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.show()
