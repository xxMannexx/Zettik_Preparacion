## Construccion del repositorio completo desde 0

# 1. CREAR EL DIRECTORIO PARA EL REPOSITORIO

```
DOTREPO=~/vixia/dia10/vixia-dotfiles
rm -rf "$DOTREPO" && mkdir -p "$DOTREPO" && cd "$DOTREPO"
git init -q
mkdir -p backups
```

# 2. Escribir los modulos de configuracion

## 2.1 ALIAS PERSONALES

```
cat > aliases << 'EOF'
# Alias Personales
alias ll='ls -la'
alias gs='git status'
alias gl='git log --oneline --graph'
alias ..='cd ..'
EOF

```

## 2.2 CONFIGURACION DE VARIABLES DE ENTORNO

```
cat > exports << 'EOF'

# Variables de entorno de VixIA (no sensibles)

export EDITOR=vim
export VIXIA_HOME="$HOME/vixia"
export PATH="$HOME/bin:$PATH"

EOF
```



## 2.3 Funciones del shell de VixIA

```
cat > functions << 'EOF'
# Funciones del shell de VixIA
mkcd() { mkdir -p "$1" && cd "$1"; }          # crear directorio y entrar
gcommit() { git add -A && git commit -m "$1"; } # add y commit con un mensaje
EOF
```



## 2.4 bashrc modular de ZETTIK — cargado vía enlace desde ~/.bashrc Y GITCONFIG para el repositorio

```
cat > bashrc << 'EOF'
# bashrc modular de ZETTIK — cargado vía enlace desde ~/.bashrc
DOTFILES="$HOME/.dotfiles"
for modulo in aliases exports functions; do
  [ -f "$DOTFILES/$modulo" ] && source "$DOTFILES/$modulo"
done
[ -f "$HOME/.secrets" ] && source "$HOME/.secrets"   # secretos locales, si existen
EOF
```

```
cat > gitconfig << 'EOF'
[user]
    name = Tu Nombre
    email = tu@correo.com
[init]
    defaultBranch = main
[alias]
    st = status
    lg = log --oneline --graph --all
EOF
```



## 2.5 Creacion de secretos y exclusiones  (.gitignore y secrets.example)

```
# Plantilla de secretos. Copie a ~/.secrets, rellene y proteja con chmod 600.
# NUNCA versione ~/.secrets (excluido por .gitignore).
export API_CAMARA="<su_clave_de_camara>"
export TOKEN_MODELO="<su_token_de_modelo>"
EOF
```

```
# --- Exclusiones ---
cat > .gitignore << 'EOF'
# Secretos locales (nunca versionar)
secrets
.secrets
# Respaldos generados por el instalador
backups/
EOF
```



# 3. CREACION DEL INSTALADOR IDEMPOTENTE

```
#!/bin/bash
set -e ## Esto es una validacion basica para que el script se detenga si ocurre algun error durante la ejecucion

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"   ## Esta variable guardara la ruta real del repositorio de configuraciones

TARGET="${DOTFILES_TARGET:-$HOME}"  ## Coloca como target de instalacion de configuraciones la carpeta personal HOME

mkdir -p "$DOTFILES_DIR/backups"  ## Crea una carpeta de respaldo para los archivos ya existentes que seran cambiados

crear_enlace() {
    local origen="$1" destino="$2" ## Inicializa las variables tanto de origen como de destino para generar los archivos y enlaces correspondientes

    if [ -e "$destino" ] && [ ! -L "$destino" ]; then
        mv "$destino" "$DOTFILES_DIR/backups/$(basename "$destino").$(date +%s)"
        echo ""$destino" ha sido respaldado en "$DOTFILES_DIR/backups""
    fi
    ln -sf "$origen" "$destino"
    echo "Se ha realizado correctamente el enlace: "$destino" -> "$origen""
}

## Creamos el directorio de dotfiles esperado por bashrc y enlazamos los modulos

mkdir -p "$TARGET/.dotfiles"
for modulo in exports aliases functions; do
    crear_enlace "$DOTFILES_DIR/$modulo" "$TARGET/.dotfiles/$modulo"
done

## Creo los enlaces para la configuracion de repo y el bashrc

crear_enlace "$DOTFILES_DIR/bashrc" "$TARGET/.bashrc"

crear_enlace "$DOTFILES_DIR/gitconfig" "$TARGET/.gitconfig"

## Crear el archivo de secretos desde la plantilla solo si no existe respetando idempotencia

if [ ! -e "$TARGET/.secrets" ]; then
    cp "$DOTFILES_DIR/secrets.example" "$TARGET/.secrets"
    chmod 600 "$TARGET/.secrets"
    echo "Se ha creado el archivo de secretos desde la plantilla: $TARGET/.secrets, rellenar con sus claves personales"
fi      
```

Es primordial darle permisos de lectura y escritura al usuario propietario

```
chmod +x install.sh
```
```



# 4. Creacion del README

```
cat > README.md << 'EOF'
# ZETTIK-dotfiles
 
Entorno de trabajo reproducible para ZETTIK / VizionarIA.
 
## Instalación
    git clone <url> ~/ZETTIK-dotfiles
    cd $_
    ./install.sh
 
El instalador crea enlaces simbólicos del directorio personal hacia este repositorio,
respaldando cualquier configuración previa, y crea ~/.secrets desde la plantilla.
Rellene ~/.secrets con sus valores reales (nunca se versiona).
EOF
```



# 5. VERSIONADO EN GIT

```
# --- Versionado ---
git add .
git status --short                 # verificar: no aparece ningún 'secrets' real
git commit -q -m "feat(dotfiles): entorno reproducible con instalador idempotente y separación de secretos"
git tag -a v1.0.0 -m "v1.0.0: configuración base reproducible de VixIA"
```

