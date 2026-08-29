import pandas as pd
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["y", "z", "w"])
print(a + b)
# x     NaN     <- 'x' solo en a: NaN
# y    12.0     <- 'y' en ambas: 2 + 10
# z    23.0     <- 'z' en ambas: 3 + 20
# w     NaN     <- 'w' solo en b: NaN
