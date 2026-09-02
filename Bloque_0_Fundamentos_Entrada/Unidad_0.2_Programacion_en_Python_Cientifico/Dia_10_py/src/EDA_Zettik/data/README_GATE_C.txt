Gate C — ataque de limpieza

Pasa el dataset principal primero por carga.py y luego por limpieza.py.

Después de limpieza verifica:
- no hay duplicados completos;
- no quedan NaN en objeto, fotograma ni confianza;
- confianza está dentro de [0,1];
- objeto queda como texto;
- confianza queda como flotante;
- fotograma queda como entero;
- limpieza() no muta el DataFrame original;
- logging separa duplicados, faltantes eliminados, imputaciones y atípicos.

caso_toda_confianza_nan.csv debe provocar ErrorFaltantes.
