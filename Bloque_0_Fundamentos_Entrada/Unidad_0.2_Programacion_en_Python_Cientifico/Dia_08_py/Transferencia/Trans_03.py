import pandas as pd

df = pd.DataFrame({
    'Sensor': ["S1","S2","S3"],
    'Temperatura': [24.5,27.1,23.8],
    'Lecturas' : [120,95,143],
    'Activo' : [True,False,True]
}, index=['Med1','Med2','Med3'])

print(df,'\n')

print(f"Temperatura de Med2:\n"
      f"{df.loc['Med2','Temperatura']}")
print(f"Ahora con iloc: \n"
      f"{df.iloc[1,1]}")


print("\nSeleccionar solo las columnas Sensor y Temperatura:")
print(df[['Sensor','Temperatura']])

print("\nFiltrar únicamente sensores activos y con temperatura mayor a 24")
print(df[(df['Activo']==True) & (df['Temperatura']>24)])