#!/usr/bin/env python3
import configparser
import glob
import json
import math
import os
import shlex
import shutil
import subprocess

import gi
from gi.repository import GLib
GLib.set_prgname("orkalinux-hello")
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

DISCORD_URL = "@ORKA_DISCORD@"
YOUTUBE_URL = "https://www.youtube.com/@_inc0gnit0"
SITE_URL = "@ORKA_URL@"
LOGO_WHITE = "/usr/share/pixmaps/orkalinux/orkalinux-logo-white.png"
AUTOSTART_FILE = os.path.expanduser("~/.config/autostart/orkalinux-hello.desktop")
LOOK_DARK = "org.orkalinux.desktop"
LOOK_LIGHT = "org.orkalinux.light.desktop"
IS_LIVE = os.path.exists("/run/live/medium")

TRANSLATIONS = {
    "pl": {
        "low_space": "Na dysku zostało tylko {free}. Programy z Flathuba potrzebują sporo miejsca (często 1-3 GB razem z bibliotekami), więc instalacja może się nie udać. Zwolnij trochę miejsca (np. Centrum > Sprzątanie albo usuń stary punkt przywracania) albo spróbuj mimo to.",
        "try_anyway": "Spróbuj mimo to",
        "title": "Witaj w OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Dzięki za wybranie OrkaLinux! To system oparty na Debianie 13 (Trixie) z pulpitem KDE Plasma. Możesz go wypróbować bez instalacji albo od razu zainstalować na dysku.",
        "welcome_text_installed": "Dzięki za zainstalowanie OrkaLinux! Fajnie, że jesteś w społeczności – mam nadzieję, że zostaniesz na dłużej. _inc0gnit0",
        "btn_readme": "Readme", "desc_readme": "Co jest w systemie",
        "btn_release": "Info o wydaniu", "desc_release": "Co nowego w @ORKA_VERSION@",
        "btn_site": "Strona projektu", "desc_site": "Pobieranie i aktualności",
        "btn_discord": "Discord", "desc_discord": "Pogadaj ze społecznością",
        "btn_youtube": "YouTube", "desc_youtube": "Mój kanał na YouTube",
        "btn_apps": "Aplikacje", "desc_apps": "Sklep z programami",
        "btn_extras": "Dodatkowe programy", "desc_extras": "Steam, OBS, GIMP i inne",
        "btn_nvidia": "Sterowniki NVIDIA", "desc_nvidia": "Pełna moc karty graficznej",
        "btn_look": "Wygląd systemu OrkaLinux", "desc_look": "Układ, kolory, tapeta, efekty",
        "btn_center": "Centrum OrkaLinux", "desc_center": "Sterowniki, jądro, sprzątanie",
        "btn_backup": "Kopia zapasowa OrkaLinux", "desc_backup": "Punkty przywracania",
        "extras_count": "Zaznaczone: {n}",
        "btn_install": "Zainstaluj OrkaLinux",
        "autostart": "Uruchamiaj przy starcie",
        "dark_mode": "Ciemny motyw",
        "close": "Zamknij",
        "cancel": "Anuluj",
        "extras_title": "Dodatkowe programy",
        "extras_intro": "Zaznacz programy, które chcesz zainstalować. Pobiorą się z Flathuba i będą się same aktualizować razem z resztą systemu (Discover).",
        "extras_install": "Zainstaluj zaznaczone",
        "installed": "zainstalowane",
        "cat_games": "Gry", "cat_create": "Tworzenie", "cat_internet": "Internet i muzyka", "cat_dev": "Praca i inne", "cat_ai": "AI",
        "nvidia_title": "Zainstalować sterownik NVIDIA?",
        "nvidia_text": "OrkaLinux zainstaluje oficjalny sterownik NVIDIA z repozytorium Debiana (ok. 500 MB do pobrania). System zapyta o Twoje hasło, a na koniec trzeba będzie uruchomić komputer ponownie.\n\nJeśli masz włączony Secure Boot, w trakcie instalacji ustawisz jednorazowe hasło do zatwierdzenia sterownika po restarcie – wszystko będzie opisane w oknie instalacji.",
        "nvidia_go": "Instaluj",
        "term_done": "Gotowe! Okno zaraz się zamknie.",
        "term_failed": "Coś poszło nie tak – zrób zrzut tego okna i wyślij mi go na Discordzie OrkaLinux. Enter zamyka okno.",
        "no_terminal": "Nie udało się otworzyć terminala.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux to dystrybucja Linuksa oparta na Debianie 13 (Trixie)\nz pulpitem KDE Plasma, stworzona przez _inc0gnit0.\n\nCo jest w systemie:\n- Firefox - przeglądarka (prosto od Mozilli)\n- Discord - komunikator (aktualizuje się sam)\n- VLC - odtwarzacz multimediów\n- LibreOffice - pakiet biurowy\n- Discover + Flathub - tysiące programów do zainstalowania\n- Drukowanie - drukarki dodasz w Ustawieniach systemowych\n- Fastfetch - informacje o systemie\n- Calamares - instalator systemu\n\nPrywatność i szybkość:\n- Bez telemetrii: system nic o Tobie nie wysyła i nie ma konta do zakładania\n- Firefox ma wyłączoną telemetrię i badania Mozilli\n- Zapora włączona od pierwszego startu\n- Poprawki bezpieczeństwa Debiana instalują się same (wyłączysz w Centrum)\n- zram zamiast wolnego swapu na dysku, więc słabszy komputer mniej się zacina\n- Żadnych reklam, kont ani zbędnych usług w tle\n\nOrkaLinux robi jedna osoba, _inc0gnit0. Jak coś nie działa albo masz pomysł,\nnapisz do mnie na Discordzie, chętnie pogadam.\n\nStrona projektu:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nSiema! Co się zmieniło od B2:\n\n- nowy wygląd, ciemny albo jasny (przełącznik na dole tego okna), tapeta zmienia się razem z nim\n- sporo nowych tapet, w tym zdjęcia EC-2\n- okna mają animacje (tak, galaretka przy przeciąganiu jest specjalnie)\n- nowy terminal: kitty, przezroczysty, z rozmyciem, smugą za kursorem i kolorowym promptem\n- Firefox prosto od Mozilli, zawsze najnowszy\n- nowsze jądro, lepiej ogarnia nowy sprzęt\n- Flathub w Discover, więc programów jest dużo więcej\n- Steam, OBS, GIMP i reszta jednym kliknięciem (Dodatkowe programy)\n- sterowniki NVIDIA da się zainstalować z Hello\n- działa drukowanie\n- Discord sam się aktualizuje\n- system jest domyślnie po angielsku, polski wybierasz w menu startowym albo w instalatorze\n\nTo dalej beta, więc coś może się wysypać. Jak coś nie działa, pisz na Discordzie:\n@ORKA_DISCORD@\n\nDzięki, że testujesz!",
    },
    "en": {
        "low_space": "Only {free} is left on the disk. Flathub apps need quite a lot of space (often 1-3 GB with their libraries), so the install may fail. Free up some space (for example Center > Cleanup, or delete an old restore point) or try anyway.",
        "try_anyway": "Try anyway",
        "title": "Welcome to OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Thanks for choosing OrkaLinux! It is based on Debian 13 (Trixie) with the KDE Plasma desktop. Try it without installing, or install it to your disk right away.",
        "welcome_text_installed": "Thanks for installing OrkaLinux! Great to have you in the community – I hope you stick around. _inc0gnit0",
        "btn_readme": "Read me", "desc_readme": "What is included",
        "btn_release": "Release info", "desc_release": "What's new in @ORKA_VERSION@",
        "btn_site": "Project website", "desc_site": "Downloads and news",
        "btn_discord": "Discord", "desc_discord": "Chat with the community",
        "btn_youtube": "YouTube", "desc_youtube": "My YouTube channel",
        "btn_apps": "Applications", "desc_apps": "Software store",
        "btn_extras": "More software", "desc_extras": "Steam, OBS, GIMP and more",
        "btn_nvidia": "NVIDIA drivers", "desc_nvidia": "Full graphics card power",
        "btn_look": "OrkaLinux Appearance", "desc_look": "Layout, colours, wallpaper, effects",
        "btn_center": "OrkaLinux Center", "desc_center": "Drivers, kernel, cleanup",
        "btn_backup": "OrkaLinux Backup", "desc_backup": "Restore points",
        "extras_count": "Selected: {n}",
        "btn_install": "Install OrkaLinux",
        "autostart": "Launch at startup",
        "dark_mode": "Dark mode",
        "close": "Close",
        "cancel": "Cancel",
        "extras_title": "More software",
        "extras_intro": "Tick the programs you want. They come from Flathub and update together with the rest of the system (Discover).",
        "extras_install": "Install selected",
        "installed": "installed",
        "cat_games": "Games", "cat_create": "Create", "cat_internet": "Internet and music", "cat_dev": "Work and more", "cat_ai": "AI",
        "nvidia_title": "Install the NVIDIA driver?",
        "nvidia_text": "OrkaLinux will install the official NVIDIA driver from the Debian repository (about 500 MB to download). You will be asked for your password, and you will need to restart your computer at the end.\n\nIf Secure Boot is on, you will set a one-time password to approve the driver after the restart – the installer window explains every step.",
        "nvidia_go": "Install",
        "term_done": "Done! This window will close in a moment.",
        "term_failed": "Something went wrong – take a screenshot of this window and send it to me on the OrkaLinux Discord. Press Enter to close.",
        "no_terminal": "Could not open the terminal.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux is a Linux distribution based on Debian 13 (Trixie)\nwith the KDE Plasma desktop, created by _inc0gnit0.\n\nWhat is included:\n- Firefox - web browser (straight from Mozilla)\n- Discord - messenger (updates itself)\n- VLC - media player\n- LibreOffice - office suite\n- Discover + Flathub - thousands of apps to install\n- Printing - add printers in System Settings\n- Fastfetch - system information\n- Calamares - system installer\n\nPrivacy and speed:\n- No telemetry: the system sends nothing about you and there is no account to make\n- Firefox has telemetry and Mozilla studies turned off\n- The firewall is on from the first start\n- Debian security fixes install by themselves (turn it off in Centrum)\n- zram instead of slow swap on disk, so older computers stutter less\n- No ads, no accounts, nothing extra running in the background\n\nOrkaLinux is made by one person, _inc0gnit0. If something doesn't work or you\nhave an idea, message me on Discord, happy to chat.\n\nProject website:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nHey! Here's what changed since B2:\n\n- new look, dark or light (switch at the bottom of this window), the wallpaper follows it\n- a bunch of new wallpapers, including EC-2 photos\n- window animations (yes, the wobbly windows are on purpose)\n- new terminal: kitty, see-through, blurred, with a cursor trail and a colourful prompt\n- Firefox straight from Mozilla, always the latest one\n- newer kernel, works better on new hardware\n- Flathub in Discover, so way more apps\n- Steam, OBS, GIMP and more in one click (Extra apps)\n- NVIDIA drivers can be installed from Hello\n- printing works\n- Discord updates itself\n- the system is in English by default, pick another language in the installer\n\nIt's still a beta, so stuff can break. If something doesn't work, tell me on Discord:\n@ORKA_DISCORD@\n\nThanks for testing!",
    },
    "de": {
        "low_space": "Auf der Festplatte sind nur noch {free} frei. Flathub-Programme brauchen viel Platz (oft 1-3 GB mit Bibliotheken), die Installation kann also fehlschlagen. Mach etwas Platz frei (z. B. Center > Aufräumen oder einen alten Wiederherstellungspunkt löschen) oder versuch es trotzdem.",
        "try_anyway": "Trotzdem versuchen",
        "title": "Willkommen bei OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Danke, dass Sie OrkaLinux gewählt haben! Es basiert auf Debian 13 (Trixie) mit dem KDE Plasma Desktop. Sie können es ohne Installation testen oder direkt installieren.",
        "welcome_text_installed": "Danke für die Installation von OrkaLinux! Schön, dass Sie dabei sind – ich hoffe, Sie bleiben lange. _inc0gnit0",
        "btn_readme": "Readme", "desc_readme": "Was enthalten ist",
        "btn_release": "Versionshinweise", "desc_release": "Neu in @ORKA_VERSION@",
        "btn_site": "Projektseite", "desc_site": "Downloads und News",
        "btn_discord": "Discord", "desc_discord": "Mit der Community chatten",
        "btn_youtube": "YouTube", "desc_youtube": "Mein YouTube-Kanal",
        "btn_apps": "Anwendungen", "desc_apps": "Software-Store",
        "btn_extras": "Weitere Programme", "desc_extras": "Steam, OBS, GIMP und mehr",
        "btn_nvidia": "NVIDIA-Treiber", "desc_nvidia": "Volle Grafikleistung",
        "btn_look": "OrkaLinux Aussehen", "desc_look": "Layout, Farben, Hintergrund, Effekte",
        "btn_center": "OrkaLinux Zentrum", "desc_center": "Treiber, Kernel, Aufräumen",
        "btn_backup": "OrkaLinux Sicherung", "desc_backup": "Wiederherstellungspunkte",
        "extras_count": "Ausgewählt: {n}",
        "btn_install": "OrkaLinux installieren",
        "autostart": "Beim Start ausführen",
        "dark_mode": "Dunkler Modus",
        "close": "Schließen",
        "cancel": "Abbrechen",
        "extras_title": "Weitere Programme",
        "extras_intro": "Wählen Sie die Programme aus, die Sie installieren möchten. Sie kommen von Flathub und werden mit dem restlichen System aktualisiert (Discover).",
        "extras_install": "Auswahl installieren",
        "installed": "installiert",
        "cat_games": "Spiele", "cat_create": "Kreativ", "cat_internet": "Internet und Musik", "cat_dev": "Arbeit und mehr", "cat_ai": "KI",
        "nvidia_title": "NVIDIA-Treiber installieren?",
        "nvidia_text": "OrkaLinux installiert den offiziellen NVIDIA-Treiber aus dem Debian-Repository (ca. 500 MB Download). Sie werden nach Ihrem Passwort gefragt und müssen den Computer am Ende neu starten.\n\nWenn Secure Boot aktiv ist, legen Sie ein Einmal-Passwort fest, um den Treiber nach dem Neustart zu bestätigen – das Installationsfenster erklärt jeden Schritt.",
        "nvidia_go": "Installieren",
        "term_done": "Fertig! Das Fenster schließt sich gleich.",
        "term_failed": "Etwas ist schiefgelaufen – machen Sie einen Screenshot und schicken Sie ihn mir im OrkaLinux-Discord. Enter schließt das Fenster.",
        "no_terminal": "Das Terminal konnte nicht geöffnet werden.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux ist eine Linux-Distribution basierend auf Debian 13\nmit dem KDE Plasma Desktop.\n\nPrivatsphäre und Tempo:\n- Keine Telemetrie: Das System sendet nichts über dich, und es gibt kein Konto anzulegen\n- In Firefox sind Telemetrie und Mozilla-Studien aus\n- Die Firewall ist ab dem ersten Start an\n- Debian-Sicherheitskorrekturen installieren sich selbst (abschaltbar im Center)\n- zram statt langsamem Swap auf der Platte, ältere Rechner ruckeln weniger\n- Keine Werbung, keine Konten, nichts Überflüssiges im Hintergrund\n\nOrkaLinux wird von einer Person gemacht: _inc0gnit0. Wenn etwas nicht klappt\noder Sie eine Idee haben, schreiben Sie mir auf Discord.\n\nProjektseite:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nHi! Das ist neu seit B2:\n\n- neues Design, dunkel oder hell (Schalter unten in diesem Fenster), das Hintergrundbild passt sich an\n- viele neue Hintergrundbilder\n- Fensteranimationen\n- neues Terminal: kitty, durchsichtig, mit Unschärfe und Cursor-Spur\n- Firefox direkt von Mozilla, immer die neueste Version\n- neuerer Kernel für neue Hardware\n- Flathub in Discover\n- Steam, OBS, GIMP und mehr mit einem Klick\n- NVIDIA-Treiber direkt aus Hello\n- Drucken funktioniert\n- Discord aktualisiert sich selbst\n\nIst noch eine Beta, also kann etwas kaputtgehen. Probleme bitte auf Discord melden:\n@ORKA_DISCORD@\n\nDanke fürs Testen!",
    },
    "fr": {
        "low_space": "Il ne reste que {free} sur le disque. Les applis Flathub prennent beaucoup de place (souvent 1-3 Go avec leurs bibliothèques), l'installation peut donc échouer. Libère de la place (par exemple Centre > Nettoyage, ou supprime un ancien point de restauration) ou essaie quand même.",
        "try_anyway": "Essayer quand même",
        "title": "Bienvenue sur OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Merci d'avoir choisi OrkaLinux! Il est basé sur Debian 13 (Trixie) avec le bureau KDE Plasma. Essayez-le sans installation ou installez-le directement.",
        "welcome_text_installed": "Merci d'avoir installé OrkaLinux ! Ravi que vous fassiez partie de la communauté – j'espère que vous resterez longtemps. _inc0gnit0",
        "btn_readme": "Lisez-moi", "desc_readme": "Ce qui est inclus",
        "btn_release": "Notes de version", "desc_release": "Nouveautés de @ORKA_VERSION@",
        "btn_site": "Site du projet", "desc_site": "Téléchargements et actus",
        "btn_discord": "Discord", "desc_discord": "Discuter avec la communauté",
        "btn_youtube": "YouTube", "desc_youtube": "Ma chaîne YouTube",
        "btn_apps": "Applications", "desc_apps": "Logithèque",
        "btn_extras": "Plus de logiciels", "desc_extras": "Steam, OBS, GIMP et plus",
        "btn_nvidia": "Pilotes NVIDIA", "desc_nvidia": "Toute la puissance graphique",
        "btn_look": "Apparence OrkaLinux", "desc_look": "Disposition, couleurs, fond, effets",
        "btn_center": "Centre OrkaLinux", "desc_center": "Pilotes, noyau, nettoyage",
        "btn_backup": "Sauvegarde OrkaLinux", "desc_backup": "Points de restauration",
        "extras_count": "Sélection : {n}",
        "btn_install": "Installer OrkaLinux",
        "autostart": "Lancer au démarrage",
        "dark_mode": "Mode sombre",
        "close": "Fermer",
        "cancel": "Annuler",
        "extras_title": "Plus de logiciels",
        "extras_intro": "Cochez les logiciels à installer. Ils viennent de Flathub et se mettent à jour avec le reste du système (Discover).",
        "extras_install": "Installer la sélection",
        "installed": "installé",
        "cat_games": "Jeux", "cat_create": "Création", "cat_internet": "Internet et musique", "cat_dev": "Travail et plus", "cat_ai": "IA",
        "nvidia_title": "Installer le pilote NVIDIA ?",
        "nvidia_text": "OrkaLinux va installer le pilote NVIDIA officiel depuis le dépôt Debian (environ 500 Mo à télécharger). Votre mot de passe sera demandé et il faudra redémarrer l'ordinateur à la fin.\n\nSi Secure Boot est activé, vous choisirez un mot de passe temporaire pour valider le pilote après le redémarrage – la fenêtre d'installation explique chaque étape.",
        "nvidia_go": "Installer",
        "term_done": "Terminé ! La fenêtre va se fermer.",
        "term_failed": "Une erreur s'est produite – faites une capture de cette fenêtre et envoyez-la-moi sur le Discord OrkaLinux. Entrée ferme la fenêtre.",
        "no_terminal": "Impossible d'ouvrir le terminal.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux est une distribution Linux basée sur Debian 13\navec le bureau KDE Plasma.\n\nVie privée et vitesse :\n- Pas de télémétrie : le système n'envoie rien sur vous et il n'y a aucun compte à créer\n- Firefox a la télémétrie et les études Mozilla désactivées\n- Le pare-feu est actif dès le premier démarrage\n- Les correctifs de sécurité Debian s'installent seuls (désactivable dans le Centre)\n- zram au lieu d'un swap lent sur disque, les vieux PC rament moins\n- Pas de pubs, pas de comptes, rien de superflu en arrière-plan\n\nOrkaLinux est fait par une seule personne, _inc0gnit0. Si quelque chose ne marche\npas ou si vous avez une idée, écrivez-moi sur Discord.\n\nSite du projet:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nSalut ! Voici ce qui a changé depuis B2 :\n\n- nouveau look, sombre ou clair (bouton en bas de cette fenêtre), le fond d'écran suit\n- plein de nouveaux fonds d'écran\n- animations des fenêtres\n- nouveau terminal : kitty, transparent, avec flou et traînée du curseur\n- Firefox directement de Mozilla, toujours à jour\n- noyau plus récent pour le matériel récent\n- Flathub dans Discover\n- Steam, OBS, GIMP et plus en un clic\n- pilotes NVIDIA depuis Hello\n- l'impression fonctionne\n- Discord se met à jour tout seul\n\nC'est encore une bêta, donc des bugs sont possibles. Signale-les sur Discord :\n@ORKA_DISCORD@\n\nMerci de tester !",
    },
    "es": {
        "low_space": "Solo quedan {free} en el disco. Las aplicaciones de Flathub ocupan bastante (a menudo 1-3 GB con sus bibliotecas), así que la instalación puede fallar. Libera algo de espacio (por ejemplo Centro > Limpieza, o borra un punto de restauración antiguo) o inténtalo de todos modos.",
        "try_anyway": "Intentar igualmente",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "title": "¡Bienvenido a OrkaLinux!",
        "welcome_text_live": "¡Gracias por elegir OrkaLinux! Está basado en Debian 13 (Trixie) con el escritorio KDE Plasma. Pruébalo sin instalar o instálalo en tu disco ahora mismo.",
        "welcome_text_installed": "¡Gracias por instalar OrkaLinux! Me alegra tenerte en la comunidad, espero que te quedes. _inc0gnit0",
        "btn_readme": "Léeme",
        "desc_readme": "Qué incluye",
        "btn_release": "Notas de la versión",
        "desc_release": "Novedades de @ORKA_VERSION@",
        "btn_site": "Web del proyecto",
        "desc_site": "Descargas y noticias",
        "btn_discord": "Discord",
        "desc_discord": "Habla con la comunidad",
        "btn_youtube": "YouTube",
        "desc_youtube": "Mi canal de YouTube",
        "btn_apps": "Aplicaciones",
        "desc_apps": "Tienda de software",
        "btn_extras": "Más programas",
        "desc_extras": "Steam, OBS, GIMP y más",
        "btn_nvidia": "Drivers NVIDIA",
        "desc_nvidia": "Toda la potencia de la gráfica",
        "btn_look": "Apariencia de OrkaLinux",
        "desc_look": "Diseño, colores, fondo, efectos",
        "btn_center": "Centro OrkaLinux",
        "desc_center": "Drivers, kernel, limpieza",
        "btn_backup": "Copia de seguridad OrkaLinux",
        "desc_backup": "Puntos de restauración",
        "extras_count": "Seleccionados: {n}",
        "btn_install": "Instalar OrkaLinux",
        "autostart": "Abrir al iniciar",
        "dark_mode": "Modo oscuro",
        "close": "Cerrar",
        "cancel": "Cancelar",
        "extras_title": "Más programas",
        "extras_intro": "Marca los programas que quieras. Vienen de Flathub y se actualizan junto con el resto del sistema (Discover).",
        "extras_install": "Instalar seleccionados",
        "installed": "instalado",
        "cat_games": "Juegos",
        "cat_create": "Crear",
        "cat_internet": "Internet y música",
        "cat_dev": "Trabajo y más",
        "cat_ai": "IA",
        "nvidia_title": "¿Instalar el driver de NVIDIA?",
        "nvidia_text": "OrkaLinux instalará el driver oficial de NVIDIA desde el repositorio de Debian (unos 500 MB de descarga). Se te pedirá tu contraseña y al final tendrás que reiniciar el ordenador.\n\nSi Secure Boot está activado, pondrás una contraseña de un solo uso para aprobar el driver después de reiniciar; la ventana del instalador explica cada paso.",
        "nvidia_go": "Instalar",
        "term_done": "¡Listo! Esta ventana se cerrará en un momento.",
        "term_failed": "Algo salió mal. Haz una captura de esta ventana y envíamela por el Discord de OrkaLinux. Pulsa Enter para cerrar.",
        "no_terminal": "No se pudo abrir la terminal.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux es una distribución de Linux basada en Debian 13 (Trixie)\ncon el escritorio KDE Plasma, creada por _inc0gnit0.\n\nQué incluye:\n- Firefox - navegador (directo de Mozilla)\n- Discord - mensajería (se actualiza solo)\n- VLC - reproductor multimedia\n- LibreOffice - ofimática\n- Discover + Flathub - miles de aplicaciones para instalar\n- Impresión - añade impresoras en la Configuración del sistema\n- Fastfetch - información del sistema\n- Calamares - instalador del sistema\n\nPrivacidad y velocidad:\n- Sin telemetría: el sistema no envía nada sobre ti y no hay que crear ninguna cuenta\n- Firefox tiene la telemetría y los estudios de Mozilla desactivados\n- El cortafuegos está activo desde el primer arranque\n- Los parches de seguridad de Debian se instalan solos (se desactiva en el Centro)\n- zram en lugar de swap lento en disco, así los ordenadores viejos van más fluidos\n- Sin anuncios, sin cuentas, nada de más en segundo plano\n\nOrkaLinux lo hace una sola persona, _inc0gnit0. Si algo no funciona o tienes\nuna idea, escríbeme por Discord, encantado de hablar.\n\nWeb del proyecto:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\n¡Hola! Esto es lo que ha cambiado desde B2:\n\n- nuevo aspecto, oscuro o claro (interruptor abajo en esta ventana), el fondo lo sigue\n- un montón de fondos nuevos, incluidas fotos de EC-2\n- animaciones de ventanas (sí, las ventanas gelatinosas son a propósito)\n- nueva terminal: kitty, transparente, con desenfoque, estela del cursor y un prompt de colores\n- Firefox directo de Mozilla, siempre el más nuevo\n- kernel más nuevo, funciona mejor en hardware reciente\n- Flathub en Discover, muchas más aplicaciones\n- Steam, OBS, GIMP y más con un clic (Más programas)\n- los drivers de NVIDIA se instalan desde Hello\n- la impresión funciona\n- Discord se actualiza solo\n- el sistema viene en inglés, elige otro idioma en el instalador\n\nSigue siendo una beta, así que algo puede fallar. Si algo no funciona, dímelo en Discord:\n@ORKA_DISCORD@\n\n¡Gracias por probarlo!",
    },
    "it": {
        "low_space": "Sul disco restano solo {free}. Le app di Flathub occupano parecchio spazio (spesso 1-3 GB con le librerie), quindi l'installazione potrebbe fallire. Libera un po' di spazio (per esempio Centro > Pulizia, o elimina un vecchio punto di ripristino) oppure prova lo stesso.",
        "try_anyway": "Prova lo stesso",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "title": "Benvenuto in OrkaLinux!",
        "welcome_text_live": "Grazie per aver scelto OrkaLinux! È basato su Debian 13 (Trixie) con il desktop KDE Plasma. Provalo senza installare, oppure installalo subito sul disco.",
        "welcome_text_installed": "Grazie per aver installato OrkaLinux! Che bello averti nella community, spero che resterai. _inc0gnit0",
        "btn_readme": "Leggimi",
        "desc_readme": "Cosa c'è dentro",
        "btn_release": "Note di rilascio",
        "desc_release": "Novità in @ORKA_VERSION@",
        "btn_site": "Sito del progetto",
        "desc_site": "Download e novità",
        "btn_discord": "Discord",
        "desc_discord": "Parla con la community",
        "btn_youtube": "YouTube",
        "desc_youtube": "Il mio canale YouTube",
        "btn_apps": "Applicazioni",
        "desc_apps": "Negozio di software",
        "btn_extras": "Altri programmi",
        "desc_extras": "Steam, OBS, GIMP e altro",
        "btn_nvidia": "Driver NVIDIA",
        "desc_nvidia": "Tutta la potenza della scheda video",
        "btn_look": "Aspetto di OrkaLinux",
        "desc_look": "Layout, colori, sfondo, effetti",
        "btn_center": "Centro OrkaLinux",
        "desc_center": "Driver, kernel, pulizia",
        "btn_backup": "Backup di OrkaLinux",
        "desc_backup": "Punti di ripristino",
        "extras_count": "Selezionati: {n}",
        "btn_install": "Installa OrkaLinux",
        "autostart": "Apri all'avvio",
        "dark_mode": "Modalità scura",
        "close": "Chiudi",
        "cancel": "Annulla",
        "extras_title": "Altri programmi",
        "extras_intro": "Spunta i programmi che vuoi. Arrivano da Flathub e si aggiornano insieme al resto del sistema (Discover).",
        "extras_install": "Installa selezionati",
        "installed": "installato",
        "cat_games": "Giochi",
        "cat_create": "Creare",
        "cat_internet": "Internet e musica",
        "cat_dev": "Lavoro e altro",
        "cat_ai": "IA",
        "nvidia_title": "Installare il driver NVIDIA?",
        "nvidia_text": "OrkaLinux installerà il driver ufficiale NVIDIA dal repository di Debian (circa 500 MB da scaricare). Ti verrà chiesta la password e alla fine dovrai riavviare il computer.\n\nSe Secure Boot è attivo, imposterai una password usa e getta per approvare il driver dopo il riavvio; la finestra dell'installer spiega ogni passaggio.",
        "nvidia_go": "Installa",
        "term_done": "Fatto! Questa finestra si chiuderà tra un attimo.",
        "term_failed": "Qualcosa è andato storto. Fai uno screenshot di questa finestra e mandamelo sul Discord di OrkaLinux. Premi Invio per chiudere.",
        "no_terminal": "Impossibile aprire il terminale.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux è una distribuzione Linux basata su Debian 13 (Trixie)\ncon il desktop KDE Plasma, creata da _inc0gnit0.\n\nCosa c'è dentro:\n- Firefox - browser (direttamente da Mozilla)\n- Discord - messaggistica (si aggiorna da solo)\n- VLC - lettore multimediale\n- LibreOffice - suite per l'ufficio\n- Discover + Flathub - migliaia di app da installare\n- Stampa - aggiungi le stampanti nelle Impostazioni di sistema\n- Fastfetch - informazioni sul sistema\n- Calamares - installer del sistema\n\nPrivacy e velocità:\n- Niente telemetria: il sistema non invia nulla su di te e non c'è nessun account da creare\n- Firefox ha telemetria e studi di Mozilla disattivati\n- Il firewall è attivo dal primo avvio\n- Le patch di sicurezza di Debian si installano da sole (si disattiva nel Centro)\n- zram al posto dello swap lento su disco, così i computer vecchi scattano meno\n- Niente pubblicità, niente account, niente di superfluo in background\n\nOrkaLinux è fatto da una sola persona, _inc0gnit0. Se qualcosa non va o hai\nun'idea, scrivimi su Discord, ne parlo volentieri.\n\nSito del progetto:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nCiao! Ecco cosa è cambiato dalla B2:\n\n- nuovo aspetto, scuro o chiaro (interruttore in fondo a questa finestra), lo sfondo lo segue\n- un sacco di nuovi sfondi, comprese le foto EC-2\n- animazioni delle finestre (sì, le finestre gommose sono volute)\n- nuovo terminale: kitty, trasparente, sfocato, con la scia del cursore e un prompt colorato\n- Firefox direttamente da Mozilla, sempre l'ultimo\n- kernel più nuovo, va meglio sull'hardware recente\n- Flathub in Discover, molte più app\n- Steam, OBS, GIMP e altro con un clic (Altri programmi)\n- i driver NVIDIA si installano da Hello\n- la stampa funziona\n- Discord si aggiorna da solo\n- il sistema è in inglese, scegli un'altra lingua nell'installer\n\nÈ ancora una beta, quindi qualcosa può rompersi. Se qualcosa non va, dimmelo su Discord:\n@ORKA_DISCORD@\n\nGrazie per i test!",
    },
    "pt": {
        "low_space": "Só restam {free} no disco. Os aplicativos do Flathub ocupam bastante espaço (muitas vezes 1-3 GB com as bibliotecas), então a instalação pode falhar. Libere espaço (por exemplo Central > Limpeza, ou apague um ponto de restauração antigo) ou tente mesmo assim.",
        "try_anyway": "Tentar mesmo assim",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "title": "Bem-vindo ao OrkaLinux!",
        "welcome_text_live": "Obrigado por escolher o OrkaLinux! Ele é baseado no Debian 13 (Trixie) com o desktop KDE Plasma. Experimente sem instalar ou instale no seu disco agora mesmo.",
        "welcome_text_installed": "Obrigado por instalar o OrkaLinux! Que bom ter você na comunidade, espero que fique. _inc0gnit0",
        "btn_readme": "Leia-me",
        "desc_readme": "O que vem incluído",
        "btn_release": "Notas da versão",
        "desc_release": "Novidades da @ORKA_VERSION@",
        "btn_site": "Site do projeto",
        "desc_site": "Downloads e novidades",
        "btn_discord": "Discord",
        "desc_discord": "Converse com a comunidade",
        "btn_youtube": "YouTube",
        "desc_youtube": "Meu canal no YouTube",
        "btn_apps": "Aplicativos",
        "desc_apps": "Loja de programas",
        "btn_extras": "Mais programas",
        "desc_extras": "Steam, OBS, GIMP e mais",
        "btn_nvidia": "Drivers NVIDIA",
        "desc_nvidia": "Toda a força da placa de vídeo",
        "btn_look": "Aparência do OrkaLinux",
        "desc_look": "Layout, cores, papel de parede, efeitos",
        "btn_center": "Central OrkaLinux",
        "desc_center": "Drivers, kernel, limpeza",
        "btn_backup": "Backup do OrkaLinux",
        "desc_backup": "Pontos de restauração",
        "extras_count": "Selecionados: {n}",
        "btn_install": "Instalar OrkaLinux",
        "autostart": "Abrir ao iniciar",
        "dark_mode": "Modo escuro",
        "close": "Fechar",
        "cancel": "Cancelar",
        "extras_title": "Mais programas",
        "extras_intro": "Marque os programas que quiser. Eles vêm do Flathub e são atualizados junto com o resto do sistema (Discover).",
        "extras_install": "Instalar selecionados",
        "installed": "instalado",
        "cat_games": "Jogos",
        "cat_create": "Criar",
        "cat_internet": "Internet e música",
        "cat_dev": "Trabalho e mais",
        "cat_ai": "IA",
        "nvidia_title": "Instalar o driver NVIDIA?",
        "nvidia_text": "O OrkaLinux vai instalar o driver oficial da NVIDIA a partir do repositório do Debian (cerca de 500 MB para baixar). Sua senha será pedida e no final você precisará reiniciar o computador.\n\nSe o Secure Boot estiver ligado, você vai definir uma senha de uso único para aprovar o driver depois de reiniciar; a janela do instalador explica cada passo.",
        "nvidia_go": "Instalar",
        "term_done": "Pronto! Esta janela vai fechar em instantes.",
        "term_failed": "Algo deu errado. Tire um print desta janela e mande para mim no Discord do OrkaLinux. Aperte Enter para fechar.",
        "no_terminal": "Não foi possível abrir o terminal.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nO OrkaLinux é uma distribuição Linux baseada no Debian 13 (Trixie)\ncom o desktop KDE Plasma, criada por _inc0gnit0.\n\nO que vem incluído:\n- Firefox - navegador (direto da Mozilla)\n- Discord - mensagens (atualiza sozinho)\n- VLC - player de mídia\n- LibreOffice - pacote de escritório\n- Discover + Flathub - milhares de aplicativos para instalar\n- Impressão - adicione impressoras nas Configurações do sistema\n- Fastfetch - informações do sistema\n- Calamares - instalador do sistema\n\nPrivacidade e velocidade:\n- Sem telemetria: o sistema não envia nada sobre você e não há conta para criar\n- O Firefox está com telemetria e estudos da Mozilla desligados\n- O firewall fica ligado desde o primeiro início\n- As correções de segurança do Debian se instalam sozinhas (dá para desligar na Central)\n- zram no lugar de swap lento em disco, então computadores antigos travam menos\n- Sem anúncios, sem contas, nada sobrando em segundo plano\n\nO OrkaLinux é feito por uma pessoa só, _inc0gnit0. Se algo não funcionar ou você\ntiver uma ideia, fale comigo no Discord, vou gostar de conversar.\n\nSite do projeto:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nOi! Veja o que mudou desde a B2:\n\n- visual novo, escuro ou claro (botão no rodapé desta janela), o papel de parede acompanha\n- vários papéis de parede novos, incluindo fotos do EC-2\n- animações de janelas (sim, as janelas gelatinosas são de propósito)\n- terminal novo: kitty, transparente, com desfoque, rastro do cursor e prompt colorido\n- Firefox direto da Mozilla, sempre o mais novo\n- kernel mais novo, funciona melhor em hardware recente\n- Flathub no Discover, muito mais aplicativos\n- Steam, OBS, GIMP e mais em um clique (Mais programas)\n- os drivers NVIDIA se instalam pelo Hello\n- a impressão funciona\n- o Discord se atualiza sozinho\n- o sistema vem em inglês, escolha outro idioma no instalador\n\nAinda é uma beta, então algo pode quebrar. Se algo não funcionar, me avise no Discord:\n@ORKA_DISCORD@\n\nValeu por testar!",
    },
    "uk": {
        "low_space": "На диску залишилося лише {free}. Програми з Flathub займають багато місця (часто 1-3 ГБ разом із бібліотеками), тож встановлення може не вдатися. Звільніть трохи місця (наприклад, Центр > Очищення або видаліть стару точку відновлення) або спробуйте все одно.",
        "try_anyway": "Спробувати все одно",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "title": "Ласкаво просимо до OrkaLinux!",
        "welcome_text_live": "Дякую, що обрали OrkaLinux! Він базується на Debian 13 (Trixie) з робочим столом KDE Plasma. Спробуйте без встановлення або встановіть на диск одразу.",
        "welcome_text_installed": "Дякую, що встановили OrkaLinux! Радий бачити вас у спільноті, сподіваюся, ви залишитеся. _inc0gnit0",
        "btn_readme": "Прочитай мене",
        "desc_readme": "Що всередині",
        "btn_release": "Про випуск",
        "desc_release": "Що нового в @ORKA_VERSION@",
        "btn_site": "Сайт проєкту",
        "desc_site": "Завантаження та новини",
        "btn_discord": "Discord",
        "desc_discord": "Спілкування зі спільнотою",
        "btn_youtube": "YouTube",
        "desc_youtube": "Мій канал на YouTube",
        "btn_apps": "Програми",
        "desc_apps": "Магазин програм",
        "btn_extras": "Більше програм",
        "desc_extras": "Steam, OBS, GIMP та інше",
        "btn_nvidia": "Драйвери NVIDIA",
        "desc_nvidia": "Уся потужність відеокарти",
        "btn_look": "Вигляд OrkaLinux",
        "desc_look": "Розташування, кольори, шпалери, ефекти",
        "btn_center": "Центр OrkaLinux",
        "desc_center": "Драйвери, ядро, очищення",
        "btn_backup": "Резервні копії OrkaLinux",
        "desc_backup": "Точки відновлення",
        "extras_count": "Вибрано: {n}",
        "btn_install": "Встановити OrkaLinux",
        "autostart": "Запускати при старті",
        "dark_mode": "Темна тема",
        "close": "Закрити",
        "cancel": "Скасувати",
        "extras_title": "Більше програм",
        "extras_intro": "Позначте програми, які хочете. Вони беруться з Flathub і оновлюються разом з рештою системи (Discover).",
        "extras_install": "Встановити вибрані",
        "installed": "встановлено",
        "cat_games": "Ігри",
        "cat_create": "Творчість",
        "cat_internet": "Інтернет і музика",
        "cat_dev": "Робота та інше",
        "cat_ai": "ШІ",
        "nvidia_title": "Встановити драйвер NVIDIA?",
        "nvidia_text": "OrkaLinux встановить офіційний драйвер NVIDIA з репозиторію Debian (близько 500 МБ завантаження). Вас попросять ввести пароль, а наприкінці потрібно буде перезавантажити комп'ютер.\n\nЯкщо Secure Boot увімкнено, ви задасте одноразовий пароль, щоб підтвердити драйвер після перезавантаження; вікно встановлювача пояснює кожен крок.",
        "nvidia_go": "Встановити",
        "term_done": "Готово! Це вікно зараз закриється.",
        "term_failed": "Щось пішло не так. Зробіть знімок цього вікна й надішліть мені в Discord OrkaLinux. Натисніть Enter, щоб закрити.",
        "no_terminal": "Не вдалося відкрити термінал.",
        "readme_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n================================\n\nOrkaLinux - це дистрибутив Linux на основі Debian 13 (Trixie)\nз робочим столом KDE Plasma, створений _inc0gnit0.\n\nЩо всередині:\n- Firefox - браузер (напряму від Mozilla)\n- Discord - месенджер (оновлюється сам)\n- VLC - медіаплеєр\n- LibreOffice - офісний пакет\n- Discover + Flathub - тисячі програм для встановлення\n- Друк - принтери додаються в Налаштуваннях системи\n- Fastfetch - інформація про систему\n- Calamares - встановлювач системи\n\nПриватність і швидкість:\n- Без телеметрії: система нічого про вас не надсилає, і не треба створювати жодних акаунтів\n- У Firefox вимкнено телеметрію та дослідження Mozilla\n- Брандмауер увімкнено з першого запуску\n- Виправлення безпеки Debian встановлюються самі (вимикається в Центрі)\n- zram замість повільного swap на диску, тож старі комп'ютери менше гальмують\n- Жодної реклами, акаунтів і зайвого у фоні\n\nOrkaLinux робить одна людина, _inc0gnit0. Якщо щось не працює або у вас\nє ідея, напишіть мені в Discord, буду радий поговорити.\n\nСайт проєкту:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@)\n\nПривіт! Ось що змінилося з B2:\n\n- новий вигляд, темний або світлий (перемикач унизу цього вікна), шпалери змінюються разом з ним\n- купа нових шпалер, зокрема фото EC-2\n- анімації вікон (так, желейні вікна - це навмисно)\n- новий термінал: kitty, прозорий, з розмиттям, слідом курсора й кольоровим рядком\n- Firefox напряму від Mozilla, завжди найновіший\n- новіше ядро, краще працює на новому залізі\n- Flathub у Discover, набагато більше програм\n- Steam, OBS, GIMP та інше в один клік (Більше програм)\n- драйвери NVIDIA встановлюються з Hello\n- друк працює\n- Discord оновлюється сам\n- система англійською за замовчуванням, іншу мову оберіть у встановлювачі\n\nЦе все ще бета, тож щось може зламатися. Якщо щось не працює, напишіть мені в Discord:\n@ORKA_DISCORD@\n\nДякую за тестування!",
    },
}

LANG_FILE = os.path.expanduser("~/.config/orkalinux/lang")
LOCALES = {
    "pl": "pl_PL.UTF-8", "en": "en_US.UTF-8", "de": "de_DE.UTF-8", "fr": "fr_FR.UTF-8",
    "es": "es_ES.UTF-8", "it": "it_IT.UTF-8", "pt": "pt_BR.UTF-8", "uk": "uk_UA.UTF-8",
}

LANG_NAMES = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "uk": "Українська",
}

EXTRAS_FILE = "/usr/share/orkalinux/extras.json"
EXTRAS_ICONS = "/usr/share/orkalinux/extras-icons"
ORKA_APPS = "/usr/share/{0}/{0}.py"


EXTRAS_SCRIPTS = "/usr/share/orkalinux/extras"


def load_extras():
    try:
        with open(EXTRAS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


WAVES = [
    (10.0, 150.0, 0.45, 0.56, (0.055, 0.070, 0.420), 0.80),
    (13.0, 220.0, -0.30, 0.70, (0.115, 0.086, 0.660), 0.85),
    (8.0, 105.0, 0.70, 0.84, (0.205, 0.122, 0.790), 0.92),
]

CSS = b"""
window.orka { background-color: #070b26; }

.hero-title { color: #ffffff; font-size: 26px; font-weight: 800; }
.hero-sub { color: rgba(255, 255, 255, 0.70); font-size: 12px; }

.welcome { color: #c9d1ff; font-size: 13px; }

button.card {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: none;
    text-shadow: none;
    -gtk-icon-shadow: none;
    transition: all 220ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
button.card:hover {
    background-color: rgba(90, 110, 255, 0.18);
    border-color: rgba(140, 155, 255, 0.60);
    box-shadow: 0 6px 18px rgba(20, 30, 160, 0.45);
}
button.card:active { background-color: rgba(90, 110, 255, 0.32); }
button.card image {
    -gtk-icon-transform: scale(1);
    transition: -gtk-icon-transform 220ms ease-out;
}
button.card:hover image { -gtk-icon-transform: scale(1.18); }
.card-title { color: #ffffff; font-weight: bold; font-size: 14px; }
.card-desc { color: rgba(255, 255, 255, 0.60); font-size: 11px; }

button.install {
    background-image: linear-gradient(90deg, #2b3bff, #6a2bff);
    color: #ffffff;
    border: none;
    border-radius: 14px;
    padding: 12px 34px;
    font-size: 15px;
    font-weight: bold;
    text-shadow: none;
    box-shadow: 0 4px 14px rgba(60, 70, 255, 0.35);
    transition: all 250ms ease-out;
}
button.install label { color: #ffffff; }
button.install:hover {
    background-image: linear-gradient(90deg, #4050ff, #7d45ff);
    box-shadow: 0 8px 28px rgba(100, 110, 255, 0.70);
}

button.primary {
    background-image: linear-gradient(90deg, #2b3bff, #6a2bff);
    border: none;
    border-radius: 10px;
    padding: 6px 20px;
    text-shadow: none;
    box-shadow: none;
}
button.primary label { color: #ffffff; font-weight: bold; }
button.primary:hover { background-image: linear-gradient(90deg, #4050ff, #7d45ff); }
button.primary:disabled { background-image: none; background-color: rgba(255, 255, 255, 0.08); }
button.primary:disabled label { color: rgba(255, 255, 255, 0.35); }

.footer { background-color: #050820; border-top: 1px solid rgba(255, 255, 255, 0.08); }
.footer label { color: rgba(255, 255, 255, 0.75); }
switch { border-radius: 14px; background-image: none; background-color: rgba(255, 255, 255, 0.15); border: none; transition: all 200ms ease-out; }
switch:checked { background-color: #3b4bff; }
switch slider { border-radius: 14px; background-image: none; background-color: #ffffff; border: none; box-shadow: none; }

button.ghost {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.08);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 6px 20px;
    text-shadow: none;
    box-shadow: none;
    transition: all 200ms ease-out;
}
button.ghost label { color: #ffffff; }
button.ghost:hover { background-color: rgba(255, 255, 255, 0.16); }

combobox button {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.10);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.20);
    border-radius: 10px;
    text-shadow: none;
    box-shadow: none;
}
combobox button label, combobox arrow { color: #ffffff; }

.doc-title { color: #ffffff; font-size: 20px; font-weight: 800; }
scrolledwindow.doc {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
}
scrolledwindow.doc viewport { background-color: transparent; }
.doc-text { color: #dfe4ff; font-size: 13px; }
dialog.orka, dialog.orka box, dialog.orka scrolledwindow, dialog.orka viewport { background-color: #0b1033; }
dialog.orka label { color: #e3e7ff; font-family: monospace; }

dialog.picker, dialog.picker box, dialog.picker scrolledwindow, dialog.picker viewport { background-color: #0b1033; }
dialog.picker label { color: #e3e7ff; }
.picker-intro { color: #c9d1ff; font-size: 13px; }
.picker-cat { color: #8f9cff; font-weight: bold; font-size: 13px; }
.picker-name { color: #ffffff; font-weight: bold; }
.picker-desc { color: rgba(255, 255, 255, 0.55); font-size: 11px; }
.picker-count { color: #c9d1ff; font-weight: bold; }

button.app-tile {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 14px 8px 12px 8px;
    box-shadow: none;
    text-shadow: none;
    transition: all 180ms ease-out;
}
button.app-tile:hover { background-color: rgba(90, 110, 255, 0.14); border-color: rgba(140, 155, 255, 0.45); }
button.app-tile:checked {
    background-color: rgba(79, 88, 240, 0.30);
    border-color: #8a93ff;
    box-shadow: 0 0 0 1px #8a93ff, 0 6px 18px rgba(40, 50, 200, 0.45);
}
button.app-tile:disabled { background-color: rgba(255, 255, 255, 0.03); border-color: rgba(255, 255, 255, 0.05); }
button.app-tile:disabled .picker-name { color: rgba(255, 255, 255, 0.55); }
.tile-mark { background-color: #4f58f0; color: #ffffff; border-radius: 11px; font-weight: bold; font-size: 11px; padding: 1px 6px; }
.tile-done { background-color: rgba(61, 220, 151, 0.20); color: #3ddc97; border-radius: 9px; font-size: 10px; font-weight: bold; padding: 1px 7px; }
flowboxchild { padding: 0; background: none; }
.extras-bar { margin-top: 6px; }
"""


LIGHT_CSS = b"""
window.orka { background-color: #f3f5fc; }
.welcome { color: #3a4170; }
button.card { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.12); }
button.card:hover { background-color: #eef0ff; border-color: #8a93ff; box-shadow: 0 6px 18px rgba(60, 70, 200, 0.18); }
button.card:active { background-color: #e2e5ff; }
.card-title { color: #161a36; }
.card-desc { color: rgba(22, 26, 54, 0.60); }

button.primary:disabled { background-color: rgba(20, 30, 90, 0.10); }
button.primary:disabled label { color: rgba(22, 26, 54, 0.40); }
button.ghost { background-color: rgba(30, 40, 120, 0.06); border-color: rgba(30, 40, 120, 0.14); color: #161a36; }
button.ghost label, button.ghost image { color: #161a36; }
button.ghost:hover { background-color: rgba(30, 40, 120, 0.12); }

.footer { background-color: #e8ebf8; border-top-color: rgba(20, 30, 90, 0.10); }
.footer label { color: rgba(22, 26, 54, 0.80); }
switch { background-color: rgba(20, 30, 90, 0.18); }
switch:checked { background-color: #3b4bff; }

.doc-title { color: #161a36; }
scrolledwindow.doc { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.12); }
.doc-text { color: #252a4a; }

.picker-intro, .picker-count { color: #3a4170; }
.picker-cat { color: #3b46d6; }
.picker-name { color: #161a36; }
.picker-desc { color: rgba(22, 26, 54, 0.60); }
button.app-tile { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.12); }
button.app-tile:hover { background-color: #eef0ff; border-color: rgba(108, 120, 255, 0.60); }
button.app-tile:checked { background-color: rgba(79, 88, 240, 0.12); border-color: #6c78ff; box-shadow: 0 0 0 1px #6c78ff; }
button.app-tile:disabled { background-color: rgba(255, 255, 255, 0.60); border-color: rgba(30, 40, 120, 0.06); }
button.app-tile:disabled .picker-name { color: rgba(22, 26, 54, 0.50); }
.tile-done { background-color: rgba(19, 138, 90, 0.12); color: #138a5a; }
"""


def first_icon(names):
    theme = Gtk.IconTheme.get_default()
    for name in names:
        if theme.has_icon(name):
            return name
    return names[-1]


def system_lang():
    if IS_LIVE:
        try:
            with open(LANG_FILE) as f:
                code = f.read().strip()
            if code in TRANSLATIONS:
                return code
        except OSError:
            pass
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var, "")
        if value and value not in ("C", "POSIX"):
            code = value.split(":")[0][:2]
            return code if code in TRANSLATIONS else "en"
    return "en"


def has_nvidia_gpu():
    for dev in glob.glob("/sys/bus/pci/devices/*"):
        try:
            with open(dev + "/vendor") as f:
                vendor = f.read().strip()
            with open(dev + "/class") as f:
                pci_class = f.read().strip()
        except OSError:
            continue
        if vendor == "0x10de" and pci_class.startswith("0x03"):
            return True
    return False


def package_installed(name):
    try:
        out = subprocess.run(["dpkg-query", "-W", "-f=${Status}", name],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return out.strip().endswith("installed") and "not-installed" not in out


def installed_flatpaks():
    try:
        out = subprocess.run(["flatpak", "list", "--app", "--columns=application"],
                             capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return set()
    return set(out.split())


def is_dark_mode():
    for path in (os.path.expanduser("~/.config/kdeglobals"), "/etc/xdg/kdeglobals"):
        try:
            with open(path, encoding="utf-8") as f:
                group = None
                for line in f:
                    line = line.strip()
                    if line.startswith("["):
                        group = line
                    elif group == "[Colors:Window]" and line.startswith("BackgroundNormal="):
                        r, g, b = (int(v) for v in line.split("=", 1)[1].split(",")[:3])
                        return 0.2126 * r + 0.7152 * g + 0.0722 * b < 128
        except (OSError, ValueError):
            continue
    return True


def set_gtk_dark(dark):
    for version in ("gtk-3.0", "gtk-4.0"):
        path = os.path.expanduser(f"~/.config/{version}/settings.ini")
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        try:
            config.read(path, encoding="utf-8")
        except configparser.Error:
            continue
        if not config.has_section("Settings"):
            config.add_section("Settings")
        config["Settings"]["gtk-theme-name"] = "Breeze-Dark" if dark else "Breeze"
        config["Settings"]["gtk-application-prefer-dark-theme"] = "true" if dark else "false"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            config.write(f, space_around_delimiters=False)


def build_cards():
    cards = [
        ("readme", ["help-about", "dialog-information"], "dialog:readme_text"),
        ("release", ["text-x-changelog", "text-x-generic"], "dialog:release_text"),
        ("site", ["internet-web-browser", "applications-internet"], SITE_URL),
        ("discord", ["discord", "applications-internet"], DISCORD_URL),
        ("youtube", ["orka-youtube", "youtube", "applications-multimedia", "video-x-generic"], YOUTUBE_URL),
        ("apps", ["plasmadiscover", "system-software-install", "applications-other"], "plasma-discover"),
        ("look", ["orka-wyglad", "preferences-desktop-theme"], ORKA_APPS.format("orka-wyglad")),
        ("center", ["orka-centrum", "preferences-system"], ORKA_APPS.format("orka-centrum")),
    ]
    if not IS_LIVE:
        cards.append(("backup", ["orka-kopia", "document-revert"], ORKA_APPS.format("orka-kopia")))
        cards.append(("extras", ["applications-games", "package-x-generic", "applications-other"], "extras:"))
        if has_nvidia_gpu() and not package_installed("nvidia-driver"):
            cards.append(("nvidia", ["nvidia", "video-display", "preferences-desktop-display"],
                          ORKA_APPS.format("orka-centrum") + " drivers"))
    return cards


class Waves(Gtk.DrawingArea):

    def __init__(self):
        super().__init__()
        self.t = 0.0
        self.add_tick_callback(self.on_tick)
        self.connect("draw", self.on_draw)

    def on_tick(self, widget, clock):
        self.t = clock.get_frame_time() / 1_000_000
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def on_draw(self, widget, cr):
        import cairo
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        bg = cairo.LinearGradient(0, 0, 0, h)
        bg.add_color_stop_rgb(0, 0.016, 0.020, 0.118)
        bg.add_color_stop_rgb(0.6, 0.043, 0.059, 0.227)
        bg.add_color_stop_rgb(1, 0.059, 0.071, 0.420)
        cr.set_source(bg)
        cr.paint()
        for i, (amp, length, speed, level, color, alpha) in enumerate(WAVES):
            points = []
            x = 0.0
            while x <= w + 8:
                points.append((x, h * level + amp * math.sin(x / length + self.t * speed + i * 1.7)))
                x += 6
            cr.move_to(0, h)
            for px, py in points:
                cr.line_to(px, py)
            cr.line_to(w, h)
            cr.close_path()
            cr.set_source_rgba(*color, alpha)
            cr.fill()
            cr.move_to(*points[0])
            for px, py in points[1:]:
                cr.line_to(px, py)
            cr.set_source_rgba(0.80, 0.82, 1.0, 0.22 + 0.10 * i)
            cr.set_line_width(1.2)
            cr.stroke()
        return False


class OrkaLinuxHello(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.lang = system_lang()
        self.tr = TRANSLATIONS[self.lang]
        self.cards = build_cards()
        self.set_title(self.tr["title"])
        self.set_icon_name("orka-hello")
        self.set_default_size(1120 if len(self.cards) > 6 else 860, -1)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.get_style_context().add_class("orka")

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.light = None
        self.set_light(not is_dark_mode())

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.root)
        self.build_ui()

    def set_light(self, on):
        screen = Gdk.Screen.get_default()
        if on and self.light is None:
            self.light = Gtk.CssProvider()
            self.light.load_from_data(LIGHT_CSS)
            Gtk.StyleContext.add_provider_for_screen(screen, self.light, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)
        elif not on and self.light is not None:
            Gtk.StyleContext.remove_provider_for_screen(screen, self.light)
            self.light = None


    def build_ui(self):
        for child in self.root.get_children():
            self.root.remove(child)
        self.reveals = []

        self.root.pack_start(self.build_hero(), False, False, 0)

        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        body.set_margin_top(22)
        body.set_margin_bottom(22)
        body.set_margin_start(28)
        body.set_margin_end(28)
        self.pages = Gtk.Stack()
        self.pages.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.pages.set_transition_duration(250)
        self.pages.set_homogeneous(True)
        self.pages.add_named(body, "home")
        self.pages.add_named(self.build_text_page(), "text")
        self.root.pack_start(self.pages, True, True, 0)

        welcome = Gtk.Label(label=self.tr["welcome_text_live" if IS_LIVE else "welcome_text_installed"])
        welcome.set_line_wrap(True)
        welcome.set_max_width_chars(90)
        welcome.set_xalign(0)
        welcome.get_style_context().add_class("welcome")
        body.pack_start(self.animated(welcome), False, False, 0)

        columns = 4 if len(self.cards) > 6 else 3
        grid = Gtk.Grid(column_spacing=12, row_spacing=12, column_homogeneous=True)
        for i, (key, icons, action) in enumerate(self.cards):
            grid.attach(self.animated(self.build_card(key, icons, action)), i % columns, i // columns, 1, 1)
        body.pack_start(grid, False, False, 0)

        if IS_LIVE:
            install = Gtk.Button()
            install.get_style_context().add_class("install")
            box = Gtk.Box(spacing=12)
            try:
                pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(LOGO_WHITE, 26, 26, True)
                box.pack_start(Gtk.Image.new_from_pixbuf(pix), False, False, 0)
            except GLib.Error:
                pass
            box.pack_start(Gtk.Label(label=self.tr["btn_install"]), False, False, 0)
            install.add(box)
            install.set_halign(Gtk.Align.CENTER)
            install.connect("clicked", self.on_action, "orka-install")
            body.pack_start(self.animated(install), False, False, 4)

        self.root.pack_end(self.build_footer(), False, False, 0)
        self.show_all()
        self.start_animation()

    def build_hero(self):
        overlay = Gtk.Overlay()
        waves = Waves()
        waves.set_size_request(-1, 170)
        overlay.add(waves)

        row = Gtk.Box(spacing=20)
        row.set_margin_start(32)
        row.set_margin_end(24)
        row.set_margin_top(20)
        row.set_margin_bottom(28)
        try:
            pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(LOGO_WHITE, 96, 96, True)
            row.pack_start(Gtk.Image.new_from_pixbuf(pix), False, False, 0)
        except GLib.Error:
            row.pack_start(Gtk.Image.new_from_icon_name("orkalinux", Gtk.IconSize.DIALOG), False, False, 0)

        texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        texts.set_valign(Gtk.Align.CENTER)
        title = Gtk.Label(label=self.tr["title"], xalign=0)
        title.get_style_context().add_class("hero-title")
        sub = Gtk.Label(label="OrkaLinux " + self.tr["subtitle"], xalign=0)
        sub.get_style_context().add_class("hero-sub")
        texts.pack_start(title, False, False, 0)
        texts.pack_start(sub, False, False, 0)
        row.pack_start(texts, True, True, 0)

        if IS_LIVE:
            lang = Gtk.ComboBoxText()
            for code, name in LANG_NAMES.items():
                lang.append(code, name)
            lang.set_active_id(self.lang)
            lang.set_valign(Gtk.Align.START)
            lang.connect("changed", self.on_lang_changed)
            row.pack_end(lang, False, False, 0)

        overlay.add_overlay(self.animated(row))
        return overlay

    def build_card(self, key, icons, action):
        button = Gtk.Button()
        button.get_style_context().add_class("card")
        box = Gtk.Box(spacing=12)
        if key == "discord" and os.path.exists("/usr/share/pixmaps/discord.png"):
            pix = GdkPixbuf.Pixbuf.new_from_file_at_scale("/usr/share/pixmaps/discord.png", 32, 32, True)
            icon = Gtk.Image.new_from_pixbuf(pix)
        else:
            icon = Gtk.Image.new_from_icon_name(first_icon(icons), Gtk.IconSize.DND)
            icon.set_pixel_size(32)
        box.pack_start(icon, False, False, 0)

        texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        title = Gtk.Label(label=self.tr["btn_" + key], xalign=0)
        title.get_style_context().add_class("card-title")
        desc = Gtk.Label(label=self.tr["desc_" + key], xalign=0)
        desc.get_style_context().add_class("card-desc")
        texts.pack_start(title, False, False, 0)
        texts.pack_start(desc, False, False, 0)
        box.pack_start(texts, True, True, 0)

        button.add(box)
        button.connect("clicked", self.on_action, action)
        return button

    def build_footer(self):
        footer = Gtk.Box(spacing=10)
        footer.get_style_context().add_class("footer")
        inner = Gtk.Box(spacing=10)
        inner.set_margin_start(28)
        inner.set_margin_end(20)
        inner.set_margin_top(10)
        inner.set_margin_bottom(10)

        switch = Gtk.Switch()
        switch.set_active(os.path.exists(AUTOSTART_FILE))
        switch.set_valign(Gtk.Align.CENTER)
        switch.connect("notify::active", self.on_autostart_toggled)
        inner.pack_start(switch, False, False, 0)
        inner.pack_start(Gtk.Label(label=self.tr["autostart"]), False, False, 0)

        dark = Gtk.Switch()
        dark.set_active(is_dark_mode())
        dark.set_valign(Gtk.Align.CENTER)
        dark.set_margin_start(24)
        dark.connect("notify::active", self.on_dark_toggled)
        inner.pack_start(dark, False, False, 0)
        inner.pack_start(Gtk.Label(label=self.tr["dark_mode"]), False, False, 0)

        close = Gtk.Button(label=self.tr["close"])
        close.get_style_context().add_class("ghost")
        close.connect("clicked", lambda *_: Gtk.main_quit())
        inner.pack_end(close, False, False, 0)

        footer.pack_start(inner, True, True, 0)
        return footer


    def animated(self, widget):
        revealer = Gtk.Revealer()
        revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        revealer.set_transition_duration(450)
        revealer.add(widget)
        self.reveals.append(revealer)
        return revealer

    def start_animation(self):
        for i, revealer in enumerate(self.reveals):
            GLib.timeout_add(80 + i * 70, self.reveal, revealer)

    @staticmethod
    def reveal(revealer):
        revealer.set_reveal_child(True)
        return GLib.SOURCE_REMOVE


    def on_action(self, widget, action):
        if action.startswith("dialog:"):
            self.show_text_dialog(action.split(":", 1)[1])
        elif action == "extras:":
            self.show_extras()
        elif action.startswith("http"):
            subprocess.Popen(["xdg-open", action])
        elif action == "orka-install":
            env = dict(os.environ)
            loc = LOCALES.get(self.lang, "en_US.UTF-8")
            env.update(LANG=loc, LC_MESSAGES=loc, LANGUAGE=self.lang)
            subprocess.Popen(["orka-install"], env=env)
            GLib.timeout_add(400, lambda: self.close() or False)
        else:
            subprocess.Popen(shlex.split(action))
            if action == "orka-install":
                GLib.timeout_add(400, lambda: self.close() or False)

    def build_text_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        page.set_margin_top(18)
        page.set_margin_bottom(18)
        page.set_margin_start(28)
        page.set_margin_end(28)
        top = Gtk.Box(spacing=12)
        back = Gtk.Button()
        back.get_style_context().add_class("ghost")
        back.add(Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON))
        back.connect("clicked", lambda *_: self.pages.set_visible_child_name("home"))
        top.pack_start(back, False, False, 0)
        self.text_icon = Gtk.Image()
        top.pack_start(self.text_icon, False, False, 0)
        self.text_title = Gtk.Label(xalign=0)
        self.text_title.get_style_context().add_class("doc-title")
        top.pack_start(self.text_title, True, True, 0)
        page.pack_start(top, False, False, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(300)
        scrolled.get_style_context().add_class("doc")
        self.text_body = Gtk.Label(xalign=0, yalign=0, selectable=True)
        self.text_body.set_line_wrap(True)
        self.text_body.set_max_width_chars(110)
        self.text_body.get_style_context().add_class("doc-text")
        self.text_body.set_margin_top(18)
        self.text_body.set_margin_bottom(18)
        self.text_body.set_margin_start(22)
        self.text_body.set_margin_end(22)
        scrolled.add(self.text_body)
        page.pack_start(scrolled, True, True, 0)
        return page

    def show_text_dialog(self, text_key):
        readme = text_key == "readme_text"
        self.text_title.set_text(self.tr["btn_readme" if readme else "btn_release"])
        icons = ["help-about", "dialog-information"] if readme else ["text-x-changelog", "text-x-generic"]
        self.text_icon.set_from_icon_name(first_icon(icons), Gtk.IconSize.DND)
        self.text_icon.set_pixel_size(28)
        self.text_body.set_text(self.tr[text_key])
        self.pages.show_all()
        self.pages.set_visible_child_name("text")

    def extras_icon(self, app_id, name):
        path = os.path.join(EXTRAS_ICONS, app_id + ".png")
        if os.path.exists(path):
            try:
                pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 56, 56, True)
                return Gtk.Image.new_from_pixbuf(pix)
            except GLib.Error:
                pass
        area = Gtk.DrawingArea()
        area.set_size_request(56, 56)
        hue = sum(map(ord, app_id)) % 360 / 360.0

        def draw(widget, cr):
            import cairo
            import colorsys
            r, g, b = colorsys.hsv_to_rgb(hue, 0.55, 0.95)
            grad = cairo.LinearGradient(0, 0, 56, 56)
            grad.add_color_stop_rgb(0, r, g, b)
            grad.add_color_stop_rgb(1, r * 0.45, g * 0.45, b * 0.75)
            radius = 14
            cr.new_sub_path()
            cr.arc(56 - radius, radius, radius, -math.pi / 2, 0)
            cr.arc(56 - radius, 56 - radius, radius, 0, math.pi / 2)
            cr.arc(radius, 56 - radius, radius, math.pi / 2, math.pi)
            cr.arc(radius, radius, radius, math.pi, 3 * math.pi / 2)
            cr.close_path()
            cr.set_source(grad)
            cr.fill()
            cr.set_source_rgb(1, 1, 1)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(28)
            ext = cr.text_extents(name[0])
            cr.move_to(28 - ext.width / 2 - ext.x_bearing, 28 - ext.height / 2 - ext.y_bearing)
            cr.show_text(name[0])
            return False
        area.connect("draw", draw)
        return area

    def extras_tile(self, app, installed):
        tile = Gtk.ToggleButton()
        tile.get_style_context().add_class("app-tile")
        tile.set_size_request(150, 150)
        overlay = Gtk.Overlay()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        icon = self.extras_icon(app["id"], app["name"])
        icon.set_halign(Gtk.Align.CENTER)
        box.pack_start(icon, False, False, 2)
        name = Gtk.Label(label=app["name"])
        name.get_style_context().add_class("picker-name")
        name.set_ellipsize(3)
        name.set_max_width_chars(16)
        box.pack_start(name, False, False, 0)
        desc = Gtk.Label(label=app.get(self.lang, app["en"]))
        desc.get_style_context().add_class("picker-desc")
        desc.set_line_wrap(True)
        desc.set_justify(Gtk.Justification.CENTER)
        desc.set_max_width_chars(18)
        box.pack_start(desc, False, False, 0)
        overlay.add(box)

        mark = Gtk.Label(label=self.tr["installed"] if installed else "\u2713")
        mark.get_style_context().add_class("tile-done" if installed else "tile-mark")
        mark.set_halign(Gtk.Align.END)
        mark.set_valign(Gtk.Align.START)
        mark.set_no_show_all(True)
        overlay.add_overlay(mark)
        tile.add(overlay)

        if installed:
            tile.set_sensitive(False)
            mark.show()
        else:
            tile.connect("toggled", lambda t: mark.set_visible(t.get_active()))
        return tile

    def show_extras(self):
        """Kafelki z programami z Flathuba do zaznaczenia; instalacja w terminalu.
        Strona wjeżdża w oknie Hello (jak Readme), strzałka wraca."""
        installed = installed_flatpaks()
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page.set_margin_top(18)
        page.set_margin_bottom(16)
        page.set_margin_start(28)
        page.set_margin_end(28)

        top = Gtk.Box(spacing=12)
        back = Gtk.Button()
        back.get_style_context().add_class("ghost")
        back.add(Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON))
        back.connect("clicked", lambda *_: self.close_extras())
        top.pack_start(back, False, False, 0)
        icon = Gtk.Image.new_from_icon_name(first_icon(["applications-games", "package-x-generic"]), Gtk.IconSize.DND)
        icon.set_pixel_size(28)
        top.pack_start(icon, False, False, 0)
        title = Gtk.Label(label=self.tr["extras_title"], xalign=0)
        title.get_style_context().add_class("doc-title")
        top.pack_start(title, True, True, 0)
        page.pack_start(top, False, False, 0)

        intro = Gtk.Label(label=self.tr["extras_intro"], xalign=0)
        intro.set_line_wrap(True)
        intro.set_max_width_chars(110)
        intro.get_style_context().add_class("picker-intro")
        page.pack_start(intro, False, False, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_min_content_height(300)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_end(8)
        tiles = []
        apps_by_id = {}
        for group in load_extras():
            head = Gtk.Label(label=self.tr.get("cat_" + group["category"], group["category"]), xalign=0)
            head.get_style_context().add_class("picker-cat")
            head.set_margin_top(10)
            box.pack_start(head, False, False, 0)
            flow = Gtk.FlowBox()
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_homogeneous(True)
            flow.set_min_children_per_line(4)
            flow.set_max_children_per_line(7)
            flow.set_column_spacing(10)
            flow.set_row_spacing(10)
            for app in group["apps"]:
                apps_by_id[app["id"]] = app
                if "script" in app:
                    done = os.path.exists(os.path.expanduser(app.get("check", "")))
                else:
                    done = app["id"] in installed
                tile = self.extras_tile(app, done)
                flow.add(tile)
                tiles.append((tile, app["id"]))
            box.pack_start(flow, False, False, 0)
        scrolled.add(box)
        page.pack_start(scrolled, True, True, 0)

        bar = Gtk.Box(spacing=10)
        bar.get_style_context().add_class("extras-bar")
        count = Gtk.Label(label=self.tr["extras_count"].format(n=0))
        count.get_style_context().add_class("picker-count")
        bar.pack_start(count, False, False, 0)
        install = Gtk.Button(label=self.tr["extras_install"])
        install.get_style_context().add_class("primary")
        install.set_sensitive(False)
        bar.pack_end(install, False, False, 0)
        cancel = Gtk.Button(label=self.tr["cancel"])
        cancel.get_style_context().add_class("ghost")
        cancel.connect("clicked", lambda *_: self.close_extras())
        bar.pack_end(cancel, False, False, 0)
        page.pack_start(bar, False, False, 0)

        def selected():
            return [app_id for tile, app_id in tiles if tile.get_active() and tile.get_sensitive()]

        def update(*_):
            chosen = selected()
            count.set_text(self.tr["extras_count"].format(n=len(chosen)))
            install.set_sensitive(bool(chosen))

        def do_install(*_):
            chosen = selected()
            self.close_extras()
            if not chosen:
                return
            free = shutil.disk_usage("/var").free
            if free < 3 * 1024 ** 3:
                dialog = Gtk.MessageDialog(transient_for=self, modal=True,
                                           message_type=Gtk.MessageType.WARNING,
                                           buttons=Gtk.ButtonsType.NONE,
                                           text=self.tr["low_space"].format(free="%.1f GB" % (free / 1024 ** 3)))
                dialog.add_button(self.tr["cancel"], Gtk.ResponseType.CANCEL)
                dialog.add_button(self.tr["try_anyway"], Gtk.ResponseType.OK)
                answer = dialog.run()
                dialog.destroy()
                if answer != Gtk.ResponseType.OK:
                    return
            steps = []
            flat = [a for a in chosen if "script" not in apps_by_id[a]]
            if flat:
                steps.append(shlex.join(["flatpak", "install", "-y", "--system", "flathub"] + flat))
            for a in chosen:
                app = apps_by_id[a]
                if "script" in app:
                    cmd = ["sh", os.path.join(EXTRAS_SCRIPTS, app["script"])]
                    steps.append(shlex.join((["sudo"] if app.get("root") else []) + cmd))
            self.run_in_terminal(["sh", "-c", " && ".join(steps)])

        for tile, _ in tiles:
            tile.connect("toggled", update)
        install.connect("clicked", do_install)

        old_page = self.pages.get_child_by_name("extras")
        if old_page is not None:
            self.pages.remove(old_page)
        self.pages.add_named(page, "extras")
        page.show_all()
        self.pages.set_visible_child_name("extras")

    def close_extras(self):
        self.pages.set_visible_child_name("home")

    def run_in_terminal(self, args):
        command = shlex.join(args)
        done = shlex.quote(self.tr["term_done"])
        failed = shlex.quote(self.tr["term_failed"])
        script = f"if {command}; then echo; echo {done}; sleep 3; else echo; echo {failed}; read -r _; fi"
        try:
            subprocess.Popen(["kitty", "sh", "-c", script])
        except OSError:
            dialog = Gtk.MessageDialog(transient_for=self, modal=True,
                                       message_type=Gtk.MessageType.ERROR,
                                       buttons=Gtk.ButtonsType.OK,
                                       text=self.tr["no_terminal"])
            dialog.run()
            dialog.destroy()

    def on_lang_changed(self, combo):
        lang = combo.get_active_id()
        if lang and lang != self.lang:
            self.lang = lang
            self.tr = TRANSLATIONS[lang]
            try:
                os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
                with open(LANG_FILE, "w") as f:
                    f.write(lang + "\n")
            except OSError:
                pass
            self.set_title(self.tr["title"])
            GLib.idle_add(self.build_ui)

    def on_dark_toggled(self, switch, _param):
        dark = switch.get_active()
        if dark == is_dark_mode():
            return
        try:
            subprocess.Popen(["plasma-apply-lookandfeel", "-a", LOOK_DARK if dark else LOOK_LIGHT])
        except OSError:
            return
        set_gtk_dark(dark)
        self.set_light(not dark)

    def on_autostart_toggled(self, switch, _param):
        if switch.get_active():
            os.makedirs(os.path.dirname(AUTOSTART_FILE), exist_ok=True)
            with open(AUTOSTART_FILE, "w") as f:
                f.write("[Desktop Entry]\nType=Application\nName=OrkaLinux Hello\n"
                        "Exec=/usr/share/orkalinux-hello/orkalinux-hello.py\nIcon=orka-hello\n"
                        "X-KDE-autostart-after=panel\n")
        elif os.path.exists(AUTOSTART_FILE):
            os.remove(AUTOSTART_FILE)


if __name__ == "__main__":
    win = OrkaLinuxHello()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
