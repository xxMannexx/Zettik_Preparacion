 1.	Diagrama de flujos: un esquema (en texto) de stdin/stdout/stderr con sus descriptores (0/1/2) y una frase explicando qué es un descriptor de archivo.
 
 Un File descriptor es en naturaleza un indice que representa la tuberia/flujo por el el cual el Comando dara sus resultados hay 3: ENTRADA/SALIDA/ERRORES
 apoyando asi la filosofia de todo es un archivo en linux.
 
 
 
       [ ENTRADA ]                               [ PROCESO ]                                [ SALIDAS ]
       
    Teclado, archivo                     Programa / Comando en ejecución                Pantalla, archivos
     o tubería (|)                         (Ej: grep, cat, app.log)                       o "hoyo negro"
           │                                          │                                          │
           │                                          │                                          │
           ▼                                          ▼                                          ▼
   ┌───────────────┐                          ┌───────────────┐                          ┌───────────────┐
   │ Standard Input│ ─── (FD 0 / stdin) ────> │               │ ─── (FD 1 / stdout) ───> │Standard Output│
   │    (stdin)    │                          │   PROCESO     │ (Flujo de datos normal)  │   (stdout)    │
   └───────────────┘                          │    LINUX      │                          └───────────────┘
                                              │               │                          ┌───────────────┐
                                              │               │ ─── (FD 2 / stderr) ───> │ Standard Error│
                                              └───────────────┘  (Mensajes de error)     │   (stderr)    │
                                                                                         └───────────────┘

2.	`>` vs `>>`: una demostración con el contenido del archivo antes y después de cada operación, evidenciando truncado vs anexado.

La redireccion de salida hacia un archivo contiene dos elementos los cuales son AÑADIR y TRUNCAR, depende de la necesidad del usuario se usa uno u otro en el siguiente ejemplo se observa como funciona

## Al Escribir en un archivo nuevo usaremos añadir debido a que no tiene nada, en caso contrario cuando un archivo ya esta escrito es necesario usar el doble >> ya que su manera de abrir el archivo es añadiendo y no borrando todo, EJEMPLO:

mensaje > archivo # Esta linea guarda desde la primer linea del documento sin excepcion. Al ejecutar cat archivo

    Mensaje

## Si tu el siguiente mensaje que quieras agregar no lo redireccionas con >> la antes escrito se borrara debido a la bandera de truncado con la que el > abre el archivo

siguiente_mensaje >> archivo

3.	Separación de canales: un comando que produzca resultados y errores, con stderr enrutado a un archivo y stdout a otro, mostrando el contenido de cada uno.

Como ya observamos en los FD las salidas tienen un estandar de a donde ir tanto errores como salidas normales y no olvidar los inputs a travez de '<'
Estas salidas las podemos redireccionar a travez de su indice y alguna combinacion de componentes:
'2>' Redireccionas errores
'1>' Redireccionas Salida
'>&2' Redirecionas errores a la tuberia de salida comun
'>&1' Redireccionas salida comun a el flujo de errores
'2>&1' Redireccionas los dos flujos al mismo canal haciendo que los errores vayan a donde va la salida comun por ello un cambio de orden afecta su funcionamiento

Un comando de ejemplo seria: 

ls /etc/passwd /carpeta/fantasma > salida_normal.txt 2> errores.txt

### 4. Pipeline de análisis

Para este ejercicio, simulamos el comportamiento de un servidor web generando un archivo de log propio llamado `servidor.log` mediante un Here-Doc. Posteriormente, aplicamos un pipeline de cuatro etapas para extraer métricas de tráfico.

#### Generación del Log (`servidor.log`)

```bash
cat << 'EOF' > servidor.log
192.168.1.5 - GET /index.html 200
10.0.0.3 - POST /login 401
192.168.1.5 - GET /dashboard 200
192.168.1.20 - GET /images/logo.png 200
10.0.0.3 - POST /login 401
192.168.1.5 - GET /index.html 200
10.0.0.3 - GET /index.html 200
EOF
```

#### Comando Utilizado (Pipeline)

El objetivo es listar las direcciones IP que realizaron peticiones exitosas (código HTTP 200), ordenadas de mayor a menor frecuencia:

```bash
grep "200" servidor.log | cut -d' ' -f1 | sort | uniq -c | sort -rn
```

#### Desglose de Componentes y Etapas

*   **`grep "200" servidor.log`**: Filtra el archivo y deja pasar únicamente las líneas que contienen el código de estado `200` (peticiones exitosas), descartando los intentos fallidos (`401`).
*   **`cut -d' ' -f1`**: Utiliza el espacio en blanco (`' '`) como delimitador y extrae el primer campo (`-f1`), aislando exclusivamente las direcciones IP de los clientes.
*   **`sort`**: Ordena las direcciones IP alfabéticamente. Este paso es un requisito indispensable para la siguiente etapa, ya que `uniq` solo puede agrupar líneas duplicadas si se encuentran en posiciones consecutivas.
*   **`uniq -c`**: Elimina las repeticiones consecutivas e introduce un prefijo numérico en cada línea que indica la cantidad de veces que apareció esa IP en el flujo.
*   **`sort -rn`**: Realiza una ordenación numérica (`-n`) de forma invertida (`-r`) tomando como referencia el conteo generado por `uniq`, posicionando a los clientes más activos al inicio.

#### Resultado Obtenido en Pantalla

```text
      3 192.168.1.5
      1 192.168.1.20
      1 10.0.0.3
```

*(El reporte final demuestra que la IP `192.168.1.5` fue la que registró la mayor actividad con un total de 3 accesos exitosos).*

5.	`tee` en acción: un uso de tee que guarde y muestre a la vez, con justificación de por qué es útil (p. ej. capturar el log de un proceso largo).

### 5. `tee` en acción

El comando `tee` funciona como una bifurcación en T dentro de un pipeline de datos: recibe información por la entrada estándar (`stdin`), escribe una copia exacta en uno o varios archivos en el disco y, de forma simultánea, deja pasar los datos intactos hacia la salida estándar (`stdout`) para que sigan su camino por la terminal.

#### Comando de Ejemplo

En este escenario, simulamos la ejecución de un script de automatización o un proceso de compilación largo, guardando todo su progreso en un archivo de auditoría mientras lo monitoreamos en tiempo real:

```bash
echo "Iniciando optimización del sistema..." | tee -a auditoria_sistema.log
```

*(Nota: Se utiliza la opción `-a` o `--append` para añadir la información al final del archivo sin borrar los registros que ya existían previamente).*

#### Justificación de Utilidad en Entornos Reales

El uso de `tee` es indispensable en la administración de sistemas debido a las siguientes ventajas críticas:

1. **Monitoreo y Persistencia Simultáneos:** En procesos de larga duración (como respaldos de bases de datos, actualizaciones del sistema o scripts de despliegue), `tee` permite al administrador ver las alertas o fallos en la pantalla en tiempo real sin perder el registro histórico de lo ocurrido para un análisis posterior.
2. **Evitar la Pérdida de Salida:** Si un proceso largo envía miles de líneas a la terminal, el búfer de la pantalla de nuestra consola puede saturarse y borrar las primeras líneas. `tee` garantiza que absolutamente toda la salida quede guardada de forma segura en el almacenamiento físico.
3. **Auditoría de Tareas Automatizadas:** Permite encadenar herramientas de notificación o procesamiento posterior dentro de la tubería mientras se genera el reporte de texto en el disco duro, todo en un único viaje de datos.

#### Resultado Obtenido en Pantalla

```text
Iniciando optimización del sistema...
```

#### Contenido Verificado en el Archivo (`auditoria_sistema.log`)

```bash
cat auditoria_sistema.log
```

```text
Iniciando optimización del sistema...
```
