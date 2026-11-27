#!/usr/bin/env python3
import glob
import os
import subprocess
import re
import shutil
import sys
import threading
import time

sys.path.insert(0, "/usr/share/orkalinux/lib")
import orka
from orka import Gtk, GLib, Gdk

NVIDIA_SCRIPT = "/usr/sbin/orkalinux-nvidia-install"

TEXTS = {
    "en": {
        "rec": "OrkaLinux Recovery", "rec_d": "A separate repair mode, like on Windows: restore points, repairing startup and software, freeing up space. It also starts from the boot menu when the desktop won't.", "rec_btn": "Restart into Recovery", "rec_q": "Restart into OrkaLinux Recovery?", "rec_q2": "Save your work first - the computer restarts right away.", "rec_go": "Restart", "sec_ra": "Passwords and terminal in Recovery", "sec_ra_d": "OrkaLinux Recovery can change a user's password and open a terminal without asking for one. Handy when you forget your password, but anyone at the computer could use it. Turn it off if other people have access to this PC.",
        "p_settings": "Settings",
        "p_settings_sub": "Everything you usually set up, one click away. Each tile opens the right page of System Settings.",
        "upd_title": "Update everything",
        "upd_text": "System packages and Flatpak apps in one go. The terminal will ask for your password.",
        "upd_btn": "Update now",
        "sec": "Security", "sec_fw": "Firewall", "sec_fw_d": "Blocks connections coming in from outside. Apps and KDE Connect keep working.", "sec_au": "Automatic security updates", "sec_au_d": "Debian security fixes install by themselves in the background, once a day.",
        "upd_none": "Everything is up to date.", "upd_some": "Updates waiting: {n}", "k_now": "running now",
        "all_settings": "All settings",
        "g_conn": "Connections",
        "g_hw": "Devices",
        "g_sys": "System",
        "k_net": "Wi-Fi and network",
        "k_bt": "Bluetooth",
        "k_disp": "Displays",
        "k_sound": "Sound",
        "k_print": "Printers",
        "k_kbd": "Keyboard",
        "k_mouse": "Mouse",
        "k_touch": "Touchpad",
        "k_power": "Power and battery",
        "k_users": "Users",
        "k_lang": "Language and region",
        "k_clock": "Date and time",
        "k_apps": "Default apps",
        "k_auto": "Autostart",
        "k_notif": "Notifications",
        "k_fonts": "Fonts",
        "k_monitor": "System monitor",
        "k_disks": "Disks and partitions",
        "k_fw": "Firewall",
        "k_about": "About this system",
        "title": "OrkaLinux Center", "subtitle": "Your computer, drivers and system in one place",
        "p_info": "This computer", "p_drivers": "Drivers", "p_kernel": "Linux kernel", "p_clean": "Cleanup",
        "p_drivers_sub": "OrkaLinux uses open drivers built into Linux. Only NVIDIA cards need an extra driver for full speed.",
        "p_kernel_sub": "The kernel is the heart of the system. OrkaLinux uses a newer one from Debian backports, for newer hardware.",
        "p_clean_sub": "Free up space by removing things the system no longer needs. Your own files are not touched.",
        "system": "System", "model": "Computer", "cpu": "Processor", "gpu": "Graphics", "ram": "Memory",
        "disk": "Disk", "kernel": "Kernel", "desktop": "Desktop", "uptime": "Running for",
        "used_of": "{used} used of {total}", "copy": "Copy info", "copied": "Copied!",
        "driver_in_use": "Driver in use: {driver}", "no_driver": "no driver loaded",
        "nv_title": "NVIDIA driver", "nv_ok": "The NVIDIA driver is installed and working.",
        "nv_installed_reboot": "The NVIDIA driver is installed. Restart the computer to start using it.",
        "nv_missing": "Your NVIDIA card runs on the basic open driver. Install the NVIDIA driver for games and full performance.",
        "nv_install": "Install NVIDIA driver", "no_nvidia": "No NVIDIA card here. Your graphics already work with the built-in driver, nothing to install.",
        "k_running": "Running now", "k_installed": "Installed kernels", "k_update": "Update the kernel",
        "k_update_avail": "Update available: {ver}", "k_up_to_date": "The kernel is up to date.",
        "k_clean": "Remove old kernels", "k_checking": "Checking...",
        "c_apt": "Downloaded update packages", "c_auto": "Packages nobody needs any more",
        "c_logs": "Old system logs (older than 2 weeks)", "c_flatpak": "Unused Flatpak runtimes",
        "c_thumbs": "Picture thumbnails", "c_trash": "Trash",
        "c_count": "{n} packages", "c_clean": "Clean selected", "c_refresh": "Refresh",
        "c_nothing": "All clean - there is nothing to tidy up right now.",
        "c_done": "Cleaned up {size}.", "c_admin": "The rest needs your password and runs in the terminal.",
        "c_q": "Clean the selected items?", "c_q2": "This can't be undone. Trash is emptied for good.",
        "clean": "Clean",
        "days": "{d} d", "hours": "{h} h", "minutes": "{m} min",
    },
    "pl": {
        "rec": "OrkaLinux Recovery", "rec_d": "Osobny tryb naprawy, jak w Windowsie: punkty przywracania, naprawa uruchamiania i programów, zwalnianie miejsca. Odpalisz go też z menu startowego, kiedy pulpit nie chce wstać.", "rec_btn": "Uruchom ponownie do Recovery", "rec_q": "Uruchomić ponownie do OrkaLinux Recovery?", "rec_q2": "Zapisz najpierw swoją pracę – komputer zrestartuje się od razu.", "rec_go": "Uruchom ponownie", "sec_ra": "Hasła i terminal w Recovery", "sec_ra_d": "OrkaLinux Recovery może zmienić hasło użytkownika i otworzyć terminal bez pytania o hasło. Przydaje się, gdy zapomnisz hasła, ale skorzystać z tego może każdy, kto siedzi przy komputerze. Wyłącz, jeśli inni mają dostęp do tego komputera.",
        "p_settings": "Ustawienia",
        "p_settings_sub": "Wszystko, co zwykle się ustawia, pod jednym kliknięciem. Każdy kafelek otwiera właściwą stronę Ustawień systemu.",
        "upd_title": "Zaktualizuj wszystko",
        "upd_text": "Paczki systemu i programy z Flatpaka za jednym razem. Terminal zapyta o hasło.",
        "upd_btn": "Aktualizuj teraz",
        "sec": "Bezpieczeństwo", "sec_fw": "Zapora sieciowa", "sec_fw_d": "Blokuje połączenia przychodzące z zewnątrz. Programy i KDE Connect działają dalej.", "sec_au": "Automatyczne aktualizacje bezpieczeństwa", "sec_au_d": "Poprawki bezpieczeństwa Debiana instalują się same w tle, raz dziennie.",
        "upd_none": "Wszystko jest aktualne.", "upd_some": "Aktualizacje do pobrania: {n}", "k_now": "działa teraz",
        "all_settings": "Wszystkie ustawienia",
        "g_conn": "Połączenia",
        "g_hw": "Urządzenia",
        "g_sys": "System",
        "k_net": "Wi-Fi i sieć",
        "k_bt": "Bluetooth",
        "k_disp": "Ekrany",
        "k_sound": "Dźwięk",
        "k_print": "Drukarki",
        "k_kbd": "Klawiatura",
        "k_mouse": "Mysz",
        "k_touch": "Touchpad",
        "k_power": "Zasilanie i bateria",
        "k_users": "Użytkownicy",
        "k_lang": "Język i region",
        "k_clock": "Data i godzina",
        "k_apps": "Domyślne programy",
        "k_auto": "Autostart",
        "k_notif": "Powiadomienia",
        "k_fonts": "Czcionki",
        "k_monitor": "Monitor systemu",
        "k_disks": "Dyski i partycje",
        "k_fw": "Zapora sieciowa",
        "k_about": "O systemie",
        "title": "Centrum OrkaLinux", "subtitle": "Komputer, sterowniki i system w jednym miejscu",
        "p_info": "Ten komputer", "p_drivers": "Sterowniki", "p_kernel": "Jądro Linuksa", "p_clean": "Sprzątanie",
        "p_drivers_sub": "OrkaLinux używa otwartych sterowników wbudowanych w Linuksa. Tylko karty NVIDIA potrzebują dodatkowego sterownika do pełnej mocy.",
        "p_kernel_sub": "Jądro to serce systemu. OrkaLinux ma nowsze, z Debian backports, żeby lepiej działał nowy sprzęt.",
        "p_clean_sub": "Zwolnij miejsce, usuwając rzeczy, których system już nie potrzebuje. Twoich plików to nie rusza.",
        "system": "System", "model": "Komputer", "cpu": "Procesor", "gpu": "Grafika", "ram": "Pamięć",
        "disk": "Dysk", "kernel": "Jądro", "desktop": "Pulpit", "uptime": "Działa od",
        "used_of": "zajęte {used} z {total}", "copy": "Kopiuj informacje", "copied": "Skopiowane!",
        "driver_in_use": "Używany sterownik: {driver}", "no_driver": "brak sterownika",
        "nv_title": "Sterownik NVIDIA", "nv_ok": "Sterownik NVIDIA jest zainstalowany i działa.",
        "nv_installed_reboot": "Sterownik NVIDIA jest zainstalowany. Uruchom komputer ponownie, żeby zaczął działać.",
        "nv_missing": "Twoja karta NVIDIA działa na podstawowym, otwartym sterowniku. Zainstaluj sterownik NVIDIA do gier i pełnej wydajności.",
        "nv_install": "Zainstaluj sterownik NVIDIA", "no_nvidia": "Nie masz karty NVIDIA. Grafika działa już na wbudowanym sterowniku, nic nie trzeba instalować.",
        "k_running": "Działa teraz", "k_installed": "Zainstalowane jądra", "k_update": "Zaktualizuj jądro",
        "k_update_avail": "Jest aktualizacja: {ver}", "k_up_to_date": "Jądro jest aktualne.",
        "k_clean": "Usuń stare jądra", "k_checking": "Sprawdzam...",
        "c_apt": "Pobrane paczki z aktualizacji", "c_auto": "Paczki, których nic już nie potrzebuje",
        "c_logs": "Stare logi systemu (starsze niż 2 tygodnie)", "c_flatpak": "Nieużywane biblioteki Flatpak",
        "c_thumbs": "Miniatury zdjęć", "c_trash": "Kosz",
        "c_count": "{n} paczek", "c_clean": "Wyczyść zaznaczone", "c_refresh": "Odśwież",
        "c_nothing": "Wszystko czyste - nie ma teraz czego sprzątać.",
        "c_done": "Wyczyszczono {size}.", "c_admin": "Reszta wymaga hasła i robi się w terminalu.",
        "c_q": "Wyczyścić zaznaczone rzeczy?", "c_q2": "Tego nie da się cofnąć. Kosz zostanie opróżniony na dobre.",
        "clean": "Wyczyść",
        "days": "{d} dni", "hours": "{h} godz.", "minutes": "{m} min",
    },
    "de": {
        "rec": "OrkaLinux Recovery", "rec_d": "Ein eigener Reparaturmodus wie unter Windows: Wiederherstellungspunkte, Start und Software reparieren, Speicher freigeben. Er startet auch aus dem Bootmenü, wenn der Desktop nicht hochfährt.", "rec_btn": "Neu starten in Recovery", "rec_q": "In OrkaLinux Recovery neu starten?", "rec_q2": "Speichere vorher deine Arbeit - der Computer startet sofort neu.", "rec_go": "Neu starten", "sec_ra": "Passwörter und Terminal in Recovery", "sec_ra_d": "OrkaLinux Recovery kann das Passwort eines Benutzers ändern und ein Terminal öffnen, ohne nach einem Passwort zu fragen. Praktisch, wenn du dein Passwort vergisst, aber jeder am Computer kann es nutzen. Schalte es aus, wenn andere Zugriff auf diesen PC haben.",
        "p_settings": "Einstellungen",
        "p_settings_sub": "Alles, was man oft einstellt, mit einem Klick. Jede Kachel öffnet die passende Seite der Systemeinstellungen.",
        "upd_title": "Alles aktualisieren",
        "upd_text": "Systempakete und Flatpak-Apps auf einmal. Das Terminal fragt nach deinem Passwort.",
        "upd_btn": "Jetzt aktualisieren",
        "sec": "Sicherheit", "sec_fw": "Firewall", "sec_fw_d": "Blockiert eingehende Verbindungen von außen. Programme und KDE Connect laufen weiter.", "sec_au": "Automatische Sicherheitsupdates", "sec_au_d": "Debian-Sicherheitskorrekturen werden einmal am Tag im Hintergrund installiert.",
        "upd_none": "Alles ist aktuell.", "upd_some": "Updates verfügbar: {n}", "k_now": "läuft gerade",
        "all_settings": "Alle Einstellungen",
        "g_conn": "Verbindungen",
        "g_hw": "Geräte",
        "g_sys": "System",
        "k_net": "WLAN und Netzwerk",
        "k_bt": "Bluetooth",
        "k_disp": "Bildschirme",
        "k_sound": "Ton",
        "k_print": "Drucker",
        "k_kbd": "Tastatur",
        "k_mouse": "Maus",
        "k_touch": "Touchpad",
        "k_power": "Energie und Akku",
        "k_users": "Benutzer",
        "k_lang": "Sprache und Region",
        "k_clock": "Datum und Uhrzeit",
        "k_apps": "Standardprogramme",
        "k_auto": "Autostart",
        "k_notif": "Benachrichtigungen",
        "k_fonts": "Schriftarten",
        "k_monitor": "Systemmonitor",
        "k_disks": "Festplatten",
        "k_fw": "Firewall",
        "k_about": "Über dieses System",
        "title": "OrkaLinux Zentrum", "subtitle": "Computer, Treiber und System an einem Ort",
        "p_info": "Dieser Computer", "p_drivers": "Treiber", "p_kernel": "Linux-Kernel", "p_clean": "Aufräumen",
        "p_drivers_sub": "OrkaLinux nutzt offene Treiber, die in Linux eingebaut sind. Nur NVIDIA-Karten brauchen einen Zusatztreiber für volle Leistung.",
        "p_kernel_sub": "Der Kernel ist das Herz des Systems. OrkaLinux nutzt einen neueren aus Debian Backports, für neue Hardware.",
        "p_clean_sub": "Schaffe Platz, indem du Unnötiges entfernst. Deine eigenen Dateien bleiben unberührt.",
        "system": "System", "model": "Computer", "cpu": "Prozessor", "gpu": "Grafik", "ram": "Arbeitsspeicher",
        "disk": "Festplatte", "kernel": "Kernel", "desktop": "Desktop", "uptime": "Läuft seit",
        "used_of": "{used} von {total} belegt", "copy": "Infos kopieren", "copied": "Kopiert!",
        "driver_in_use": "Treiber: {driver}", "no_driver": "kein Treiber geladen",
        "nv_title": "NVIDIA-Treiber", "nv_ok": "Der NVIDIA-Treiber ist installiert und läuft.",
        "nv_installed_reboot": "Der NVIDIA-Treiber ist installiert. Starte den Computer neu, um ihn zu nutzen.",
        "nv_missing": "Deine NVIDIA-Karte läuft mit dem einfachen offenen Treiber. Installiere den NVIDIA-Treiber für Spiele und volle Leistung.",
        "nv_install": "NVIDIA-Treiber installieren", "no_nvidia": "Keine NVIDIA-Karte vorhanden. Die Grafik läuft schon mit dem eingebauten Treiber.",
        "k_running": "Läuft gerade", "k_installed": "Installierte Kernel", "k_update": "Kernel aktualisieren",
        "k_update_avail": "Update verfügbar: {ver}", "k_up_to_date": "Der Kernel ist aktuell.",
        "k_clean": "Alte Kernel entfernen", "k_checking": "Wird geprüft...",
        "c_apt": "Heruntergeladene Update-Pakete", "c_auto": "Pakete, die niemand mehr braucht",
        "c_logs": "Alte Systemprotokolle (älter als 2 Wochen)", "c_flatpak": "Ungenutzte Flatpak-Laufzeiten",
        "c_thumbs": "Vorschaubilder", "c_trash": "Papierkorb",
        "c_count": "{n} Pakete", "c_clean": "Auswahl aufräumen", "c_refresh": "Aktualisieren",
        "c_nothing": "Alles sauber - gerade gibt es nichts aufzuräumen.",
        "c_done": "{size} aufgeräumt.", "c_admin": "Der Rest braucht dein Passwort und läuft im Terminal.",
        "c_q": "Ausgewähltes aufräumen?", "c_q2": "Das lässt sich nicht rückgängig machen. Der Papierkorb wird endgültig geleert.",
        "clean": "Aufräumen",
        "days": "{d} T.", "hours": "{h} Std.", "minutes": "{m} Min.",
    },
    "fr": {
        "rec": "OrkaLinux Recovery", "rec_d": "Un mode de réparation à part, comme sous Windows : points de restauration, réparation du démarrage et des logiciels, libération d'espace. Il se lance aussi depuis le menu de démarrage quand le bureau ne démarre pas.", "rec_btn": "Redémarrer dans Recovery", "rec_q": "Redémarrer dans OrkaLinux Recovery ?", "rec_q2": "Enregistre ton travail avant - l'ordinateur redémarre tout de suite.", "rec_go": "Redémarrer", "sec_ra": "Mots de passe et terminal dans Recovery", "sec_ra_d": "OrkaLinux Recovery peut changer le mot de passe d'un utilisateur et ouvrir un terminal sans en demander. Pratique si tu oublies ton mot de passe, mais n'importe qui devant l'ordinateur peut s'en servir. Désactive-le si d'autres ont accès à ce PC.",
        "p_settings": "Réglages",
        "p_settings_sub": "Tout ce qu'on règle souvent, en un clic. Chaque tuile ouvre la bonne page de la Configuration du système.",
        "upd_title": "Tout mettre à jour",
        "upd_text": "Paquets du système et applis Flatpak d'un coup. Le terminal demandera ton mot de passe.",
        "upd_btn": "Mettre à jour",
        "sec": "Sécurité", "sec_fw": "Pare-feu", "sec_fw_d": "Bloque les connexions entrantes. Les applis et KDE Connect continuent de marcher.", "sec_au": "Mises à jour de sécurité automatiques", "sec_au_d": "Les correctifs de sécurité Debian s'installent seuls en arrière-plan, une fois par jour.",
        "upd_none": "Tout est à jour.", "upd_some": "Mises à jour disponibles : {n}", "k_now": "en cours",
        "all_settings": "Tous les réglages",
        "g_conn": "Connexions",
        "g_hw": "Périphériques",
        "g_sys": "Système",
        "k_net": "Wi-Fi et réseau",
        "k_bt": "Bluetooth",
        "k_disp": "Écrans",
        "k_sound": "Son",
        "k_print": "Imprimantes",
        "k_kbd": "Clavier",
        "k_mouse": "Souris",
        "k_touch": "Pavé tactile",
        "k_power": "Énergie et batterie",
        "k_users": "Utilisateurs",
        "k_lang": "Langue et région",
        "k_clock": "Date et heure",
        "k_apps": "Applis par défaut",
        "k_auto": "Démarrage auto",
        "k_notif": "Notifications",
        "k_fonts": "Polices",
        "k_monitor": "Moniteur système",
        "k_disks": "Disques",
        "k_fw": "Pare-feu",
        "k_about": "À propos du système",
        "title": "Centre OrkaLinux", "subtitle": "Ton ordinateur, les pilotes et le système au même endroit",
        "p_info": "Cet ordinateur", "p_drivers": "Pilotes", "p_kernel": "Noyau Linux", "p_clean": "Nettoyage",
        "p_drivers_sub": "OrkaLinux utilise les pilotes libres intégrés à Linux. Seules les cartes NVIDIA ont besoin d'un pilote en plus.",
        "p_kernel_sub": "Le noyau est le cœur du système. OrkaLinux en utilise un plus récent (Debian backports) pour le matériel récent.",
        "p_clean_sub": "Libère de la place en supprimant ce dont le système n'a plus besoin. Tes fichiers ne sont pas touchés.",
        "system": "Système", "model": "Ordinateur", "cpu": "Processeur", "gpu": "Graphique", "ram": "Mémoire",
        "disk": "Disque", "kernel": "Noyau", "desktop": "Bureau", "uptime": "Allumé depuis",
        "used_of": "{used} utilisés sur {total}", "copy": "Copier les infos", "copied": "Copié !",
        "driver_in_use": "Pilote utilisé : {driver}", "no_driver": "aucun pilote chargé",
        "nv_title": "Pilote NVIDIA", "nv_ok": "Le pilote NVIDIA est installé et fonctionne.",
        "nv_installed_reboot": "Le pilote NVIDIA est installé. Redémarre l'ordinateur pour l'utiliser.",
        "nv_missing": "Ta carte NVIDIA utilise le pilote libre de base. Installe le pilote NVIDIA pour les jeux et toutes les performances.",
        "nv_install": "Installer le pilote NVIDIA", "no_nvidia": "Pas de carte NVIDIA ici. Le graphique marche déjà avec le pilote intégré.",
        "k_running": "En cours", "k_installed": "Noyaux installés", "k_update": "Mettre à jour le noyau",
        "k_update_avail": "Mise à jour disponible : {ver}", "k_up_to_date": "Le noyau est à jour.",
        "k_clean": "Supprimer les anciens noyaux", "k_checking": "Vérification...",
        "c_apt": "Paquets de mise à jour téléchargés", "c_auto": "Paquets dont plus rien n'a besoin",
        "c_logs": "Anciens journaux système (plus de 2 semaines)", "c_flatpak": "Runtimes Flatpak inutilisés",
        "c_thumbs": "Miniatures d'images", "c_trash": "Corbeille",
        "c_count": "{n} paquets", "c_clean": "Nettoyer la sélection", "c_refresh": "Actualiser",
        "c_nothing": "Tout est propre - rien à nettoyer pour l'instant.",
        "c_done": "{size} libérés.", "c_admin": "Le reste demande ton mot de passe et se fait dans le terminal.",
        "c_q": "Nettoyer la sélection ?", "c_q2": "Impossible d'annuler. La corbeille sera vidée définitivement.",
        "clean": "Nettoyer",
        "days": "{d} j", "hours": "{h} h", "minutes": "{m} min",
    },
}

VENDORS = {"0x10de": "NVIDIA", "0x1002": "AMD", "0x8086": "Intel", "0x15ad": "VMware",
           "0x80ee": "VirtualBox", "0x1af4": "Virtio", "0x1234": "QEMU", "0x1b36": "QEMU"}


def read(path, default=""):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except OSError:
        return default


def gpus():
    found = []
    for dev in sorted(glob.glob("/sys/bus/pci/devices/*")):
        if not read(dev + "/class").startswith("0x03"):
            continue
        vendor_id = read(dev + "/vendor")
        vendor = VENDORS.get(vendor_id, vendor_id)
        name = vendor
        if shutil.which("lspci"):
            out = orka.output(["lspci", "-mm", "-s", os.path.basename(dev)], 5)
            parts = re.findall(r'"([^"]*)"', out)
            if len(parts) >= 3:
                name = f"{parts[1]} {parts[2]}"
        driver = os.path.basename(os.path.realpath(dev + "/driver")) if os.path.exists(dev + "/driver") else ""
        found.append((name, vendor, driver))
    return found


def cpu_name():
    for line in read("/proc/cpuinfo").splitlines():
        if line.startswith("model name"):
            return re.sub(r"\s+", " ", line.split(":", 1)[1].strip())
    return os.uname().machine


def meminfo():
    info = {}
    for line in read("/proc/meminfo").splitlines():
        key, _, rest = line.partition(":")
        try:
            info[key] = int(rest.split()[0]) * 1024
        except (IndexError, ValueError):
            pass
    return info


def os_name():
    for line in read("/etc/os-release").splitlines():
        if line.startswith("PRETTY_NAME="):
            return line.split("=", 1)[1].strip('"')
    return "Linux"


APT = "apt-get -o DPkg::Lock::Timeout=300"


HELPER = "/usr/sbin/orka-centrum-helper"


def firewall_on():
    return "ENABLED=yes" in read("/etc/ufw/ufw.conf")


def autoupdate_on():
    return 'Unattended-Upgrade "1"' in read("/etc/apt/apt.conf.d/20auto-upgrades")


def recadmin_on():
    return "ALLOW_ADMIN=no" not in read("/etc/orkalinux/recovery.conf").split()


SETTINGS_TILES = [
    ("g_conn", "k_net", ["preferences-system-network", "network-wireless"], "kcm_networkmanagement"),
    ("g_conn", "k_bt", ["preferences-system-bluetooth", "bluetooth"], "kcm_bluetooth"),
    ("g_conn", "k_fw", ["security-high", "preferences-security-firewall"], "kcm_firewall"),
    ("g_hw", "k_disp", ["preferences-desktop-display", "video-display"], "kcm_kscreen"),
    ("g_hw", "k_sound", ["preferences-desktop-sound", "audio-speakers"], "kcm_pulseaudio"),
    ("g_hw", "k_print", ["printer", "preferences-devices-printer"], "kcm_printer_manager"),
    ("g_hw", "k_kbd", ["input-keyboard", "preferences-desktop-keyboard"], "kcm_keyboard"),
    ("g_hw", "k_mouse", ["input-mouse", "preferences-desktop-mouse"], "kcm_mouse"),
    ("g_hw", "k_touch", ["input-touchpad", "preferences-desktop-touchpad"], "kcm_touchpad"),
    ("g_hw", "k_power", ["preferences-system-power-management", "battery"], "kcm_powerdevilprofilesconfig"),
    ("g_sys", "k_users", ["system-users", "preferences-system-users"], "kcm_users"),
    ("g_sys", "k_lang", ["preferences-desktop-locale", "preferences-desktop-locale"], "kcm_regionandlang"),
    ("g_sys", "k_clock", ["preferences-system-time", "clock"], "kcm_clock"),
    ("g_sys", "k_apps", ["preferences-desktop-default-applications", "applications-other"], "kcm_componentchooser"),
    ("g_sys", "k_auto", ["system-run", "preferences-system-startup"], "kcm_autostart"),
    ("g_sys", "k_notif", ["preferences-desktop-notification", "notifications"], "kcm_notifications"),
    ("g_sys", "k_fonts", ["preferences-desktop-font", "font"], "kcm_fonts"),
    ("g_sys", "k_monitor", ["utilities-system-monitor", "org.kde.plasma-systemmonitor"], "app:plasma-systemmonitor"),
    ("g_sys", "k_disks", ["partitionmanager", "drive-harddisk"], "app:partitionmanager"),
    ("g_sys", "k_about", ["help-about", "dialog-information"], "kcm_about-distro"),
]


def kcm_available(name):
    return bool(glob.glob("/usr/lib/*/qt6/plugins/plasma/kcms/*/%s.so" % name)
                or glob.glob("/usr/lib/qt6/plugins/plasma/kcms/*/%s.so" % name))


class OrkaCentrum(orka.PagedWindow):
    def __init__(self):
        t = orka.Texts(TEXTS)
        super().__init__("orka-centrum", t["title"], t["subtitle"], "orka-centrum")
        self.t = t
        self.add_page("info", t["p_info"], "computer", self.page_info())
        self.add_page("settings", t["p_settings"], "preferences-system", self.page_settings(), t["p_settings_sub"])
        self.add_page("drivers", t["p_drivers"], "video-display", self.page_drivers(), t["p_drivers_sub"])
        self.add_page("kernel", t["p_kernel"], "orka-kernel", self.page_kernel(), t["p_kernel_sub"])
        self.add_page("clean", t["p_clean"], "edit-clear-all", self.page_clean(), t["p_clean_sub"])
        self.show_all()
        if len(sys.argv) > 1 and sys.argv[1] in ("info", "settings", "drivers", "kernel", "clean"):
            self.show_page(sys.argv[1])


    def page_settings(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        upd = Gtk.Box(spacing=16)
        icon = Gtk.Image.new_from_icon_name(orka.first_icon(["system-software-update", "update-none"]), Gtk.IconSize.DIALOG)
        icon.set_pixel_size(44)
        upd.pack_start(icon, False, False, 0)
        texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        texts.set_valign(Gtk.Align.CENTER)
        texts.pack_start(orka.label(self.t["upd_title"], "big"), False, False, 0)
        texts.pack_start(orka.label(self.t["upd_text"], "dim", wrap=True), False, False, 0)
        self.upd_status = orka.label(self.t["k_checking"], "dim")
        texts.pack_start(self.upd_status, False, False, 0)
        upd.pack_start(texts, True, True, 0)
        self.upd_btn = orka.button(self.t["upd_btn"], "ghost", self.update_all)
        self.upd_btn.set_valign(Gtk.Align.CENTER)
        self.upd_btn.set_sensitive(False)
        upd.pack_end(self.upd_btn, False, False, 0)
        page.pack_start(orka.card(upd), False, False, 0)
        threading.Thread(target=self.check_updates, daemon=True).start()

        self.sec_switches = {}
        self.sec_lock = False
        rows = []
        if shutil.which("ufw") or os.path.exists("/usr/sbin/ufw"):
            rows.append(("firewall", "sec_fw", firewall_on))
        if os.path.exists("/usr/bin/unattended-upgrade"):
            rows.append(("autoupdate", "sec_au", autoupdate_on))
        if not orka.IS_LIVE and os.path.exists("/usr/sbin/orka-recovery"):
            rows.append(("recadmin", "sec_ra", recadmin_on))
        if rows:
            page.pack_start(orka.label(self.t["sec"], "section"), False, False, 6)
        for what, key, state in rows:
            row = Gtk.Box(spacing=14)
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            texts.pack_start(orka.label(self.t[key], "big"), False, False, 0)
            texts.pack_start(orka.label(self.t[key + "_d"], "dim", wrap=True), False, False, 0)
            row.pack_start(texts, True, True, 0)
            switch = Gtk.Switch()
            switch.set_valign(Gtk.Align.CENTER)
            switch.set_active(state())
            switch.set_sensitive(not orka.IS_LIVE)
            switch.connect("notify::active", self.on_security, what, state)
            row.pack_end(switch, False, False, 0)
            self.sec_switches[what] = switch
            page.pack_start(orka.card(row), False, False, 0)

        if not orka.IS_LIVE and os.path.exists("/usr/sbin/orka-recovery"):
            page.pack_start(orka.label(self.t["rec"], "section"), False, False, 6)
            row = Gtk.Box(spacing=14)
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            texts.pack_start(orka.label(self.t["rec"], "big"), False, False, 0)
            texts.pack_start(orka.label(self.t["rec_d"], "dim", wrap=True), False, False, 0)
            row.pack_start(texts, True, True, 0)
            btn = orka.button(self.t["rec_btn"], "ghost", self.to_recovery)
            btn.set_valign(Gtk.Align.CENTER)
            row.pack_end(btn, False, False, 0)
            page.pack_start(orka.card(row), False, False, 0)

        group = None
        flow = None
        for grp, key, icons, target in SETTINGS_TILES:
            if target.startswith("app:"):
                if not shutil.which(target[4:]):
                    continue
            elif not kcm_available(target):
                continue
            if grp != group:
                group = grp
                page.pack_start(orka.label(self.t[grp], "section"), False, False, 6)
                flow = Gtk.FlowBox()
                flow.set_selection_mode(Gtk.SelectionMode.NONE)
                flow.set_homogeneous(True)
                flow.set_min_children_per_line(3)
                flow.set_max_children_per_line(5)
                flow.set_column_spacing(10)
                flow.set_row_spacing(10)
                page.pack_start(flow, False, False, 0)
            flow.add(self.settings_tile(self.t[key], icons, target))

        more = orka.button(self.t["all_settings"], "ghost", self.open_target, "app:systemsettings")
        more.set_halign(Gtk.Align.START)
        page.pack_start(more, False, False, 8)
        return page

    def settings_tile(self, text, icons, target):
        tile = Gtk.Button()
        tile.get_style_context().add_class("tile")
        box = Gtk.Box(spacing=12)
        box.set_margin_start(4)
        img = Gtk.Image.new_from_icon_name(orka.first_icon(icons), Gtk.IconSize.DND)
        img.set_pixel_size(32)
        box.pack_start(img, False, False, 0)
        box.pack_start(orka.label(text, "tile-name"), False, False, 0)
        tile.add(box)
        tile.connect("clicked", lambda *_: self.open_target(target))
        return tile

    def open_target(self, target):
        if target.startswith("app:"):
            cmd = [target[4:]]
        else:
            cmd = ["systemsettings", target]
        try:
            subprocess.Popen(cmd)
        except OSError:
            pass

    def on_security(self, switch, _param, what, state):
        if self.sec_lock:
            return
        want = switch.get_active()
        if want == state():
            return

        def done():
            self.sec_lock = True
            switch.set_active(state())
            self.sec_lock = False
        orka.run_in_terminal(self, ["sudo", HELPER, what, "on" if want else "off"], self.t, done)

    def to_recovery(self):
        if self.confirm(self.t["rec_q"], self.t["rec_q2"], self.t["rec_go"], self.t["cancel"], danger=True):
            try:
                subprocess.Popen(["pkexec", HELPER, "recovery"])
            except OSError:
                pass

    def update_all(self):
        orka.run_in_terminal(self, ["sudo", "sh", "-c", APT + " update && " + APT + " full-upgrade -y && "
                                    "(flatpak update -y --system || true)"], self.t, self.recheck_updates)


    def uptime(self):
        try:
            secs = int(float(read("/proc/uptime").split()[0]))
        except (IndexError, ValueError):
            return "?"
        d, rest = divmod(secs, 86400)
        h, rest = divmod(rest, 3600)
        m = rest // 60
        parts = []
        if d:
            parts.append(self.t["days"].format(d=d))
        if d or h:
            parts.append(self.t["hours"].format(h=h))
        parts.append(self.t["minutes"].format(m=m))
        return " ".join(parts)

    def page_info(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        head = Gtk.Box(spacing=18)
        logo = Gtk.Image.new_from_icon_name("orka-start", Gtk.IconSize.DIALOG)
        logo.set_pixel_size(72)
        head.pack_start(logo, False, False, 0)
        texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        texts.set_valign(Gtk.Align.CENTER)
        texts.pack_start(orka.label(os_name(), "page-title"), False, False, 0)
        vendor = read("/sys/class/dmi/id/sys_vendor")
        product = read("/sys/class/dmi/id/product_name")
        model = " ".join(p for p in (vendor, product) if p and "To Be Filled" not in p) or os.uname().nodename
        texts.pack_start(orka.label(model, "page-sub"), False, False, 0)
        head.pack_start(texts, True, True, 0)
        page.pack_start(orka.card(head), False, False, 0)

        mem = meminfo()
        total_ram = mem.get("MemTotal", 0)
        used_ram = total_ram - mem.get("MemAvailable", 0)
        disk = shutil.disk_usage("/")
        plasma = orka.output(["plasmashell", "--version"], 5).strip().replace("plasmashell", "KDE Plasma")
        gpu_names = [g[0] for g in gpus()] or ["?"]

        rows = [
            ("cpu", f"{cpu_name()} ({os.cpu_count()} × CPU)", None),
            ("gpu", "\n".join(gpu_names), None),
            ("ram", self.t["used_of"].format(used=orka.human_size(used_ram), total=orka.human_size(total_ram)),
             used_ram / total_ram if total_ram else 0),
            ("disk", self.t["used_of"].format(used=orka.human_size(disk.used), total=orka.human_size(disk.total)),
             disk.used / disk.total if disk.total else 0),
            ("kernel", os.uname().release, None),
            ("desktop", plasma or "KDE Plasma", None),
            ("uptime", self.uptime(), None),
        ]
        self.info_text = [f"{os_name()} – {model}"]
        grid = Gtk.Grid(column_spacing=24, row_spacing=12)
        for i, (key, value, fraction) in enumerate(rows):
            grid.attach(orka.label(self.t[key], "dim"), 0, i, 1, 1)
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            col.set_hexpand(True)
            col.pack_start(orka.label(value, "text", selectable=True), False, False, 0)
            if fraction is not None:
                bar = Gtk.LevelBar()
                bar.set_value(max(0.0, min(1.0, fraction)))
                col.pack_start(bar, False, False, 0)
            grid.attach(col, 1, i, 1, 1)
            self.info_text.append(f"{self.t[key]}: {value}".replace("\n", ", "))
        page.pack_start(orka.card(grid), False, False, 0)

        copy = orka.button(self.t["copy"], "ghost")
        copy.set_halign(Gtk.Align.START)
        copy.connect("clicked", self.copy_info)
        page.pack_start(copy, False, False, 0)
        return page

    def copy_info(self, btn):
        Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text("\n".join(self.info_text), -1)
        btn.set_label(self.t["copied"])
        GLib.timeout_add(1500, lambda: btn.set_label(self.t["copy"]) or False)


    def page_drivers(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        cards = gpus()
        for name, vendor, driver in cards:
            row = Gtk.Box(spacing=14)
            icon = Gtk.Image.new_from_icon_name("video-display", Gtk.IconSize.DIALOG)
            icon.set_pixel_size(40)
            row.pack_start(icon, False, False, 0)
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            texts.pack_start(orka.label(name, "big", wrap=True), False, False, 0)
            texts.pack_start(orka.label(self.t["driver_in_use"].format(driver=driver or self.t["no_driver"]), "dim"),
                             False, False, 0)
            row.pack_start(texts, True, True, 0)
            page.pack_start(orka.card(row), False, False, 0)

        has_nvidia = any(v == "NVIDIA" for _, v, _ in cards)
        nv = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        nv.pack_start(orka.label(self.t["nv_title"], "section"), False, False, 0)
        if not has_nvidia:
            nv.pack_start(orka.label(self.t["no_nvidia"], "text", wrap=True), False, False, 0)
        else:
            in_use = any(d == "nvidia" for _, v, d in cards if v == "NVIDIA")
            installed = orka.package_installed("nvidia-driver")
            if in_use:
                nv.pack_start(orka.label("✓ " + self.t["nv_ok"], "ok", wrap=True), False, False, 0)
            elif installed:
                nv.pack_start(orka.label(self.t["nv_installed_reboot"], "warn", wrap=True), False, False, 0)
            else:
                nv.pack_start(orka.label(self.t["nv_missing"], "text", wrap=True), False, False, 0)
                btn = orka.button(self.t["nv_install"], "primary", self.install_nvidia)
                btn.set_halign(Gtk.Align.START)
                if orka.IS_LIVE:
                    btn.set_sensitive(False)
                    nv.pack_start(orka.label(self.t["live_only_installed"], "dim", wrap=True), False, False, 0)
                nv.pack_start(btn, False, False, 0)
        page.pack_start(orka.card(nv), False, False, 6)
        return page

    def install_nvidia(self):
        lang = "pl" if self.t.lang == "pl" else "en"
        orka.run_in_terminal(self, ["sudo", NVIDIA_SCRIPT, lang], self.t)


    def page_kernel(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        run = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        run.pack_start(orka.label(self.t["k_running"], "dim"), False, False, 0)
        run.pack_start(orka.label(os.uname().release, "big", selectable=True), False, False, 0)
        page.pack_start(orka.card(run), False, False, 0)

        inst = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        inst.pack_start(orka.label(self.t["k_installed"], "section"), False, False, 0)
        out = orka.output(["dpkg-query", "-W", "-f=${Package} ${Version} ${db:Status-Abbrev}\n",
                           "linux-image-[0-9]*"], 10)
        for line in sorted(out.splitlines(), reverse=True):
            parts = line.split()
            if len(parts) >= 3 and parts[2].startswith("ii"):
                current = parts[0] == "linux-image-" + os.uname().release
                row = Gtk.Box(spacing=10)
                row.pack_start(orka.label(parts[0].replace("linux-image-", ""), "text"), False, False, 0)
                if current:
                    badge = orka.label(self.t["k_now"], "badge-ok")
                    badge.set_valign(Gtk.Align.CENTER)
                    row.pack_start(badge, False, False, 0)
                inst.pack_start(row, False, False, 0)
        page.pack_start(orka.card(inst), False, False, 0)

        self.kernel_status = orka.label(self.t["k_checking"], "dim")
        page.pack_start(self.kernel_status, False, False, 0)
        buttons = Gtk.Box(spacing=10)
        self.kernel_upd = upd = orka.button(self.t["k_update"], "ghost", self.update_kernel)
        cln = orka.button(self.t["k_clean"], "ghost", self.clean_kernels)
        upd.set_sensitive(False)
        cln.set_sensitive(not orka.IS_LIVE)
        for b in (upd, cln):
            buttons.pack_start(b, False, False, 0)
        page.pack_start(buttons, False, False, 0)
        if orka.IS_LIVE:
            page.pack_start(orka.label(self.t["live_only_installed"], "dim", wrap=True), False, False, 0)
        threading.Thread(target=self.check_kernel, daemon=True).start()
        return page

    def check_kernel(self):
        out = orka.output(["apt-cache", "policy", "linux-image-amd64"], 30)
        installed = re.search(r"Installed:\s*(\S+)", out)
        candidate = re.search(r"Candidate:\s*(\S+)", out)
        if installed and candidate and installed.group(1) not in ("(none)", candidate.group(1)):
            text, cls = self.t["k_update_avail"].format(ver=candidate.group(1)), "warn"
        else:
            text, cls = self.t["k_up_to_date"], "ok"
        GLib.idle_add(self.show_kernel_status, text, cls)

    def show_kernel_status(self, text, cls):
        self.kernel_status.set_text(text)
        ctx = self.kernel_status.get_style_context()
        for c in ("dim", "ok", "warn"):
            ctx.remove_class(c)
        ctx.add_class(cls)
        if cls == "warn":
            self.kernel_upd.get_style_context().remove_class("ghost")
            self.kernel_upd.get_style_context().add_class("primary")
            self.kernel_upd.set_sensitive(not orka.IS_LIVE)
        else:
            self.kernel_upd.get_style_context().remove_class("primary")
            self.kernel_upd.get_style_context().add_class("ghost")
            self.kernel_upd.set_sensitive(False)
        return False

    def check_updates(self):
        """Ile paczek naprawdę by się zaktualizowało: symulacja full-upgrade (to samo,
        co robi przycisk) plus Flatpaki, które są zainstalowane i mają nowszą wersję."""
        sim = orka.output(["apt-get", "-s", "-o", "Debug::NoLocking=1", "full-upgrade"], 60)
        n = sum(1 for line in sim.splitlines() if line.startswith("Inst "))
        installed = set(orka.output(["flatpak", "list", "--system", "--columns=ref"], 30).split())
        newer = set(orka.output(["flatpak", "remote-ls", "--updates", "--system", "--columns=ref"], 60).split())
        n += len(installed & newer)
        GLib.idle_add(self.show_updates, n)

    def recheck_updates(self):
        self.show_updates(None)
        threading.Thread(target=self.check_updates, daemon=True).start()
        return False

    def show_updates(self, n):
        ctx = self.upd_status.get_style_context()
        btn = self.upd_btn.get_style_context()
        for c in ("dim", "ok", "warn"):
            ctx.remove_class(c)
        btn.remove_class("primary")
        btn.add_class("ghost")
        self.upd_btn.set_sensitive(False)
        if n is None:
            self.upd_status.set_text(self.t["k_checking"])
            ctx.add_class("dim")
        elif n:
            self.upd_status.set_text(self.t["upd_some"].format(n=n))
            ctx.add_class("warn")
            btn.remove_class("ghost")
            btn.add_class("primary")
            self.upd_btn.set_sensitive(not orka.IS_LIVE)
        else:
            self.upd_status.set_text(self.t["upd_none"])
            ctx.add_class("ok")
        return False

    def update_kernel(self):
        orka.run_in_terminal(self, ["sudo", "sh", "-c", APT + " update && " + APT +
                                    " install --only-upgrade -y linux-image-amd64 linux-headers-amd64"], self.t,
                             self.recheck_kernel)

    def recheck_kernel(self):
        self.show_kernel_status(self.t["k_checking"], "dim")
        threading.Thread(target=self.check_kernel, daemon=True).start()
        return False

    def clean_kernels(self):
        orka.run_in_terminal(self, ["sudo", "sh", "-c", APT + " autoremove --purge -y"], self.t)


    def page_clean(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.clean_items = {}
        home = os.path.expanduser("~")
        self.clean_defs = [
            ("c_apt", True, APT + " clean"),
            ("c_auto", True, APT + " autoremove --purge -y"),
            ("c_logs", True, "journalctl --vacuum-time=14d"),
            ("c_flatpak", True, "flatpak uninstall --unused -y --noninteractive"),
            ("c_thumbs", False, os.path.join(home, ".cache/thumbnails")),
            ("c_trash", False, os.path.join(home, ".local/share/Trash")),
        ]
        for key, _root, _what in self.clean_defs:
            row = Gtk.Box(spacing=12)
            check = Gtk.CheckButton()
            check.set_active(key != "c_trash")
            check.set_valign(Gtk.Align.CENTER)
            check.connect("toggled", lambda *_: self.update_clean_button())
            row.pack_start(check, False, False, 0)
            row.pack_start(orka.label(self.t[key], "text"), True, True, 0)
            size = orka.label("…", "dim")
            row.pack_end(size, False, False, 0)
            page.pack_start(orka.card(row), False, False, 0)
            self.clean_items[key] = (check, size)

        buttons = Gtk.Box(spacing=10)
        go = orka.button(self.t["c_clean"], "primary", self.do_clean)
        go.set_sensitive(False)
        self.clean_go = go
        self.clean_amounts = {}
        buttons.pack_start(go, False, False, 0)
        buttons.pack_start(orka.button(self.t["c_refresh"], "ghost", self.refresh_sizes), False, False, 0)
        page.pack_start(buttons, False, False, 8)
        self.clean_note = orka.label(self.t["live_only_installed"] if orka.IS_LIVE else "", "dim", wrap=True)
        page.pack_start(self.clean_note, False, False, 0)
        self.refresh_sizes()
        return page

    def refresh_sizes(self):
        for _check, size in self.clean_items.values():
            size.set_text("…")
        threading.Thread(target=self.measure, daemon=True).start()

    def measure(self):
        results = {}
        apt = sum(os.path.getsize(p) for p in glob.glob("/var/cache/apt/archives/*.deb") if os.path.isfile(p))
        results["c_apt"] = (orka.human_size(apt), apt)
        sim = orka.output(["apt-get", "-s", "autoremove"], 60)
        n = sum(1 for line in sim.splitlines() if line.startswith("Remv "))
        results["c_auto"] = (self.t["c_count"].format(n=n), n)
        cutoff = time.time() - 14 * 86400
        old = 0
        for p in glob.glob("/var/log/journal/*/*@*.journal*"):
            try:
                st = os.stat(p)
            except OSError:
                continue
            if st.st_mtime < cutoff:
                old += st.st_size
        results["c_logs"] = (orka.human_size(old), old)
        runtimes = orka.output(["flatpak", "list", "--runtime", "--columns=application"], 20).strip()
        results["c_flatpak"] = ("0", 0) if not runtimes else ("–", None)
        for key, root, what in self.clean_defs:
            if not root:
                size = orka.dir_size(what) if os.path.isdir(what) else 0
                results[key] = (orka.human_size(size), size)
        GLib.idle_add(self.show_sizes, results)

    def show_sizes(self, results):
        for key, (text, amount) in results.items():
            self.clean_items[key][1].set_text(text)
            self.clean_amounts[key] = amount
        self.update_clean_button()
        return False

    def update_clean_button(self):
        if not self.clean_amounts:
            return
        something = any(self.clean_items[k][0].get_active() and self.clean_amounts.get(k)
                        for k in self.clean_items)
        self.clean_go.set_sensitive(something and not orka.IS_LIVE)
        if not orka.IS_LIVE:
            nothing = not any(self.clean_amounts.get(k) for k in self.clean_items)
            if nothing:
                self.clean_note.set_text(self.t["c_nothing"])
            elif self.clean_note.get_text() == self.t["c_nothing"]:
                self.clean_note.set_text("")

    def do_clean(self):
        chosen = [d for d in self.clean_defs if self.clean_items[d[0]][0].get_active()]
        if not chosen or not self.confirm(self.t["c_q"], self.t["c_q2"], self.t["clean"], self.t["cancel"]):
            return
        freed = 0
        for key, root, what in chosen:
            if root:
                continue
            freed += orka.dir_size(what)
            for sub in (os.listdir(what) if os.path.isdir(what) else []):
                path = os.path.join(what, sub)
                if key == "c_trash" and sub in ("files", "info"):
                    for item in os.listdir(path):
                        target = os.path.join(path, item)
                        shutil.rmtree(target, ignore_errors=True) if os.path.isdir(target) else os.remove(target)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    try:
                        os.remove(path)
                    except OSError:
                        pass
        commands = [what for key, root, what in chosen if root]
        note = self.t["c_done"].format(size=orka.human_size(freed))
        if commands:
            note += " " + self.t["c_admin"]
            orka.run_in_terminal(self, ["sudo", "sh", "-c", "; ".join(commands)], self.t)
        self.clean_note.set_text(note)
        GLib.timeout_add(1500, lambda: self.refresh_sizes() or False)


if __name__ == "__main__":
    OrkaCentrum()
    orka.run()
