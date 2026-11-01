# Building OrkaLinux

OrkaLinux is built with Debian's [live-build](https://salsa.debian.org/live-team/live-build). The scripts are made for **Debian 13 (Trixie)**, for example in WSL on Windows.

## Build

In the project folder:

```bash
sudo bash build.sh
```

The finished ISO lands in `out/`, together with `build.log`.

- The build itself runs in `/srv/orkalinux-build` on the Linux disk, because live-build does not work on `/mnt/c`. Set `ORKA_WORK` to use another folder.
- Downloaded packages stay there in a cache, so later builds are faster.
- The first build takes 30 to 90 minutes and downloads about 3 GB of packages. Keep about 20 GB free.
- Files edited on Windows are fine: `build.sh` fixes line endings and file permissions on its own.

## Name and version

Change them only in `orkalinux.conf`. `build.sh` puts these values in place of every `@ORKA_...@` in `config/` (os-release, installer, OrkaLinux Hello, boot menu).

## What is where

| What | Where |
|---|---|
| Name, version, links | `orkalinux.conf` |
| live-build settings | `auto/config` |
| Installed programs | `config/package-lists/*.list.chroot` |
| GRUB packages on the ISO, for installing offline | `config/package-lists/*.list.binary` |
| Scripts run inside the new system | `config/hooks/normal/` |
| Files copied into the system | `config/includes.chroot/` |
| ISO boot menu | `config/bootloaders/` |
| Original artwork from B1 | `b1-assets/` |

## Hooks

| Hook | What it does |
|---|---|
| `0100` | os-release, so the system calls itself OrkaLinux |
| `0200` | Discord, from the official .deb package (it is not in Debian) |
| `0300` | Theme (wallpaper, GRUB and login background through desktop-base), Plymouth, Fastfetch |
| `0400` | Calamares installer branding |

## Secure Boot

Calamares runs `/usr/sbin/orkalinux-grub-install` instead of `grub-install`. On UEFI it adds `--force-extra-removable`, so the signed shim and GRUB also go to `/EFI/BOOT`. The installed system then starts with Secure Boot on even when the firmware forgets its boot entry. The EFI folder stays `debian`, because Debian's signed GRUB looks for its config there.

## Testing in a virtual machine

`test-vm.sh` starts the ISO in QEMU without a window and drives it from the command line (as root, in WSL):

```bash
bash test-vm.sh start out/OrkaLinux-B2-amd64.hybrid.iso [uefi|uefi-sb|bios] [disk]
bash test-vm.sh start - uefi            # boot the installed system from the disk
bash test-vm.sh shot name               # screenshot to out/screens/name.png
bash test-vm.sh key ret tab ...         # press keys (QEMU names: ret, tab, down, spc, ctrl-alt-t)
bash test-vm.sh type "text"             # type text
bash test-vm.sh click X Y               # click a point (pixels from the last screenshot)
bash test-vm.sh stop
```

`uefi-sb` turns on Secure Boot with Microsoft keys, like a typical laptop. `disk` attaches an empty 30 GB disk for installing.
