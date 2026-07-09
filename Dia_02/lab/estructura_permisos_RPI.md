Este es un ejemplo de estructura preparada con los permisos correctos para un despliegue real para la Raspberry PI

## A partir de aqui es codigo
     mkdir -p rpi/{bin,config,data}
     echo "#!/bin/bash" > rpi/bin/arranque.sh
     echo "TOKEN=xyz" > rpi/config/secreto.env
     echo "muestra" > rpi/data/lectura.csv

     chmod 755 rpi/bin/arranque.sh     # ejecutable por el sistema, escribible solo por ti
     chmod 600 rpi/config/secreto.env  # secreto: solo tú
     chmod 644 rpi/data/lectura.csv    # datos: tú escribes, el resto lee
     
     # Verificar todo de un vistazo:
     ls -l rpi/bin rpi/config rpi/data
