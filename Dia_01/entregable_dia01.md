# ENTREGABLE DÍA 01 - MAPA DE ORIENTACIÓN DEL SISTEMA

## 1. Mapa del FHS
=== Salida del proceso tree -L 1 / ===
/
├── bin -> usr/bin
├── boot
├── dev
├── etc
├── home
├── init
├── lib -> usr/lib
├── lib64 -> usr/lib64
├── lost+found
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin -> usr/sbin
├── snap
├── srv
├── sys
├── tmp
├── usr
└── var

22 directories, 1 file

### Explicación de 8 directorios principales:
1. /tmp: En este se guardan archivos temporales que se eliminan al reiniciar.
2. /: Raiz del arbol completa, basicamente de aqui nace todo.
3. /root: Este es el directorio del superusuario o lo que muchos llaman administrador.
4. /bin: Aqui se guardan los binarios principales del sistema.
5. /usr: En este se guardan todos los programas y datos instalados en el SO.
6. /home: Este es el directorio principal del usuario, basicamente donde se guardan la mayoria de archivos de los usos cotidianos.
7. /etc: En este directorio se guardan las configuraciones del sistema.
8. /var: En este se guardan todos los datos variables que cambian en tiempo de ejecucion.

## 2. Listados Comentados de ls -li

=== Directorio 1: /usr ===
total 68
 1471 drwxr-xr-x   2 root root 32768 Jun 25 13:51 bin
 2373 drwxr-xr-x   2 root root  4096 Apr 20 02:46 games
 2374 drwxr-xr-x   4 root root  4096 Apr 20 12:06 include
 2380 drwxr-xr-x  58 root root  4096 Jun  9 20:44 lib
15955 drwxr-xr-x   2 root root  4096 Apr 20 12:05 lib64
15957 drwxr-xr-x  14 root root  4096 Jun  9 20:44 libexec
16015 drwxr-xr-x  11 root root  4096 Apr 20 12:05 local
16042 drwxr-xr-x   2 root root  4096 Jun  9 20:41 sbin
16218 drwxr-xr-x 115 root root  4096 Jun  9 20:44 share
41929 drwxr-xr-x   2 root root  4096 Apr 20 02:46 src
Interpretación de una línea real:
Línea elegida: '1471 drwxr-xr-x 2 root root 32768 Jun 25 13:51 bin'
- Inodo: 1471
- Tipo de archivo: d (Directorio)
- Permisos: rwxr-xr-x (Lectura, escritura y ejecución para dueño; lectura y ejecución para grupo y otros)
- Enlaces: 2 enlaces duros al inodo
- Dueño: root
- Grupo: root
- Tamaño: 32768 bytes
- Fecha/Hora: Jun 25 13:51
- Nombre: bin

=== Directorio 2: $HOME ===
total 4
38671 drwxr-xr-x 3 manee manee 4096 Jun 25 13:19 ZETTIK
Interpretación de una línea real:
Línea elegida: '38671 drwxr-xr-x 3 manee manee 4096 Jun 25 13:19 ZETTIK'
- Inodo: 38671, Tipo: d, Permisos: rwxr-xr-x, Enlaces: 3, Dueño: manee, Grupo: manee, Tamaño: 4096 bytes, Modificación: Jun 25 13:19, Nombre: ZETTIK

=== Directorio 3: Variable local ($VAR / Directorio de Trabajo) ===
total 28
38697 drwxr-xr-x 3 manee manee 4096 Jun 25 20:08 a
38705 -rw-r--r-- 1 manee manee 1004 Jun 25 21:00 desafio_01.md
38708 -rw-r--r-- 1 manee manee 2668 Jun 25 22:17 entregable_dia01.md
 8963 -rw-r--r-- 1 manee manee  399 Jun 25 19:23 fhs_panorama.txt
 8964 -rw-r--r-- 1 manee manee 1075 Jun 25 19:26 listados_comentados.txt
38687 -rw-r--r-- 1 manee manee  111 Jun 25 19:28 modelo_procesos.txt
 8958 drwxr-xr-x 3 manee manee 4096 Jun 25 14:08 ~Zettik
Interpretación de una línea real:
Línea elegida: '38705 -rw-r--r-- 1 manee manee 1004 Jun 25 21:00 desafio_01.md'
- Inodo: 38705, Tipo: - (Archivo regular), Permisos: rw-r--r--, Enlaces: 1, Dueño: manee, Grupo: manee, Tamaño: 1004 bytes, Modificación: Jun 25 21:00, Nombre: desafio_01.md

## 3. Evidencia del Modelo de Procesos
=== Comando: type cd ===
cd is a shell builtin
=== Comando: type -a ls ===
ls is aliased to `ls --color=auto'
ls is /usr/bin/ls
ls is /bin/ls

### Explicación del modelo de procesos:
Difieren porque 'cd' es un comando interno de la shell (Builtin). Modifica directamente el entorno del proceso actual (CWD) sin crear un proceso hijo; si fuera externo, cambiaría el directorio de un hijo y la terminal principal se quedaría en el mismo lugar. En cambio, 'ls' es un comando externo (o alias apuntando a un binario) que requiere que la shell haga un 'fork' para duplicarse, ejecute en 'foreground' un proceso hijo, muestre los datos y luego muera para devolver el control.

## 4. Tres Pares de Rutas
PUNTO DE PARTIDA DECLARADO (pwd): /home/manee/ZETTIK/VixIA/Dia_01

Par 1:
- Ruta Absoluta: /home
- Ruta Relativa: ../../../
- Confirmación de llegada: cd ../../../ && pwd

Par 2:
- Ruta Absoluta: /etc
- Ruta Relativa: ../../../../etc
- Confirmación de llegada: cd ../../../../etc && pwd

Par 3:
- Ruta Absoluta: /home/manee/ZETTIK
- Ruta Relativa: ../../
- Confirmación de llegada: cd ../../ && pwd

