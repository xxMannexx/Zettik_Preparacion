# Informe EDA — VizionarIA

## Resumen del dataset
- Detecciones analizadas: 118275
- Clase predominante: persona

## Distribución de clases
- persona: 54045
- coche: 34677
- bici: 21272
- perro: 8281

## Distribución global de confianza
- Media: 0.7718
- Mediana: 0.7948
- Q1: 0.7017
- Q3: 0.8711
- Desviación estándar: 0.1459

## Confianza por clase
- bici: 0.7733
- coche: 0.7712
- perro: 0.7727
- persona: 0.7715

## Relación temporal
- Correlación confianza-fotograma: 0.0031
- No se observa una relación lineal relevante entre fotograma y confianza.

## Panel EDA
![Panel EDA](panel_eda.png)

## Conclusiones
- La clase predominante es persona.
- Las medias de confianza por clase son muy similares entre sí.
- La distribución de confianza presenta una dispersión moderada.
- No se observa una tendencia lineal clara con el avance de los fotogramas.