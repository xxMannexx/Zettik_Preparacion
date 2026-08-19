Explicacion de la ejecucion de : cd /tmp && bash -c 'cd /etc' && pwd
cd /tmp
/home/manee/ZETTIK/VixIA/Dia_01

Podemos observar que su ejecucion da como resultado /tmp, pero ¿Por que?
=== PASO POR PASO ===
1. Primero entender los interconectores que tenemos por la linea: '&&'. Este interconector funciona como un and y si seguimos la logica solo se ejecutara lo siguiente si se ha tenido exito en la ejecucion en curso. 'bash -c. Esto nos genera una miniterminal o terminal hija, que se puede explicar como un fork() una copia casi exacta de si mismo que ejecuta lo que se encuentra en comillas simples'

2. Una vez esto entendido tenemos que saber que en primer lugar nos lleva a ejecutar el cambio de directorio que es /tmp, en seguida crea una miniterminal y ejecuta el cambio de directorio, por ultimo como se ha tenido exito ejecuta la impresion del directorio pero como el cambio de directorio paso en un proceso hijo la ruta de directorio impresa obviamente siguen siendo los archivos temporales
