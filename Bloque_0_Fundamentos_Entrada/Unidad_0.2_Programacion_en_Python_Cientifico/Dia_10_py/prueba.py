from matplotlib import pyplot as plt
import pandas as pd


dataframe = pd.DataFrame({
    'objeto': ['A', 'A', 'B', 'C'],
    'confianza': [0.85, 0.85, 1, 0.7],
    'fotograma': [10, 10, 11, 12]
})




fig, ax = plt.subplots(2, 2)

## Grafico de linea: Evolución/comportamiento de confianza por fotograma
ax[0, 0].plot(dataframe['fotograma'],dataframe['confianza'])

plt.show()