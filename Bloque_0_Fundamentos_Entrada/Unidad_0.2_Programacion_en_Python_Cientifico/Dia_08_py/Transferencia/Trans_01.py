import pandas as pd

df = pd.DataFrame({
    'Sensor': ["S1","S2","S3"],
    'Temperatura': [24.5,27.1,23.8],
    'Lecturas' : [120,95,143],
    'Activo' : [True,False,True]
}, index=['Med1','Med2','Med3'])

print(f"El dataframe es: \n"
      f"{df}\nContienes los siguientes dtypes: \n{df.dtypes}\n"
      f"Esta compuesto por una forma:\n{df.shape}\n"
      f"Tiene los index: \n{df.index.tolist()}\n"
      f"Y las columnas: \n{df.columns.tolist()}")