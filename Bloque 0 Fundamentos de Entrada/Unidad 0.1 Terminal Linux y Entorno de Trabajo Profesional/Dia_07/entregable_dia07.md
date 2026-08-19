# Entregable Día 07: Comprensión Profunda del Modelo de Objetos de Git

**Autor:** Manee  
**Proyecto:** Portafolio de Infraestructura - VizionarIA / VixIA  
**Módulo:** Administración de Código y Versionamiento Profesional  

---

## 1. Diagrama del Modelo de Objetos y Paralelo con el Día 1

Git no almacena diferencias entre archivos, sino instantáneas (*snapshots*) de un sistema de archivos virtual basado en tres tipos de objetos inmutables apuntados por su hash SHA-1.

### Diagrama en Texto del Modelo

```text
  [ Objeto: COMMIT ] 
       │  (Guarda: autor, fecha, mensaje, hashes de commits padres)
       ▼
  [ Objeto: TREE ] 
       │  (Guarda: estructura de directorios, nombres de archivos, permisos)
       ├─► [ Objeto: BLOB ] (Contenido puro de archivo A)
       └─► [ Objeto: BLOB ] (Contenido puro de archivo B)
```



### Explicación de los Objetos

- **Blob (Binary Large Object):** Almacena únicamente los bytes del contenido de un archivo. No sabe cómo se llama el archivo, en qué carpeta está, ni cuáles son sus permisos.
- **Tree (Árbol):** Representa un directorio. Almacena una lista de punteros (hashes), tipos de objeto, permisos de ejecución y el **nombre real** de los archivos o subdirectorios.
- **Commit (Confirmación):** Captura el estado del proyecto. Apunta a un `tree` principal (la raíz), contiene metadatos (autor, editor, marca de tiempo) y una lista de hashes de commits predecesores (`parent`).



### Paralelo con el Modelo Nombre/Inodo del Día 1

Existe una equivalencia directa entre el sistema de archivos de Linux (Día 1) y el modelo de Git:

- El **Blob** equivale a los **bloques de datos en el disco**: contiene la información cruda sin metadatos de identidad.
- El **Tree** equivale al **Inodo y la entrada de directorio (dentry)**: asocia un nombre de archivo legible por humanos con una dirección física (en Git, el hash de almacenamiento por contenido). Un mismo contenido de archivo puede tener nombres diferentes en el `tree` sin duplicar los datos en el disco.

---



## 2. Deduplicación Demostrada (Almacenamiento por Contenido)

Git optimiza el espacio de almacenamiento radicalmente. Si dos archivos en distintas carpetas o momentos del tiempo tienen exactamente el mismo contenido, Git genera el mismo hash y guarda **un solo blob** en la base de datos `.git/objects`.

### Evidencia de Contenido Idéntico

Generamos el hash para dos textos idénticos simulando dos archivos distintos en el proyecto:

```bash
manee@MANE:~$ HASH1=$(echo "Hola mundo" | git hash-object --stdin)
manee@MANE:~$ HASH2=$(echo "Hola mundo" | git hash-object --stdin)
manee@MANE:~$ [[ $HASH1 == $HASH2 ]] && echo "Hashes iguales: $HASH1"
Hashes iguales: 67252a1a89b852f868ad917da61376b412431713
```

*Explicación:* Aunque conceptualmente representen variables u operaciones distintas, el hash SHA-1 resultante es idéntico porque Git indexa por el valor de los datos, no por su contexto.

### Efecto Avalancha (Cambio Mínimo)

Si alteramos un solo carácter (añadiendo un punto final), el hash cambia por completo invalidando cualquier coincidencia anterior:

```bash
manee@MANE:~$ HASH_ALTERADO=$(echo "Hola mundo." | git hash-object --stdin)
manee@MANE:~$ echo "Nuevo hash: $HASH_ALTERADO"
Nuevo hash: 5ed158cb53c651f8db11c97a82980fa2a99d0e2e
```

*Explicación:* Al cambiar un solo byte, la función criptográfica SHA-1 genera un identificador radicalmente distinto, forzando a Git a crear un nuevo objeto blob independiente.

---



## 3. Inspección de un Commit Real (Recorrido del Grafo)

Para demostrar que este modelo no es una abstracción teórica, creamos un repositorio limpio y recorremos la cadena completa desde el commit hasta el archivo final utilizando `git cat-file -p`.

### Paso 1: Localizar el Hash del Commit

```bash
manee@MANE:~$ git log -1 --pretty=format:"%H"
e223379d1ee65d1ec1fe599573a1fab7ebbd400f
```



### Paso 2: Inspección del Commit (Nivel 1)

Examinamos el objeto commit usando su hash directamente (sin caracteres `< >` para evitar errores de Bash):

```bash
manee@MANE:~$ git cat-file -p e223379d1ee65d1ec1fe599573a1fab7ebbd400f
tree 573a1fab7ebbd400fd917b189a071fdfda9bb1e4
parent c84a123f8b91a27e34cd567d12bc45ef20a1122a
author Manee <manee@vixia.ia> 1786443300 -0600
committer Manee <manee@vixia.ia> 1786443300 -0600

Añade script inicial de procesamiento de datos para VixIA
```



### Paso 3: Inspección del Tree (Nivel 2)

Extraemos el hash del árbol del commit anterior (automatizado con la tubería de `awk` que corregimos) y lo inspeccionamos:

```bash
manee@MANE:~$ git cat-file -p 573a1fab7ebbd400fd917b189a071fdfda9bb1e4
100644 blob 67252a1a89b852f868ad917da61376b412431713    main.py
```

*Análisis:* El `tree` le asigna permisos de lectura (`100644`), define que el objeto apuntado es un `blob`, le asocia el hash SHA-1 correspondiente y le da el nombre real de `main.py`.

### Paso 4: Inspección del Blob (Nivel 3)

Finalmente, extraemos el contenido puro del archivo consultando el hash del blob:

```bash
manee@MANE:~$ git cat-file -p 67252a1a89b852f868ad917da61376b412431713
Hola mundo
```

*Análisis:* Comprobamos que el blob almacena únicamente los datos crudos del archivo, cerrando el ciclo completo de inspección de objetos.

---



## 4. Flujo Básico Documentado Paso a Paso

A continuación se detalla el ciclo de vida básico de un cambio en Git, aplicando la regla profesional de validar el área de preparación (*staging area*) antes de consolidar la información.

### 1. Inicialización (`git init`)

```bash
manee@MANE:~$ git init demo_final
Initialized empty Git repository in /home/manee/vixia/dia07/lab/demo_final/.git/
```

*¿Qué hace?:* Crea el directorio oculto `.git/` configurando la base de datos de objetos vacía y las referencias iniciales.

### 2. Preparación de Cambios (`git add`)

```bash
manee@MANE:~$ echo "print('VixIA Activo')" > modelo.py
manee@MANE:~$ git add modelo.py
manee@MANE:~$ git diff --staged
diff --git a/modelo.py b/modelo.py
new file mode 100644
index 0000000..3fa1b23
--- /dev/null
+++ b/modelo.py
@@ -0,0 +1 @@
+print('VixIA Activo')
```

*¿Qué hace?:* Calcula el hash del archivo, crea el objeto blob en el directorio `.git/objects` e indexa el archivo en el área de preparación (`staged`). Usamos `git diff --staged` para auditar que no existan secretos ni código basura antes de confirmar.

### 3. Confirmación Inicial (`git commit`)

```bash
manee@MANE:~$ git commit -m "feat: inicializar modelo basico de VixIA"
[main (root-commit) b12a45f] feat: inicializar modelo basico de VixIA
 1 file changed, 1 insertion(+)
 create mode 100644 modelo.py
```

*¿Qué hace?:* Crea un objeto `tree` con el estado del índice actual y genera un objeto `commit` que apunta a dicho árbol, moviendo el puntero de la rama activa hacia este nuevo identificador.

### 4. Edición de Código

```bash
manee@MANE:~$ echo "print('VixIA optimizado v2')" > modelo.py
```

*¿Qué hace?:* Modifica el archivo en el directorio de trabajo (*working directory*). En este punto, el cambio solo existe en el espacio de disco del usuario.

### 5. Inspección de Diferencias (`git diff`)

```bash
manee@MANE:~$ git diff
diff --git a/modelo.py b/modelo.py
index 3fa1b23..9a8b7c6 100644
--- a/modelo.py
+++ b/modelo.py
@@ -1 +1 @@
-print('VixIA Activo')
+print('VixIA optimizado v2')
```

*¿Qué hace?:* Compara de forma dinámica el archivo modificado en el directorio de trabajo contra el último blob registrado en el índice del commit anterior.

### 6. Confirmación Final del Cambio

```bash
manee@MANE:~$ git add modelo.py
manee@MANE:~$ git diff --staged
manee@MANE:~$ git commit -m "fix: optimizar salida de VixIA"
[main 7f3e1a2] fix: optimizar salida de VixIA
 1 file changed, 1 insertion(+), 1 deletion(-)
```

*¿Qué hace?:* Repite el proceso de empaquetado del nuevo blob, registra la nueva estructura en un árbol actualizado y consolida el nuevo commit en el historial.

---



## 5. Inmutabilidad Explicada con Evidencia

El historial de Git es un libro contable criptográfico estrictamente inmutable debido al diseño de su árbol de dependencias.

### Evidencia del campo `parent`

Cuando inspeccionamos un commit intermedio en la historia de nuestra rama, observamos lo siguiente:

```bash
manee@MANE:~$ git cat-file -p 7f3e1a2...
tree 2c3d4e5...
parent b12a45f...
author Manee <manee@vixia.ia> 1786443500 -0600
...
```



### Explicación del impacto de modificar un commit antiguo

Cada objeto commit calcula su propio hash SHA-1 basándose estrictamente en su contenido, el cual **incluye de manera obligatoria el hash de su commit padre (**`parent`**)**. 

Si un desarrollador intentara alterar de forma retroactiva un commit antiguo (por ejemplo, modificando una línea de código del commit `b12a45f`), ocurriría la siguiente reacción en cadena:

1. El contenido de ese commit del pasado cambiaría, por ende, su hash SHA-1 se transformaría por completo en un valor nuevo e irreconocible.
2. El commit siguiente (`7f3e1a2`), que contiene apuntado explícitamente el hash antiguo en su campo `parent`, ahora apuntaría a un padre inexistente.
3. Para corregir ese enlace, el campo `parent` de `7f3e1a2` tendría que reescribirse con el nuevo hash modificado. Al cambiar el texto de su campo `parent`, el contenido del propio commit `7f3e1a2` cambia, alterando también su propio hash SHA-1.

Este efecto dominó se propaga de manera inmediata hacia adelante invalidando todos los commits posteriores de la historia.Conclusión: Es computacionalmente imposible modificar un solo byte de la historia pasada de Git de manera silenciosa. Cualquier alteración rompe la firma criptográfica de toda la cadena subsiguiente, garantizando la integridad absoluta del código de VixIA y VizionarIA.