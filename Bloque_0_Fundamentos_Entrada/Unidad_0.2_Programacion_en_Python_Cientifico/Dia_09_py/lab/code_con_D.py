import matplotlib


import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

np.random.seed(42)
clases = np.random.choice(["persona", "coche", "bici", "perro"], 300, p=[0.40, 0.30, 0.20, 0.10])
confs = np.clip(np.where(clases == "persona", np.random.beta(9, 2, 300),
                         np.where(clases == "coche", np.random.beta(7, 3, 300),
                                  np.where(clases == "bici", np.random.beta(6, 4, 300),
                                           np.random.beta(5, 5, 300)))), 0, 1)
df = pd.DataFrame({"clase": clases, "confianza": confs,
                   "fotograma": np.random.randint(1, 21, 300)})

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1) Histograma con grupos por clase (hue)
sns.histplot(data=df, x="confianza", hue="clase", bins=20, element="step", ax=axes[0])
axes[0].set_title("Distribución de confianza por clase")
axes[0].set_xlabel("Confianza")

# 2) Boxplot: distribución por clase
sns.boxplot(data=df, x="clase", y="confianza", ax=axes[1], palette="Set2",
            order=["persona", "coche", "bici", "perro"])
axes[1].set_title("Confianza por clase");
axes[1].set_xlabel("Clase");
axes[1].set_ylabel("Confianza")

# 3) Lineplot con banda: evolución temporal
sns.lineplot(data=df, x="fotograma", y="confianza", hue="clase",
             ax=axes[2], estimator="mean", errorbar="sd")
axes[2].set_title("Confianza media por fotograma y clase")
axes[2].set_xlabel("Fotograma");
axes[2].set_ylabel("Confianza media")

fig.suptitle("Seaborn: visualización estadística del detector", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.show()
