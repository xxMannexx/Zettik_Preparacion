Portafolio Día 06: Kit de Procesamiento de Datos y Automatización para VizionarIAEntorno de Ejecución: Raspberry Pi / Linux BashPropósito: Demostrar dominio en transformación de flujos de texto, análisis de datos en terminal, gestión de variables de entorno y persistencia de procesos mediante automatización (cron/systemd) para la operación continua de VizionarIA.1. Transformaciones de Flujo de Texto con sedPara estas pruebas, utilizaremos un archivo de log simulado llamado detecciones.log con el siguiente contenido inicial:text[2026-08-10 08:00:01] INFO: Inicializando pipeline de inferencia.
[2026-08-10 08:01:15] DEBUG: Procesando frame ID 204123.
[2026-08-10 08:01:16] DETECCION: Persona detectada en camara_01.
[2026-08-10 08:01:20] DEBUG: Procesando frame ID 204124.
[2026-08-10 08:02:45] DETECCION: Vehiculo detectada en camara_02.
Usa el código con precaución.A) Sustitución Global (Corrección de error de concordancia: "detectada" por "detectado")Comando:bashsed 's/detectada/detectado/g' detecciones.log
Usa el código con precaución.Salida en Terminal:text[2026-08-10 08:00:01] INFO: Inicializando pipeline de inferencia.
[2026-08-10 08:01:15] DEBUG: Procesando frame ID 204123.
[2026-08-10 08:01:16] DETECCION: Persona detectado en camara_01.
[2026-08-10 08:02:45] DETECCION: Vehiculo detectado en camara_02.
Usa el código con precaución.B) Borrado por Patrón (Eliminación de líneas de ruido analítico "DEBUG")Comando:bashsed '/DEBUG/d' detecciones.log
Usa el código con precaución.Salida en Terminal:text[2026-08-10 08:00:01] INFO: Inicializando pipeline de inferencia.
[2026-08-10 08:01:16] DETECCION: Persona detectada en camara_01.
[2026-08-10 08:02:45] DETECCION: Vehiculo detectada en camara_02.
Usa el código con precaución.C) Edición In Situ con Respaldo Extensión .bakComando:bashsed -i.bak 's/camara_/cam_/g' detecciones.log
Usa el código con precaución.Resultado del Archivo Modificado (detecciones.log):text[2026-08-10 08:00:01] INFO: Inicializando pipeline de inferencia.
[2026-08-10 08:01:15] DEBUG: Procesando frame ID 204123.
[2026-08-10 08:01:16] DETECCION: Persona detectada en cam_01.
[2026-08-10 08:01:20] DEBUG: Procesando frame ID 204124.
[2026-08-10 08:02:45] DETECCION: Vehiculo detectada en cam_02.
Usa el código con precaución.Verificación del Respaldo Generado (detecciones.log.bak):Conserva intacto el texto original con las cadenas camara_01 y camara_02, asegurando la recuperabilidad del sistema ante fallos de regex.2. Análisis e Inferencia de Datos con awkPara los análisis utilizaremos un reporte de telemetría y conteo estructurado llamado metricas.csv:textcamara,objeto,confianza
cam_01,persona,0.94
cam_02,vehiculo,0.88
cam_01,persona,0.91
cam_03,bicicleta,0.76
cam_02,persona,0.85
cam_01,vehiculo,0.92
Usa el código con precaución.A) Filtrado por Condición Estricta (Confianza de detección > 0.90)Comando:bashawk -F',' 'NR > 1 && $3 > 0.90 {print "ALTA_CONFIANZA: " $2 " en " $1 " (" $3 ")"}' metricas.csv
Usa el código con precaución.Salida en Terminal:textALTA_CONFIANZA: persona en cam_01 (0.94)
ALTA_CONFIANZA: persona en cam_01 (0.91)
ALTA_CONFIANZA: vehiculo en cam_01 (0.92)
Usa el código con precaución.B) Agregado: Conteo por Categoría mediante Array AsociativoComando:bashawk -F',' 'NR > 1 {conteo[$2]++} END {for (objeto in conteo) print "Objeto: " objeto " -> Total: " conteo[objeto]}' metricas.csv
Usa el código con precaución.Salida en Terminal:textObjeto: persona -> Total: 3
Objeto: vehiculo -> Total: 2
Objeto: bicicleta -> Total: 1
Usa el código con precaución.C) Agregado Complejo: Promedio de Confianza Global de la InferenciaComando:bashawk -F',' 'NR > 1 {suma += $3; filas++} END {if (filas > 0) print "Métrica de Calidad: Promedio Confianza = " (suma / filas)}' metricas.csv
Usa el código con precaución.Salida en Terminal:textMétrica de Calidad: Promedio Confianza = 0.876667
Usa el código con precaución.3. Demostración Práctica de Herencia de EntornoEl aislamiento de procesos en Unix dicta que un proceso hijo hereda las variables de su entorno padre únicamente si estas han sido explícitamente exportadas a la tabla de entorno global.Comandos de Ejecución y Evidenciabash# Definición de variables en el shell actual (Padre)
VIXIA_LOCAL="Modo_Desarrollo_Local"
export VIXIA_GLOBAL="Modo_Produccion_Pi"

# Intento de lectura desde un subshell (Hijo simulado mediante paréntesis)
( echo "Desde Hijo - Local: [$VIXIA_LOCAL]"; echo "Desde Hijo - Global: [$VIXIA_GLOBAL]" )
Usa el código con precaución.Salida Obtenida en TerminaltextDesde Hijo - Local: []
Desde Hijo - Global: [Modo_Produccion_Pi]
Usa el código con precaución.Explicación MecánicaVIXIA_LOCAL se almacena exclusivamente en la memoria local del Intérprete de Comandos actual (Shell Padre). Al bifurcarse el sistema (fork) para abrir el subshell hijo, este espacio de memoria local no se copia.export VIXIA_GLOBAL instruye al sistema operativo a colocar la variable dentro de la estructura de datos del entorno del proceso. Todo subshell o binario ejecutado posteriormente hereda una copia exacta de esta tabla de entorno.Nota de Seguridad: Siguiendo las buenas prácticas del proyecto, nunca incluiremos tokens o secretos embebidos en el entorno persistente.4. Planificación Robustecida con cronLa automatización de tareas con cron suele fallar en entornos embebidos como la Raspberry Pi debido a la ausencia de variables de entorno comunes como PATH. Esta plantilla soluciona el problema de manera definitiva.Entrada de Cron Diseñada (Frecuencia: Cada hora a los 0 minutos)text0 * * * * /usr/bin/python3 /home/ana/vixia/pipeline.py >> /home/ana/vixia/cron_ejecuciones.log 2>&1
Usa el código con precaución.Desglose Campo por Campo y Justificación de Estabilidad0: Minuto. Se ejecuta exactamente al inicio de cada hora (evita ejecuciones masivas concurrentes cada minuto si se usara *).*: Hora. Aplica para las 24 horas del día.*: Día del Mes. Corre todos los días del mes de forma continua.*: Mes. Activo los 12 meses del año.*: Día de la Semana. Ejecución de lunes a domingo./usr/bin/python3: Ruta Absoluta al Binario. Mitigación de fallo crítico: cron inicializa un entorno mínimo donde PATH solo incluye /usr/bin:/bin. Si se llama solo a python3, el servicio puede fallar al no encontrar el ejecutable./home/ana/vixia/pipeline.py: Ruta Absoluta al Script. Garantiza que el demonio cron localice el archivo sin importar cuál sea el directorio de trabajo por defecto del sistema al instanciarse la tarea.>> /home/ana/vixia/cron_ejecuciones.log: Redirección de Salida Estándar (stdout). Escribe los prints informativos del script añadiendo líneas al final del archivo en lugar de sobreescribirlo (>> vs >).2>&1: Redirección de Errores (stderr) a Salida Estándar. Mitigación de fallo crítico: Si el script de Python arroja un error de ejecución o un fallo de librería, este se enviará directamente al archivo de log junto con la salida normal. Si se omite, el error se pierde o satura el sistema de correo interno de Linux (mail), invisibilizando los bugs de VizionarIA.5. Plantilla Arquitectónica de Servicio systemdEste documento simula la configuración requerida para operar la canalización de procesamiento como un demonio de fondo nativo en el sistema operativo.Archivo de Ejemplo: vizionaria.serviceini[Unit]
Description=Servicio de Inferencia de Datos VizionarIA
After=network.target

[Service]
Type=simple
User=ana
WorkingDirectory=/home/ana/vixia
Environment=MODEL_PATH=/home/ana/vixia/modelo.pt
ExecStart=/usr/bin/python3 /home/ana/vixia/pipeline.py
Restart=on-failure
RestartSec=5
SignalKill=SIGTERM

[Install]
WantedBy=multi-user.target
Usa el código con precaución.Relación Directiva-Concepto y TrazabilidadAfter=network.target (Concepto: Ciclo de Vida del Sistema)Asegura que el servicio espere a que la pila de red de Linux esté lista. Evita que VizionarIA intente transmitir logs o recibir flujos de video antes de que la interfaz de la Raspberry Pi obtenga dirección IP.User=ana (Concepto: Principio de Mínimo Privilegio)Evita ejecutar software de procesamiento de datos como usuario root. Si un atacante compromete el pipeline mediante una inyección de datos en el stream de video, los daños quedarán confinados exclusivamente al directorio home de la usuaria ana, protegiendo la integridad del sistema base.WorkingDirectory=/home/ana/vixia (Concepto: Espacio de Nombres de Ruta)Establece el directorio raíz del proceso. Permite que el script de Python maneje rutas relativas de manera segura hacia scripts internos o dependencias locales sin romperse.Environment=MODEL_PATH=... (Concepto: Configuración Limpia)Inyecta parámetros operativos directamente a la tabla de entorno del proceso de forma limpia antes de invocar el binario principal. Separa el código de la infraestructura (los pesos del modelo).ExecStart=... (Concepto: Ciclo de Vida del Proceso)Declara el comando absoluto exacto que el kernel debe registrar en la tabla de procesos del sistema operativo.Restart=on-failure y RestartSec=5 (Concepto: Tolerancia a Fallos)Gobernabilidad automática del proceso. Si el pipeline sufre un Crash por falta de memoria o interrupción de hardware, systemd esperará 5 segundos para liberar buffers del sistema e intentará levantarlo indefinidamente, garantizando operación 24/7 sin intervención manual.SignalKill=SIGTERM (Concepto: Manejo de Señales Interproceso) Define que al detener el servicio con systemctl stop, el sistema enviará la señal estándar 15 (SIGTERM), otorgándole al script de Python la oportunidad de cerrar descriptores de archivos, streams de video abiertos y conexiones de red de manera ordenada en lugar de un corte abrupto de memoria.WantedBy=multi-user.target (Concepto: Persistencia en Arranque)Indica que al habilitar el servicio con systemctl enable, este se enlazará al modo multiusuario estándar (consola sin entorno gráfico o entorno gráfico completo), permitiendo que VizionarIA inicie de forma automática tan pronto como la Raspberry Pi reciba energía eléctrica.
