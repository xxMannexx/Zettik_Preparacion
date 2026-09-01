import matplotlib
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2,2, figsize=(10,4)) ##Figure con 2 axes

axes[0,1].set_title("Izquierdo")
axes[0,1].set_xlabel("Eje X")
axes[0,1].set_ylabel("Eje Y")
axes[1,0].set_title("Derecho")
axes[1,0].set_xlabel("Eje X")
axes[1,0].set_ylabel("Eje Y")
fig.suptitle("Figura con dos subgráficos")   # título de la Figure completa
fig.tight_layout()  ## Da un espaciado correcto entre plots
fig.show()