
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
