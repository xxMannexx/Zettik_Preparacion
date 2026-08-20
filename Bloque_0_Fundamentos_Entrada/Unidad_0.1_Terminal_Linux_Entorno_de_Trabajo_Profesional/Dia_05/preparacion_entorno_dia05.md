# Crear un árbol de prueba para find
mkdir -p proyecto/{src,data,logs,config}
touch proyecto/src/main.py proyecto/src/utils.py proyecto/src/test_main.py
touch proyecto/data/train.csv proyecto/data/val.csv
touch proyecto/config/settings.env
echo secreto > proyecto/config/api.key
chmod 777 proyecto/config/api.key   # un permiso peligroso a propósito, para find -perm
 
# Crear un log de prueba para grep/regex
cat > app.log << 'EOF'
2026-01-15 08:30:12 INFO  Sistema iniciado v2.3.1
2026-01-15 08:30:45 WARN  Memoria al 82%
2026-01-15 08:31:02 ERROR Timeout en cámara IP 192.168.1.45
2026-01-15 08:31:10 INFO  Reintento conexión user=ana
2026-01-15 08:31:55 ERROR Fallo de lectura en /dev/video0
2026-01-15 08:32:03 INFO  Detección: persona (conf=0.94)
2026-01-15 08:32:30 WARN  Memoria al 88%
2026-01-15 08:33:01 INFO  Detección: coche (conf=0.71)
EOF
cat app.log | head -3
# Esperado: las primeras 3 líneas del log

