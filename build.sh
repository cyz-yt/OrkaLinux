#!/bin/bash
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
WORK="${ORKA_WORK:-/srv/orkalinux-build}"
OUT="$SRC/out"

if [ "$(id -u)" -ne 0 ]; then
	echo "Uruchom przez sudo: sudo bash $0" >&2
	exit 1
fi

. <(sed 's/\r$//' "$SRC/orkalinux.conf")
echo ">> Buduję $ORKA_NAME $ORKA_VERSION ($ORKA_CODENAME)"

. /etc/os-release
if [ "${VERSION_CODENAME:-}" != trixie ]; then
	echo "Uwaga: budowanie jest przygotowane pod Debiana 13 (trixie), a masz: $PRETTY_NAME" >&2
fi
missing=""
for p in live-build apt-utils rsync; do
	dpkg -s "$p" >/dev/null 2>&1 || missing="$missing $p"
done
if [ -n "$missing" ]; then
	echo ">> Instaluję:$missing"
	apt-get update
	apt-get install -y $missing
fi

mkdir -p "$WORK"
cd "$WORK"
if [ -d .build ]; then
	lb clean
fi
rsync -a --delete --chown=root:root --chmod=D755,F644 "$SRC/auto/" auto/
rsync -a --delete --chown=root:root --chmod=D755,F644 "$SRC/config/" config/
install -m 644 "$SRC/orkalinux.conf" orkalinux.conf

{ grep -rlIZ $'\r' auto config orkalinux.conf || true; } | xargs -0 -r sed -i 's/\r$//'
chmod 755 auto/* config/hooks/normal/*.hook.chroot \
	config/includes.chroot/usr/share/orkalinux-hello/orkalinux-hello.py \
	config/includes.chroot/usr/sbin/orkalinux-grub-install \
	config/includes.chroot/usr/lib/live/config/*
{ grep -rlIZ '@ORKA_' config || true; } | xargs -0 -r sed -i \
	-e "s|@ORKA_NAME@|$ORKA_NAME|g" \
	-e "s|@ORKA_VERSION@|$ORKA_VERSION|g" \
	-e "s|@ORKA_VERSION_ID@|$ORKA_VERSION_ID|g" \
	-e "s|@ORKA_CODENAME@|$ORKA_CODENAME|g" \
	-e "s|@ORKA_URL@|$ORKA_URL|g" \
	-e "s|@ORKA_DISCORD@|$ORKA_DISCORD|g"

lb config
lb build 2>&1 | tee build.log

mkdir -p "$OUT"
iso="$(ls -t ./*.iso | head -n 1)"
cp -v "$iso" "$OUT/"
cp build.log "$OUT/build.log"
echo ">> Gotowe: $OUT/$(basename "$iso")"
