import pandas as pd, numpy as np

s = pd.Series([1.0, 2.0, np.nan, 4.0])
print(s + 10)  # [11, 12, NaN, 14]  <- el NaN se propaga
print(s.mean())  # 2.333...  <- mean OMITE el NaN (skipna=True)
print(s.sum())  # 7.0       <- sum también omite el NaN
print(s.isna().tolist())  # [False, False, True, False]

# Manejar los datos faltantes:
print(s.dropna().tolist())  # [1.0, 2.0, 4.0]   <- eliminar
print(s.fillna(0).tolist())  # [1.0, 2.0, 0.0, 4.0]  <- imputar con 0
print(s.fillna(s.mean()).round(3).tolist())  # imputar con la media

# Suma de dos Series: el NaN se PROPAGA en operaciones elemento a elemento
t = pd.Series([10.0, np.nan, 30.0, 40.0])
print((s + t).tolist())  # [11.0, nan, nan, 44.0]  <- NaN en posiciones donde hay NaN
