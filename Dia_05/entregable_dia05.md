# Entregable Día 05 - Administración del Sistema y Expresiones Regulares

## 1. Cinco búsquedas con 'find' de complejidad creciente

### Búsqueda 1: Por Nombre (Básica)
*   **Comando:** `find . -type f -name "*.py"`
*   **Qué busca:** Todos los archivos regulares que terminen con la extensión `.py` a partir del directorio actual.
*   **Por qué se usa:** Es el punto de partida indispensable para localizar archivos fuentes específicos en proyectos de desarrollo antes de aplicarles inspecciones o refactorizaciones.

### Búsqueda 2: Por Tipo de Archivo
*   **Comando:** `find /var/log -type l`
*   **Qué busca:** Únicamente los enlaces simbólicos (`-type l`) dentro de la ruta del sistema `/var/log`.
*   **Por qué se usa:** Permite auditar la estructura de bitácoras del sistema, asegurando que los accesos directos o redirecciones de logs hacia otros discos apunten de forma correcta y no existan enlaces rotos.

### Búsqueda 3: Por Tamaño y Fecha (Filtros Combinados)
*   **Comando:** `find /var/log -type f -size +50M -mtime -7`
*   **Qué busca:** Archivos regulares en `/var/log` que pesen estrictamente más de 50 Megabytes (`-size +50M`) y que hayan sido modificados en los últimos 7 días (`-mtime -7`).
*   **Por qué se usa:** Es un comando crítico de mantenimiento para administradores de sistemas (SysAdmins). Permite identificar de inmediato qué archivos de registro están creciendo anómalamente rápido en la última semana para prevenir problemas de espacio en disco.

### Búsqueda 4: Por Permisos para Auditoría de Seguridad
*   **Comando:** `find /home -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null`
*   **Qué busca:** Archivos en `/home` que tengan activos los bits de seguridad SUID (`-perm -4000`) o SGID (`-perm -2000`).
*   **Por qué se usa:** Auditoría de seguridad (Hardening). Los archivos con SUID/SGID se ejecutan con los privilegios del propietario (ej. root). Detectar archivos con estos permisos en los directorios de usuarios previene escaladas de privilegios no autorizadas.

### Búsqueda 5: Acción Avanzada con -exec y Filtro Invertido
*   **Comando:** `find proyecto/src -type f -name "*.py" ! -name "__init__.py" -exec grep -l "TODO" {} +`
*   **Qué busca:** Busca archivos `.py` excluyendo los archivos de inicialización de módulos `__init__.py` (`! -name`), y ejecuta de forma masiva eficiente (`{} +`) un `grep` que devuelve solo los nombres de los archivos (`-l`) que contienen la palabra "TODO".
*   **Por qué se usa:** Automatiza la recolección de deuda técnica en un proyecto de software, procesando cientos de archivos en un solo proceso de ejecución sin saturar la memoria de la terminal.

---

## 2. Tabla de Metacaracteres Propios

| Metacarácter | Categoría | Explicación | Ejemplo Práctico | Coincidencia de Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Literal** | Carácter Fijo | Empareja exactamente el carácter indicado tal cual. | `vixia` | Coincide con la palabra "vixia". |
| **.** | Comodín | Empareja cualquier carácter individual, excepto saltos de línea. | `b.to` | Coincide con "beto", "boto", "b2to". |
| **`[]`** | Clases | Define un conjunto o rango de caracteres. Coincide con uno solo de ellos. | `[D d]ia` | Coincide con "Dia" o "dia". |
| **`^$`** | Anclas | `^` marca el inicio estricto de la línea; `$` el final de la línea. | `^inicio$` | Coincide únicamente si la línea solo dice "inicio". |
| **`*`** | Cuantificador | Coincide con cero o más repeticiones del elemento anterior. | `ca*sa` | Coincide con "csa", "casa", "caasa". |
| **`+`** | Cuantificador | Coincide con una o más repeticiones del elemento anterior. | `grep.+` | Coincide con "grep1", "grep_abc". No con "grep". |
| **`?`** | Cuantificador | El elemento anterior es opcional (cero o una aparición). | `colou?r` | Coincide con "color" y "colour". |
| **`{n,m}`** | Cuantificador | Rango explícito. Ocurre entre `n` y `m` veces el elemento previo. | `[0-9]{2,4}` | Coincide con "24", "853", "2026". |
| **`()`** | Grupos | Agrupa caracteres para tratarlos como un bloque único o capturarlos. | `(error)+` | Coincide con "error", "errorerror". |
| **`\|`** | Alternancia | Actúa como un operador lógico OR entre patrones. | `cat\|grep` | Coincide si encuentra "cat" o encuentra "grep". |

---

## 3. Cinco Patrones Regex para Validación de Formatos

### Patrón 1: Fecha (Formato AAAA-MM-DD)
*   **Expresión Regular:** `^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$`
*   **Cadenas Aceptadas:**
    1. `2026-07-30`
    2. `1999-12-31`
*   **Cadenas Rechazadas:**
    1. `26-07-30` *(Faltan dígitos en el año)*
    2. `2026-13-45` *(Mes y día fuera de rango válido)*

### Patrón 2: Hora de 24 Horas (Formato HH:MM)
*   **Expresión Regular:** `^([01][0-9]|2[0-3]):[0-5][0-9]$`
*   **Cadenas Aceptadas:**
    1. `08:45`
    2. `23:59`
*   **Cadenas Rechazadas:**
    1. `24:00` *(La hora 24 es inválida en este formato estándar)*
    2. `9:30` *(Falta el cero a la izquierda en la hora)*

### Patrón 3: Dirección IP IPv4 Estándar
*   **Expresión Regular:** `^([0-9]{1,3}\.){3}[0-9]{1,3}$` *(Nota: Validación estructural simple)*
*   **Cadenas Aceptadas:**
    1. `192.168.1.15`
    2. `10.0.0.1`
*   **Cadenas Rechazadas:**
    1. `192.168.1` *(Falta el cuarto octeto)*
    2. `172.16.256.1` *(Contiene un número fuera del rango de red de un byte)*

### Patrón 4: Correo Electrónico (Email Simplificado)
*   **Expresión Regular:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
*   **Cadenas Aceptadas:**
    1. `usuario.vixia@dominio.com`
    2. `mane123@sub.net.org`
*   **Cadenas Rechazadas:**
    1. `@dominio.com` *(Falta la identidad del usuario antes del arroba)*
    2. `mane@com` *(Falta el dominio de nivel superior o extensión TLD)*

### Patrón 5: Identificador de Usuario de Sistema (ID Alfanumérico)
*   **Expresión Regular:** `^[a-z][a-z0-9_-]{3,15}$`
*   **Cadenas Aceptadas:**
    1. `manee_99`
    2. `vix-user`
*   **Cadenas Rechazadas:**
    1. `1user` *(Falla porque no inicia estrictamente con una letra minúscula)*
    2. `id` *(Muy corto, no cumple la longitud mínima de 4 caracteres)*

---

## 4. Pipeline de Análisis de Log

### Generación del Log de Pruebas (Here-Doc)
Ejecuta este bloque para simular el archivo de log en tu entorno de análisis:
```bash
cat << 'LOGEOF' > servicio.log
2026-07-30 10:01:05 [INFO] IP:192.168.1.50 - Usuario:manee - Acceso concedido
2026-07-30 10:02:11 [WARN] IP:192.168.1.65 - Usuario:invitado - Intento fallido
2026-07-30 10:02:15 [ERROR] IP:192.168.1.50 - Usuario:manee - Timeout de conexion
2026-07-30 10:03:40 [INFO] IP:192.168.1.100 - Usuario:root - Tarea completada
2026-07-30 10:05:12 [ERROR] IP:192.168.1.50 - Usuario:manee - Base de datos bloqueada
LOGEOF
```

### Pipeline de Extracción y Métricas Completo
Este pipeline cuenta incidencias por nivel, aísla el campo **IP**, y calcula la dirección IP más frecuente en las bitácoras:

```bash
echo "=== Conteo por Nivel de Log ==="
grep -o -E "\[(INFO\vert{}WARN\vert{}ERROR)\]" servicio.log | tr -d '[]' | sort | uniq -c

echo -e "\n=== Extracción de IP y el Valor Más Frecuente ==="
grep -o -E "IP:[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" servicio.log | cut -d':' -f2 | sort | uniq -c | sort -nr | head -n 1
```

*   **Resultados esperados del comando:**
    *   Muestra el conteo de eventos distribuidos de la siguiente forma: 2 `ERROR`, 2 `INFO`, 1 `WARN`.
    *   Calcula el valor más frecuente del campo IP indicando de forma limpia: `3 192.168.1.50`.

---

## 5. Dialectos: BRE (Basic Regular Expressions) vs ERE (Extended Regular Expressions)

Para demostrar que ambos dialectos resuelven exactamente la misma lógica, se plantea la búsqueda del patrón **"una o más cifras consecutivas"** dentro de un flujo de texto.

### Comando en dialecto BRE (Basic)
```bash
grep -v "^\$" servicio.log | grep "[0-9]\{1,\}"
```

### Comando en dialecto ERE (Extended)
```bash
grep -v "^\$" servicio.log | grep -E "[0-9]+"
```


### Explicación de las Diferencias de Sintaxis
1.  **Escape de Cuantificadores Modernos:** En **BRE**, los metacaracteres avanzados como `+`, `?`, y las llaves `{}` no se reconocen como operadores de forma nativa; se interpretan como texto literal. Para activar su función especial, es obligatorio antecederlos con una barra invertida (`\`). Por ello se escribe `\{1,\}` para emular el comportamiento de un "uno o más".
2.  **Sintaxis Nativa Extendida:** En **ERE** (activado mediante `grep -E` o usando el comando nativo `egrep`), los cuantificadores modernos se interpretan de forma directa como operadores lógicos por defecto. El signo `+` reemplaza de manera limpia a `\{1,\}` sin necesidad de escapar caracteres, lo que genera expresiones regulares considerablemente más legibles y fáciles de mantener.
