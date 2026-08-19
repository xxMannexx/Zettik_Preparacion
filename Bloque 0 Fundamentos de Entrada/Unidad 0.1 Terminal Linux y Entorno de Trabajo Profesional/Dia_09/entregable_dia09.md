# Entregable Día 09 — Git III: Remotos, Colaboración y Herramientas Profesionales
## Objetivo

En este día ya no estamos trabajando solamente con la historia local de Git. Ahora estamos trabajando con varios repositorios que tienen sus propios objetos y sus propias referencias y que en algún momento necesitan sincronizarse.

A final de cuentas, sincronizar no significa “mandar archivos” nada más. Se transfieren **objetos** —commits, trees y blobs— y después se actualizan **referencias** para saber a qué commits apunta cada rama.

La intención de este entregable es demostrar mecánicamente que entiendo cómo se mueve la historia entre dos repositorios, qué pasa cuando existe divergencia, por qué `.gitignore` no puede modificar el pasado, cómo localizar un defecto utilizando búsqueda binaria y cómo marcar una versión con un tag real de Git.

> Si mi Git utiliza `master` como rama principal en lugar de `main`, sustituyo `main` por `master`. La mecánica no cambia.

---

# 1. Sincronización entre clones

## Preparación del remoto

Primero creo un repositorio **bare**. Este repositorio no tiene un directorio de trabajo normal; su trabajo es almacenar objetos y referencias y servir como punto de sincronización.

```
mkdir -p ~/ZETTIK/VixIA/Dia_09/lab
cd ~/ZETTIK/VixIA/Dia_09/lab

rm -rf remoto.git clonA clonB

git init --bare remoto.git

```

Ahora creo el primer clon:

```
git clone remoto.git clonA
cd clonA

```

Creo el primer archivo:

```
echo "estado inicial" > app.txt
git add app.txt
git diff --staged
git commit -m "feat(sync): crea estado inicial"

```

Antes de publicar revisé el staging con `git diff --staged`, porque quiero confirmar exactamente lo que voy a mandar al commit y no cualquier cosa que esté en mi working directory.

Publico la rama:

```
git push -u origin main

```

`origin` no significa GitHub. Es simplemente el nombre convencional que Git le dio al repositorio remoto.

`main` es mi rama local.

`origin/main` es la referencia local donde Git recuerda dónde estaba `main` en el remoto la última vez que hablamos con él.

Ahora creo el segundo clon:

```
cd ..
git clone remoto.git clonB

```

Tenemos entonces:

```
remoto.git
   ↑
   ├── clonA
   └── clonB

```

Los dos clones son repositorios completos.

## Propagación de un nuevo commit

Desde `clonA` hago un cambio nuevo:

```
cd clonA

echo "cambio publicado desde A" > sincronizacion.txt
git add sincronizacion.txt
git diff --staged
git commit -m "feat(sync): publica cambio desde clon A"

git push origin main

```

En este punto el remoto avanzó.

`clonB` todavía tiene en su rama local la historia que conocía antes.

Entro a B:

```
cd ../clonB

```

Traigo e integro lo publicado por A:

```
git pull origin main

```

Compruebo que el archivo llegó:

```
cat sincronizacion.txt
git log --oneline --graph --decorate

```

### Evidencia

Pegar aquí la salida real:

```
[PEGAR SALIDA DE cat sincronizacion.txt]

[PEGAR SALIDA DE git log --oneline --graph --decorate]

```

## Explicación

Lo que realmente pasó fue:

```
clonA
  commit nuevo
      │
      │ push
      ▼
remoto
      │
      │ pull
      ▼
clonB

```

No estamos moviendo una carpeta de una computadora a otra.

Git manda los **objetos que faltan** y actualiza las referencias correspondientes.

Eso es precisamente por lo que Git sigue siendo distribuido: A, B y el remoto tienen cada uno su propio repositorio.

---

# 2. Divergencia y rechazo non-fast-forward

Ahora voy a provocar exactamente el problema que pasa cuando dos personas trabajan sin tener todavía el trabajo de la otra.

Primero B hace un cambio:

```
cd ~/ZETTIK/VixIA/Dia_09/lab/clonB

echo "aporte realizado por B" > b.txt
git add b.txt
git diff --staged
git commit -m "feat(sync): añade aporte de B"

git push origin main

```

El remoto ahora conoce el commit de B.

Mientras tanto A todavía no lo ha traído.

En A hago otro cambio diferente:

```
cd ../clonA

echo "aporte realizado por A" > a.txt
git add a.txt
git diff --staged
git commit -m "feat(sync): añade aporte de A"

```

En este momento la historia conceptualmente está así:

```
                commit A
               /
ancestro común
               \
                commit B  ← origin/main

```

Los dos avanzaron desde el mismo ancestro.

Eso es **divergencia**.

Ahora A intenta publicar:

```
git push origin main

```

### Evidencia del rechazo

Pegar aquí la salida real del comando:

```
[PEGAR MENSAJE rejected / non-fast-forward]

```

## ¿Por qué Git lo rechaza?

Porque este push **no sería fast-forward**.

El remoto ya tiene el commit de B.

Mi commit A no desciende del commit B.

Si Git simplemente moviera la referencia del remoto hacia A, estaría dejando fuera la historia que B ya publicó.

A final de cuentas Git está diciendo:

> “No puedo mover esta referencia hacia tu commit porque hay historia publicada que tú todavía no tienes.”

No es un error absurdo de Git. Es una protección para no borrar trabajo ajeno.

## Resolución

Primero integro el estado real del remoto:

```
git pull origin main

```

Como A y B cambiaron archivos distintos, Git puede hacer la integración sin conflicto.

Como ambos lados habían avanzado, esta integración puede generar un **merge de tres vías**.

Reviso el grafo:

```
git log --oneline --graph --all --decorate

```

Ahora publico:

```
git push origin main

```

Esta vez sí puede realizarse el avance porque mi nueva historia ya contiene lo que estaba publicado en el remoto.

### Evidencia final

```
[PEGAR GRAFO DESPUÉS DEL PULL]

[PEGAR SALIDA DEL PUSH EXITOSO]

```

## Explicación

El flujo fue:

```
B hace commit
      ↓
B hace push
      ↓
remoto avanza

A hace commit sin conocer B
      ↓
A intenta push
      ↓
RECHAZADO: non-fast-forward

A hace pull
      ↓
integra la historia de B
      ↓
A hace push
      ↓
PUBLICACIÓN ACEPTADA

```

Para mí la regla queda así:

> Si el remoto tiene commits que yo no tengo, no puedo publicar encima como si no existieran. Primero tengo que integrar esa historia y después publicar.

---

# 3. Límite de `.gitignore`

Aquí quiero demostrar algo importante: `.gitignore` **no modifica el pasado**.

Voy a utilizar un archivo normal de prueba, no un secreto real.

Creo un repositorio independiente:

```
cd ~/ZETTIK/VixIA/Dia_09/lab
mkdir -p gitignore-demo
cd gitignore-demo
git init

```

Creo un archivo:

```
echo "configuracion_de_prueba=123" > config.local

```

Lo agrego y confirmo:

```
git add config.local
git diff --staged
git commit -m "chore(ignore): rastrea archivo de configuracion de prueba"

```

En este momento `config.local` ya está **versionado**.

Ahora intento ignorarlo:

```
echo "config.local" > .gitignore

```

Agrego el `.gitignore`:

```
git add .gitignore
git diff --staged
git commit -m "chore(ignore): añade regla para config.local"

```

Compruebo qué archivos siguen siendo rastreados:

```
git ls-files

```

### Evidencia

```
[PEGAR SALIDA DONDE config.local SIGUE APARECIENDO]

```

Aunque ya está dentro de `.gitignore`, Git sigue rastreándolo.

## ¿Por qué?

Porque `.gitignore` funciona sobre archivos **no rastreados**.

Pero `config.local` ya fue convertido en parte de la historia.

Ya existió un blob referenciado por un tree y después por un commit.

Por la **inmutabilidad de objetos**, añadir una línea a `.gitignore` no puede viajar hacia atrás y editar commits que ya existen.

No es:

```
.gitignore → borra el pasado

```

Es:

```
.gitignore → evita comenzar a rastrear ciertas cosas en adelante

```

## Dejar de rastrearlo

Para retirarlo del seguimiento actual sin eliminarlo físicamente de mi disco utilizo:

```
git rm --cached config.local

```

Reviso:

```
git diff --staged

```

Confirmo:

```
git commit -m "chore(ignore): deja de rastrear config.local"

```

Compruebo:

```
git ls-files

```

Ahora ya no debe aparecer como rastreado.

Pero puedo demostrar que existió en la historia anterior:

```
git log --oneline

```

### Evidencia

```
[PEGAR SALIDA DE git ls-files ANTES]

[PEGAR SALIDA DE git ls-files DESPUÉS]

[PEGAR git log --oneline]

```

## Implicación para secretos

Esto es especialmente importante con una API key.

Si confirmo una clave secreta y después escribo:

```
.env

```

en `.gitignore`, **la clave no desapareció**.

Hay commits anteriores donde el secreto continúa almacenado.

Entonces ese secreto debe considerarse comprometido.

Por eso `.gitignore` debe existir **antes** de comenzar a versionar información sensible.

En este entregable no se confirmó ningún secreto real.

---

# 4. Localización de una regresión con `git bisect`

Ahora voy a provocar un defecto a propósito para localizarlo utilizando búsqueda binaria.

Creo otro repositorio:

```
cd ~/ZETTIK/VixIA/Dia_09/lab
mkdir -p bisect-demo
cd bisect-demo
git init

```

## Commit 1 — correcto

```
echo "resultado=correcto" > estado.txt
git add estado.txt
git diff --staged
git commit -m "feat(test): establece estado correcto inicial"

```

Guardo mentalmente que este estado funciona.

## Commit 2 — todavía correcto

```
echo "paso 2" > cambio2.txt
git add cambio2.txt
git diff --staged
git commit -m "feat(test): añade cambio correcto dos"

```

## Commit 3 — todavía correcto

```
echo "paso 3" > cambio3.txt
git add cambio3.txt
git diff --staged
git commit -m "feat(test): añade cambio correcto tres"

```

## Commit 4 — todavía correcto

```
echo "paso 4" > cambio4.txt
git add cambio4.txt
git diff --staged
git commit -m "feat(test): añade cambio correcto cuatro"

```

## Commit 5 — aquí introduzco el defecto

```
echo "resultado=DEFECTUOSO" > estado.txt
git add estado.txt
git diff --staged
git commit -m "fix(test): introduce regresion deliberada para bisect"

```

El mensaje solamente documenta el laboratorio; el defecto se está provocando intencionalmente.

## Commits posteriores

```
echo "paso 6" > cambio6.txt
git add cambio6.txt
git diff --staged
git commit -m "feat(test): añade cambio posterior seis"

echo "paso 7" > cambio7.txt
git add cambio7.txt
git diff --staged
git commit -m "feat(test): añade cambio posterior siete"

echo "paso 8" > cambio8.txt
git add cambio8.txt
git diff --staged
git commit -m "feat(test): añade cambio posterior ocho"

```

Veo la historia:

```
git log --oneline

```

Tenemos ocho commits.

Sabemos:

```
v1 = good
v8 = bad

```

Inicio `bisect`:

```
git bisect start

```

Marco el actual como defectuoso:

```
git bisect bad

```

Marco el commit antiguo correcto:

```
git bisect good $(git rev-parse HEAD~7)

```

Git automáticamente se coloca aproximadamente a la mitad.

Ahora compruebo:

```
cat estado.txt

```

Si dice:

```
resultado=correcto

```

marco:

```
git bisect good

```

Si dice:

```
resultado=DEFECTUOSO

```

marco:

```
git bisect bad

```

Repito hasta que Git indique:

```
<hash> is the first bad commit

```

### Evidencia

```
[PEGAR AQUÍ LOS PASOS REALES DE BISECT]

[PEGAR AQUÍ "is the first bad commit"]

```

Al terminar:

```
git bisect reset

```

## ¿Por qué funciona tan rápido?

Si tuviera que revisar uno por uno:

```
N commits → hasta N pruebas

```

Con `bisect`:

```
N
N/2
N/4
N/8
...

```

Cada prueba elimina aproximadamente la mitad.

Por eso el coste es:

```
O(log₂ N)

```

Para 1024 commits:

```
log₂(1024) = 10

```

Entonces puedo reducir un problema de hasta 1024 pruebas a aproximadamente 10.

A final de cuentas es **divide y vencerás aplicado a la historia de Git**.

El supuesto importante es que pueda clasificar de manera fiable cada versión como `good` o `bad`, y que la regresión se comporte de manera suficientemente monótona: antes del defecto funciona y después del defecto permanece defectuosa.

---

# 5. Conventional Commits y versión marcada con tag anotado

Primero voy a demostrar tres mensajes estructurados.

Supongamos que la versión actual del proyecto es:

```
1.4.2

```

## Corrección — patch

```
echo "correccion de volumen" > audio.txt
git add audio.txt
git diff --staged
git commit -m "fix(audio): corrige volumen de salida"

```

Un `fix` aumenta el parche:

```
1.4.2 → 1.4.3

```

## Nueva funcionalidad — minor

```
echo "seguimiento visual" > vision.txt
git add vision.txt
git diff --staged
git commit -m "feat(vision): añade seguimiento de objetivos"

```

Un `feat` aumenta la versión menor:

```
1.4.3 → 1.5.0

```

## Breaking change — major

```
echo "nuevo formato de API" > api.txt
git add api.txt
git diff --staged
git commit -m "feat(api)!: cambia formato de respuesta"

```

El `!` indica un **breaking change**.

Un breaking change es:

> Un cambio que hace que código que antes funcionaba deje de funcionar sin realizar ajustes.

Por ello aumenta la versión mayor:

```
1.5.0 → 2.0.0

```

La estructura de Conventional Commits permite que una máquina entienda el propósito de cada commit.

Así puede generar automáticamente:

- un changelog;
- el siguiente número de versión semántica.

## Crear el tag de versión

Ahora marco el commit correspondiente a esta release:

```
git tag -a v2.0.0 -m "Version 2.0.0: nuevo formato de API"

```

Compruebo el tipo:

```
git cat-file -t v2.0.0

```

La salida esperada es:

```
tag

```

### Evidencia

```
[PEGAR SALIDA REAL DE git cat-file -t v2.0.0]

```

Veo sus metadatos:

```
git show v2.0.0 | head -8

```

### Evidencia de metadatos

```
[PEGAR SALIDA REAL]

```

## Explicación

Aquí está la diferencia importante:

Un **tag ligero** es prácticamente una referencia fija hacia un commit.

Un **tag anotado** sí crea uno de los cuatro objetos de Git:

```
blob
tree
commit
tag

```

El tag anotado puede contener:

- commit al que apunta;
- tagger;
- autor;
- fecha;
- mensaje;
- y opcionalmente información de firma.

Para una release utilizo un tag anotado porque quiero **trazabilidad**.

No porque la versión sea mayor o menor.

Incluso una release `v1.0.1` puede y normalmente debe marcarse con un tag anotado.

La diferencia con una rama es que:

```
rama → se mueve conforme aparecen nuevos commits

tag → permanece fijo sobre el commit marcado

```

---

# Conclusión

Después de este día mi modelo de Git queda mucho más completo.

Hasta el Día 8 yo podía pensar principalmente en:

```
branch
  ↓
commit
  ↓
tree
  ↓
blob / subtree

```

Ahora además tengo repositorios separados que necesitan ponerse de acuerdo:

```
clon A
   ↕
remoto
   ↕
clon B

```

La sincronización mueve **objetos y referencias**.

`fetch` me permite conocer el estado nuevo del remoto sin meter esos cambios directamente a mi rama.

`pull` hace `fetch` y después integra, por lo que sí puede provocar un merge, un rebase o incluso un conflicto.

`push` intenta publicar mi historia, pero Git exige que pueda avanzar el remoto mediante fast-forward; si hay divergencia me obliga a integrar primero para no destruir trabajo ajeno.

`.gitignore` es preventivo. No viaja hacia atrás y borra objetos que ya fueron versionados, precisamente porque Git mantiene objetos inmutables.

`git bisect` me permite localizar una regresión dividiendo la historia aproximadamente a la mitad en cada prueba, reduciendo el coste desde `O(N)` hasta `O(log N)`.

Conventional Commits convierte mensajes de texto en información que una máquina puede procesar para generar changelogs y versionado semántico.

Finalmente, un tag anotado me permite dejar una marca fija, documentada y verificable sobre una versión concreta.

A final de cuentas, todas estas herramientas siguen respetando la misma idea que apareció desde el Día 7:

> Git no funciona modificando arbitrariamente la historia. Funciona creando objetos y moviendo referencias de manera controlada.
