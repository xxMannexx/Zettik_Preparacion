import pandas as pd, numpy as np

df = pd.DataFrame({
    'Sensor': ["S1","S2","S3","S4"],
    'Temperatura': [24.5,np.nan,27,25.5]
})

# print(f"El Dato faltante esta en: {(df.isna()).stack().index[3]}")
print(f"El Dato faltante esta en: \n{df.isna()}")
print(f"La media es original es:")
print(df['Temperatura'].mean())

df['Temperatura'] = df['Temperatura'].fillna(df['Temperatura'].mean())
print(df)
print(df.isna())