1.	Tabla de conversión propia: los 8 valores octales (0–7) con su cadena rwx, escrita por mi.

Octal | Binario | Cadena rwx | Significado técnico
-----------------------------------------------------------
  0   |   000   |    ---     | Sin ningún permiso
  1   |   001   |    --x     | Solo ejecución
  2   |   010   |    -w-     | Solo escritura
  3   |   011   |    -wx     | Escritura y ejecución
  4   |   100   |    r--     | Solo lectura
  5   |   101   |    r-x     | Lectura y ejecución
  6   |   110   |    rw-     | Lectura y escritura
  7   |   111   |    rwx     | Permisos totales (r, w, x)

2.	Evidencia de enlaces: salida de ls -li mostrando que un enlace duro comparte inodo con su origen y un simbólico no, con tu explicación (3–4 líneas) del mecanismo.

=== Enlaces inodo y contador ===                                                                                              'touch base.txt'                                                                       
1876 -rw-r--r-- 2 manee manee 17 Jul  8 16:08 base.txt
2006 lrwxrwxrwx 1 manee manee  8 Jul  8 16:09 blando.txt -> base.txt
1876 -rw-r--r-- 2 manee manee 17 Jul  8 16:08 duro.txt

El inodo de base.txt y duro.txt debe COINCIDIR; el de blando debe diferir

OK: duro comprate inodo con base

OK: blando tiene su propio inodo

¿Por que un enlace duro comparte inodo y un enlace simbolico no?

Permitiendome explicarlo como de manera un tanto coloquial una manera facil de entenderlo seria con cajas y etiquetas, esto tomando como caja el contenido del archivo (inodo) y el nombre como la etiqueta que referencia a esta caja (numero de inodo/caja), un enlace duro es solamente poner un nombre con el mismo numero de inodo, mejor explicado como poner una etiqueta mas a la caja, cualquiera de las 2 etiquetas lleva hacia el contenido de la caja. En un enlace duro no sucede esto se crea una caja nueva con una etiqueta nueva pero en este caso el contenido de la caja es la referencia hacia el contenido de otra caja, es como si una caja te llevara a otra desde cualquier lugar, ojo, muy importante que un enlace duro no permite refernciar entre diferentes rutas.
3.	Cálculo de umask: tu umask actual, la derivación base & ~umask para archivo y directorio, y la verificación creando uno de cada.

Demostrar el efecto del umask creando con 2 mascaras distintas
                                                                   Esto se da por el cambio bit a bit de la siguiente condicion:                                                                         final = base && ~umask                                                                        
=== umask 022 (000 010 010) ===
644 -rw-r--r-- f022
755 drwxr-xr-x d022

=== umask 077 (000 111 111) ===
600 -rw------- f077
700 drwx------ d077

4.	Diagnóstico de permission denied: un caso que provoques (script sin x, o directorio sin x), el mensaje de error, y el chmod exacto que lo resuelve, con explicación de qué bit faltaba y sobre qué objeto.

Provocar y resolver un permission deniend                                                                                     Primero es necesario crear un archivo ejecutable en este caso (run.sh):                                                                                                                                  'echo El ejecutable funciona > run.sh'                                                   
 === Antes del chmod +x ===
-bash: ./run.sh: Permission denied
(Fallo como se esperaba: sin bit x)                                                                                                   Para hacer que funcione se le dan permisos de ejecucion al archivo en ugo:                                                                                                                               'chmod +x run.sh'

=== Despues de chmod +x ===
El ejecutable funciona


5.	Estructura segura para la RPi: tres archivos con permisos por rol (ejecutable 755, secreto 600, datos 644) y la justificación de seguridad de cada uno.

'mkdir -p rpi/{bin,config,data}
echo TOKEN=xyz > rpi/config/secreto.env
echo muestra > rpi/data/lectura.csv
 
chmod 755 rpi/bin/arranque.sh     # ejecutable por el sistema, escribible solo por ti
chmod 600 rpi/config/secreto.env  # secreto: solo tú
chmod 644 rpi/data/lectura.csv    # datos: tú escribes, el resto lee
 
# Verificar todo de un vistazo:
ls -l rpi/bin rpi/config rpi/data
'
