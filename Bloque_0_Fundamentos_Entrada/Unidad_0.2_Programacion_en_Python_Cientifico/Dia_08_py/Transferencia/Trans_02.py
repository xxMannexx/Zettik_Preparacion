import numpy as np
import pandas as pd

serie_A = pd.Series([10,20,30],index=['cam1','cam2','cam3'],dtype=np.int16)
serie_B = pd.Series([100,200,300],index=['cam3','cam1','cam4'],dtype=np.int16)

print(f"La serie A:\n{serie_A}\nLa serie B:\n{serie_B}\n")
print(f"\nLas operaciones entre ellas provocaran una discrepancia ya que aunque seda por vectorizacion, se basa en los index por lo cual el resultado esperado es:"
      f"A+B = [210,NaN,130,NaN] a continuacion se demuestra: ")
print(f"\nSerie A + B:\n{serie_A + serie_B}\n")
print(f"\nSerie A * B:\n{serie_A * serie_B}\n")