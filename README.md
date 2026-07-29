# Zettik · Preparación

> Repositorio de evidencia académica y técnica de la **Segunda Universidad VixIA**.

Este repositorio documenta el avance diario de un programa personal de formación intensiva orientado a ingeniería de sistemas inteligentes, inteligencia artificial, software, sistemas Linux y desarrollo de **V********A**.

No funciona únicamente como una colección de apuntes. Cada carpeta conserva ejercicios, laboratorios, explicaciones propias, comandos ejecutados y entregables que permiten comprobar el aprendizaje mediante evidencia reproducible.

---

## Propósito

El proyecto **Segunda Universidad VixIA** busca construir, de manera progresiva, un perfil técnico capaz de:

- comprender los mecanismos internos de los sistemas informáticos;
- diseñar y programar software con fundamentos sólidos;
- trabajar con inteligencia artificial, visión por computadora y sistemas embebidos;
- desarrollar investigación técnica basada en evidencia;
- transferir el aprendizaje al proyecto **VizionarIA**;
- documentar decisiones, errores, pruebas y resultados de forma profesional.

Este repositorio corresponde a la etapa de **preparación y fundamentos**. No representa por sí mismo una versión funcional o validada de V********A.

---

## Metodología de estudio

Cada día de formación sigue un ciclo de aprendizaje activo:

1. **Diagnóstico de entrada** para detectar lagunas.
2. **Estudio conceptual** del mecanismo, no solo de la sintaxis.
3. **Predicción de resultados** antes de ejecutar comandos.
4. **Práctica en terminal o código**.
5. **Análisis de errores y outputs reales**.
6. **Entregable diario** con evidencia.
7. **Comprobación de dominio** mediante explicación y aplicación.
8. **Registro de límites de evidencia**, evitando convertir una prueba pequeña en una afirmación de producción.

La prioridad es poder explicar qué ocurre, predecir el comportamiento, ejecutar correctamente y defender las decisiones tomadas.

---

## Estado actual

**Bloque:** B0 — Fundamentos de Entrada y Entorno  
**Unidad:** 0.1 — Terminal Linux y Entorno de Trabajo Profesional  
**Avance documentado:** Días 1–4

| Día | Tema principal | Evidencia destacada |
|---|---|---|
| [Día 01](./Dia_01/) | Shell, FHS, rutas y modelo de procesos | Mapa del sistema de archivos, análisis de `ls -li`, rutas absolutas/relativas y relación `fork`/ejecución |
| [Día 02](./Dia_02/) | Permisos, `umask` y enlaces | Tabla octal, enlaces duros y simbólicos, diagnóstico de permisos y estructura segura de archivos |
| [Día 03](./Dia_03/) | Redirecciones, flujos estándar y pipelines | `stdin`/`stdout`/`stderr`, `>`/`>>`, separación de errores, pipelines y `tee` |
| [Día 04](./Dia_04/) | Procesos, señales y job control | Árbol PID/PPID, estados, `SIGTERM`/`SIGKILL`, `nice` y persistencia con `nohup` |

---

## Estructura del repositorio

```text
Zettik_Preparacion/
├── Dia_01/
│   ├── proyectos/
│   ├── desafio_01.md
│   ├── entregable_dia01.md
│   └── evidencias de terminal
├── Dia_02/
│   ├── datasets/
│   ├── exp1/
│   ├── exp2/
│   ├── lab/
│   └── entregable_dia02.md
├── Dia_03/
│   └── entregable_dia03.md
└── Dia_04/
    ├── lab/
    └── entregable_dia04.md
```

La estructura crecerá siguiendo el orden oficial definido en la Tabla Maestra del programa.

---

## Tipos de evidencia

Los archivos pueden contener distintas clases de evidencia. Deben interpretarse por separado:

- **Explicación conceptual:** demuestra comprensión teórica.
- **Ejemplo:** ilustra un mecanismo, pero no constituye validación general.
- **Ejecución host:** comando o programa ejecutado en el entorno local.
- **Test:** comprueba un contrato específico bajo condiciones definidas.
- **Benchmark:** requiere hardware, metodología y métricas documentadas.
- **Integración:** demuestra comunicación entre componentes.
- **Validación física:** requiere evidencia obtenida con hardware real.
- **Claim de producto:** exige un nivel de validación mucho mayor.

Un test unitario o una ejecución local no prueban automáticamente seguridad, rendimiento, producción, tiempo real o funcionamiento en hardware final.

---

## Requisitos actuales

Para reproducir la etapa documentada hasta ahora:

- Linux o un entorno compatible, como WSL;
- Bash;
- utilidades GNU/POSIX comunes;
- Git;
- permisos para crear y modificar archivos dentro del directorio de trabajo.

Algunas prácticas utilizan comandos como:

```bash
ps
pgrep
top
nice
renice
kill
nohup
grep
sort
uniq
tee
find
```

---

## Uso del repositorio

Clonar el proyecto:

```bash
git clone https://github.com/xxMannexx/Zettik_Preparacion.git
cd Zettik_Preparacion
```

Explorar un día:

```bash
cd Dia_04
find . -maxdepth 2 -type f | sort
```

Leer el entregable correspondiente:

```bash
less entregable_dia04.md
```

Los comandos incluidos en los entregables son evidencia educativa. Deben leerse antes de ejecutarse, especialmente cuando utilicen `kill`, `chmod`, `rm`, redirecciones destructivas o cambios de prioridad.

---

## Convenciones recomendadas

### Carpetas

```text
Dia_XX/
├── lab/                  # Prácticas ejecutables
├── proyectos/            # Mini-proyectos, cuando correspondan
├── evidencia/            # Logs, outputs o capturas textuales
├── notas.md               # Notas propias opcionales
└── entregable_diaXX.md    # Evidencia principal del día
```

### Commits

Se recomienda utilizar mensajes claros y consistentes:

```text
docs: completar entregable del día 04
feat: agregar monitor de estados de procesos
fix: corregir redirección de stderr
test: validar transición SIGSTOP a SIGCONT
refactor: reorganizar laboratorio del día 03
```

---

## Seguridad

Nunca deben publicarse:

- contraseñas;
- tokens;
- claves de API;
- llaves SSH;
- archivos `.env`;
- credenciales de servicios;
- datos personales sensibles.

Configuración recomendada para `.gitignore`:

```gitignore
.env
.env.*
!.env.example
*.key
*.pem
*.log
nohup.out
__pycache__/
.venv/
venv/
```

Para documentar variables necesarias, debe utilizarse un archivo seguro como:

```text
.env.example
```

con valores ficticios y sin secretos reales.

---

## Próximos pasos

- Completar la Unidad 0.1 de terminal Linux.
- Mantener un entregable verificable por cada día.
- Normalizar la estructura de las carpetas.
- Añadir evaluaciones de cierre por unidad.
- Incorporar tests y scripts reproducibles conforme avance el programa.
- Relacionar cada práctica con aplicaciones legítimas de V********A sin exagerar la evidencia obtenida.

---

## Autor

**Mane — xxMannexx**

Estudiante y creador del programa personal **Segunda Universidad VixIA**, enfocado en construir fundamentos técnicos para investigación, sistemas inteligentes y el desarrollo progresivo de V********A.

---

## Estado del proyecto

🚧 **En desarrollo activo**

El contenido refleja un proceso de aprendizaje progresivo. Los entregables pueden revisarse, corregirse o ampliarse cuando aparezca nueva evidencia o una comprensión más precisa.
