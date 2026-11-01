#!/bin/bash
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
RUN=/srv/orkalinux-vm
MON="$RUN/monitor.sock"
QMP="$RUN/qmp.sock"
SHOTS="$SRC/out/screens"
mkdir -p "$RUN" "$SHOTS"

hmp() { printf '%s\n' "$1" | socat -t2 - "UNIX-CONNECT:$MON" >/dev/null; }
qmp() { printf '{"execute":"qmp_capabilities"}\n%s\n' "$@" | socat -t1 - "UNIX-CONNECT:$QMP" >/dev/null; }

key_for() {
	case "$1" in
		[a-z0-9]) echo "$1" ;;
		[A-Z]) echo "shift-$(echo "$1" | tr 'A-Z' 'a-z')" ;;
		' ') echo spc ;; '.') echo dot ;; ',') echo comma ;; '-') echo minus ;;
		'_') echo shift-minus ;; '/') echo slash ;; '@') echo shift-2 ;; '!') echo shift-1 ;;
		'|') echo shift-backslash ;; ';') echo semicolon ;; ':') echo shift-semicolon ;;
		'=') echo equal ;; '+') echo shift-equal ;; '"') echo shift-apostrophe ;; "'") echo apostrophe ;;
		'>') echo shift-dot ;; '<') echo shift-comma ;; '*') echo shift-8 ;; '$') echo shift-4 ;;
		'&') echo shift-7 ;; '(') echo shift-9 ;; ')') echo shift-0 ;; '#') echo shift-3 ;;
		'?') echo shift-slash ;; '[') echo bracket_left ;; ']') echo bracket_right ;; '~') echo shift-grave_accent ;;
		*) echo "Nieobsługiwany znak: $1" >&2; return 1 ;;
	esac
}

case "${1:-}" in
start)
	iso="${2:?podaj ISO albo -}"; fw="${3:-uefi}"; disk="${4:-}"
	machine=q35
	[ "$fw" = uefi-sb ] && machine=q35,smm=on
	args=(-enable-kvm -cpu host -smp 4 -m 4096 -machine "$machine"
		-device virtio-vga -display none
		-device qemu-xhci -device usb-tablet -device usb-kbd
		-netdev user,id=n0 -device virtio-net-pci,netdev=n0
		-monitor "unix:$MON,server,nowait" -qmp "unix:$QMP,server,nowait"
		-daemonize -pidfile "$RUN/qemu.pid")
	[ "$iso" = - ] || args+=(-cdrom "$(readlink -f "$iso")")
	if [ "$fw" = uefi ]; then
		[ -e "$RUN/vars.fd" ] && [ "$iso" = - ] || cp /usr/share/OVMF/OVMF_VARS_4M.fd "$RUN/vars.fd"
		args+=(-drive "if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd"
			-drive "if=pflash,format=raw,file=$RUN/vars.fd")
	elif [ "$fw" = uefi-sb ]; then
		cp /usr/share/OVMF/OVMF_VARS_4M.ms.fd "$RUN/vars-sb.fd"
		args+=(-global driver=cfi.pflash01,property=secure,value=on
			-drive "if=pflash,format=raw,unit=0,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.ms.fd"
			-drive "if=pflash,format=raw,unit=1,file=$RUN/vars-sb.fd")
	fi
	if [ -n "$disk" ]; then
		[ -e "$RUN/disk.qcow2" ] || qemu-img create -f qcow2 "$RUN/disk.qcow2" 30G >/dev/null
		args+=(-drive "file=$RUN/disk.qcow2,if=virtio")
	fi
	qemu-system-x86_64 "${args[@]}"
	echo "VM działa (pid $(cat "$RUN/qemu.pid"))"
	;;
shot)
	hmp "screendump $SHOTS/${2:?nazwa}.png -f png"
	echo "$SHOTS/$2.png"
	;;
key)
	shift
	for k in "$@"; do hmp "sendkey $k"; sleep 0.15; done
	;;
type)
	text="${2:?tekst}"
	for ((i = 0; i < ${#text}; i++)); do hmp "sendkey $(key_for "${text:i:1}")"; sleep 0.08; done
	;;
click)
	x="${2:?X}"; y="${3:?Y}"
	last="$(ls -t "$SHOTS"/*.png | head -n 1)"
	read -r w h < <(od -An -tu1 -j16 -N8 "$last" | awk '{print $1*16777216+$2*65536+$3*256+$4, $5*16777216+$6*65536+$7*256+$8}')
	ax=$((x * 32767 / (w - 1))); ay=$((y * 32767 / (h - 1)))
	qmp "{\"execute\":\"input-send-event\",\"arguments\":{\"events\":[{\"type\":\"abs\",\"data\":{\"axis\":\"x\",\"value\":$ax}},{\"type\":\"abs\",\"data\":{\"axis\":\"y\",\"value\":$ay}}]}}"
	sleep 0.2
	qmp '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":true,"button":"left"}}]}}'
	sleep 0.1
	qmp '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":false,"button":"left"}}]}}'
	;;
stop)
	[ -e "$RUN/qemu.pid" ] && kill "$(cat "$RUN/qemu.pid")" 2>/dev/null || true
	rm -f "$RUN/qemu.pid"
	;;
*)
	sed -n '2,9p' "$0"
	exit 1
	;;
esac
