import pandas as pd

df = pd.DataFrame({
    'Sensor' : ['S1','S2','S3','S4','S5'],
    'Zona' : ["Norte","Sur","Norte","Sur","Norte"],
    'Temperatura' : [24,28,26,30,25]
})

print(df.groupby("Zona")["Temperatura"].agg([
    'count',
    'sum',
    'mean',
    'max'
]))
