## 1.	Árbol de procesos: la salida de ps -ef --forest (o pstree -p $$) de tu sesión, con una explicación del parentesco PID/PPID y dónde está init (PID 1).

    El parentezco PID deriva un poco de lo que hemos visto como FHS todo nace de un padre generando un arbol completo de procesos y jerarquias todo nace desde INIT(PID 1) y de ahi derivan todos siendo hijos de el PPID de su proceso: 

    UID          PID    PPID  C STIME TTY          TIME CMD
    root           1       0  0 14:39 ?        00:00:01 /sbin/init
    root           2       1  0 14:39 hvc0     00:00:00 /init
    root           6       2  0 14:39 hvc0     00:00:00  \_ plan9 --control-socket 7 --log-level 4 --server-fd 8 --pipe-fd 10 --log-truncate
    root         340       2  0 14:39 ?        00:00:00  \_ login -- manee
    manee        413     340  0 14:39 pts/1    00:00:00  |   \_ -bash
    root         610       2  0 14:48 ?        00:00:00  \_ /init
    root         611     610  0 14:48 ?        00:00:00  |   \_ /init
    manee        617     611  0 14:48 pts/2    00:00:01  |       \_ -bash
    manee       5225     617  0 17:50 pts/2    00:00:00  |           \_ ps -ef --forest
    root        5125       2  0 17:45 ?        00:00:00  \_ /init
    root        5126    5125  0 17:45 ?        00:00:00      \_ /init
    manee       5133    5126  0 17:45 pts/0    00:00:00          \_ /tmp/tmp.1Xb3NPlFLr/ijent grpc-server --self-delete-on-exit
    root          46       1  0 14:39 ?        00:00:00 /usr/lib/systemd/systemd-journald
    systemd+      81       1  0 14:39 ?        00:00:00 /usr/lib/systemd/systemd-resolved
    root          88       1  0 14:39 ?        00:00:02 /usr/lib/systemd/systemd-udevd
    root         158       1  0 14:39 ?        00:00:00 /bin/sh /usr/lib/systemd/scripts/chronyd-starter.sh -n -F 1
    _chrony      273     158  0 14:39 ?        00:00:00  \_ /usr/sbin/chronyd -n -F 1 -x
    _chrony      274     273  0 14:39 ?        00:00:00      \_ /usr/sbin/chronyd -n -F 1 -x
    root         159       1  0 14:39 ?        00:00:00 /usr/sbin/cron -f -P
    message+     160       1  0 14:39 ?        00:00:00 @dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
    root         164       1  0 14:39 ?        00:00:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
    root         178       1  0 14:39 ?        00:00:00 /usr/lib/systemd/systemd-logind
    syslog       213       1  0 14:39 ?        00:00:00 /usr/sbin/rsyslogd -n -iNONE
    root         281       1  0 14:39 ?        00:00:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
    root         283       1  0 14:39 tty1     00:00:00 /usr/sbin/agetty --noreset --noclear --issue-file=/etc/issue:/etc/issue.d:/run/issue.d:/usr/lib/issue.d - linux
    manee        386       1  0 14:39 ?        00:00:00 /usr/lib/systemd/systemd --user
    manee        388     386  0 14:39 ?        00:00:00  \_ (sd-pam)
    polkitd     1427       1  0 15:09 ?        00:00:00 /usr/lib/polkit-1/polkitd --no-debug --log-level=notice
    root        5169       1  0 17:46 ?        00:00:00 /usr/libexec/wsl-pro-service

## 2.	Ciclo de vida con señales: la demostración de lanzar un proceso, suspenderlo (SIGSTOP → estado T), reanudarlo (SIGCONT → S) y terminarlo (SIGTERM), con el ps de cada estado.

" #!/bin/bash
PID=$1

for i in $(seq 0 1 10); do
ps -o pid,stat,cmd,%cpu,%mem -p $PID >> monitor_estados.txt
sleep 1
done "

Con este codigo generamos el m onitor, con el siguiente mandamos una signal:

"kill -INT $PID"

Y da un resultado similar a esto: 

    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 S    sleep 1000                   0.0  0.1
    PID STAT CMD                         %CPU %MEM
   4959 T    sleep 1000                   0.0  0.1

## 3.	TERM vs KILL: una explicación, con evidencia, de la diferencia entre terminación limpia y forzada, y por qué -9 puede corromper datos.

La terminacion limpia es la primer forma de terminar un proceso para que todo se termine de manera ordenada y sin dejar basura sobre lo que sea que actuaba, el kill se usa una vez hecha term no hya funcionado y sea muy necesario termniar el proceso, la mejor secuencia es la siguiente: 

PID=12345
kill -TERM $PID                              # 1) petición limpia
sleep 3                                       # 2) margen para limpiar
if kill -0 $PID 2>/dev/null; then             # 3) ¿sigue vivo?
  echo "No respondió; forzando."; kill -9 $PID
else
  echo "Terminó limpiamente."
fi

## 4.	nice en acción: dos procesos con niceness distinta (0 y 19), mostrando la columna NI, con tu explicación de cuándo afecta la prioridad.

Prioridad con nice: lanzar dos procesos con niceness distinta
nice -n 0  sleep 300 & A=$!
nice -n 19 sleep 300 & B=$!

=== Niceness: A debe ser 0, B debe ser 19 ===
    PID  NI CMD
   1204   0 sleep 300
    PID  NI CMD
   1216  19 sleep 300

## 5.	Persistencia con nohup: un proceso lanzado con nohup que demuestres inmune a SIGHUP (enviándoselo y comprobando que sobrevive), con el patrón completo nohup.

nohup: un proceso inmune a SIGHUP (evidencia de que ignora la señal)
nohup sleep 300 > /dev/null 2>&1 &
NH=$!
{
  echo "=== nohup: el proceso ignora SIGHUP ==="
  echo "PID nohup: $NH"
  kill -HUP $NH; sleep 0.3
  ps -o pid,stat,cmd -p $NH >/dev/null 2>&1 && echo "Sigue vivo tras SIGHUP (correcto)" || echo "Murió (inesperado)"
} > evidencia_nohup.txt
kill $NH 2>/dev/null     # limpieza final

=== nohup: el proceso ignora SIGHUP ===
PID nohup: 1780
Sigue vivo tras SIGHUP (correcto)
