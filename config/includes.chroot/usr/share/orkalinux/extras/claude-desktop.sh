#!/bin/sh
set -e
key=/usr/share/keyrings/claude-desktop-archive-keyring.asc
curl -fsSLo "$key" https://downloads.claude.ai/claude-desktop/key.asc
gpg --show-keys --with-colons "$key" | grep -q '^fpr:::::::::31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE:' || {
	echo "Zły klucz repozytorium Claude, przerywam."
	rm -f "$key"
	exit 1
}
echo "deb [arch=amd64,arm64 signed-by=$key] https://downloads.claude.ai/claude-desktop/apt/stable stable main" \
	> /etc/apt/sources.list.d/claude-desktop.list
apt-get -o DPkg::Lock::Timeout=300 update
apt-get -o DPkg::Lock::Timeout=300 install -y claude-desktop
