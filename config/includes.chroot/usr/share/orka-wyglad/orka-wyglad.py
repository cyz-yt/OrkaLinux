#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import sys

sys.path.insert(0, "/usr/share/orkalinux/lib")
import orka
from orka import Gtk, GLib, GdkPixbuf

TEXTS = {
    "en": {
        "title": "OrkaLinux Appearance", "subtitle": "Make the desktop yours in a few clicks",
        "p_layout": "Layout", "p_layout_sub": "Pick how the panel looks. Your apps and files stay as they are.",
        "p_colors": "Colours", "p_colors_sub": "Dark or light mode and the accent colour of buttons and highlights.",
        "p_wall": "Wallpaper", "p_wall_sub": "Click a picture to set it. Undertow switches between light and dark by itself.",
        "p_fx": "Effects", "p_fx_sub": "Window animations and how fast things move.",
        "p_login": "Login", "p_login_sub": "How the screen where you type your password looks. Changing it asks for your password.",
        "p_boot": "Boot", "p_boot_sub": "What you see while the computer starts. Changing it takes a minute in the terminal.",
        "lg_breeze": "Plasma", "lg_breeze_d": "The standard KDE screen with the OrkaLinux wallpaper",
        "lg_glass": "Glass", "lg_glass_d": "Big clock on top, frosted password field in the middle",
        "lg_side": "Side panel", "lg_side_d": "Clock and login on a dark panel, wallpaper on the right",
        "bt_bar": "Bar", "bt_bar_d": "Logo and a thin loading bar (default)",
        "bt_dots": "Dots", "bt_dots_d": "Logo and spinning dots near the bottom",
        "bt_text": "Text", "bt_text_d": "No boot screen - startup messages like in Arch",
        "dot_size": "Dot size", "dot_apply": "Apply", "dot_size_d": "Pick a size to see it on the Dots preview, then click Apply. This also switches the boot screen to dots.", "ds_micro": "Micro", "ds_small": "Small", "ds_medium": "Medium", "ds_large": "Large", "ds_giga": "Giga",
        "in_use": "In use",
        "login_note": "You will see it after logging out or restarting. The lock screen (Meta+L) is a separate Plasma screen.",
        "by": "by {a}",
        "l_orka": "OrkaLinux", "l_orka_d": "Floating bar at the bottom",
        "l_win": "Windows", "l_win_d": "Centered icons, full-width bar",
        "l_mac": "macOS", "l_mac_d": "Top bar with menus and a dock",
        "l_classic": "Classic", "l_classic_d": "Menu on the left, window names",
        "layout_q": "Change the panel layout?", "layout_q2": "Your current panels (and widgets on them) will be replaced. Desktop icons and files stay.",
        "change": "Change",
        "dark": "Dark", "light": "Light", "mode": "Mode",
        "accent": "Accent colour", "accent_auto": "From wallpaper",
        "lock_too": "Also use it on the lock screen", "own_wall": "Choose your own picture...",
        "pick_image": "Choose a wallpaper", "images": "Images",
        "fx_wobbly": "Wobbly windows", "fx_wobbly_d": "Windows wobble like jelly while you drag them",
        "fx_lamp": "Magic lamp", "fx_lamp_d": "Minimised windows get sucked into the panel",
        "fx_blur": "Blur behind transparent windows", "fx_blur_d": "Panel, menus and kitty get a frosted look",
        "fx_move": "See-through windows while moving", "fx_move_d": "A dragged window turns slightly transparent",
        "speed": "Animation speed", "s_off": "Off", "s_fast": "Fast", "s_normal": "Normal", "s_slow": "Slow",
        "failed": "It didn't work.", "failed_plasma": "Plasma did not answer. Is the desktop running?",
    },
    "pl": {
        "title": "Wygląd systemu OrkaLinux", "subtitle": "Pulpit po Twojemu w kilka kliknięć",
        "p_layout": "Układ", "p_layout_sub": "Wybierz, jak ma wyglądać panel. Programy i pliki zostają bez zmian.",
        "p_colors": "Kolory", "p_colors_sub": "Tryb ciemny albo jasny i kolor akcentu przycisków i zaznaczeń.",
        "p_wall": "Tapeta", "p_wall_sub": "Kliknij obrazek, żeby go ustawić. Undertow sam zmienia się na jasny i ciemny.",
        "p_fx": "Efekty", "p_fx_sub": "Animacje okien i to, jak szybko wszystko się rusza.",
        "p_login": "Logowanie", "p_login_sub": "Jak wygląda ekran, na którym wpisujesz hasło. Zmiana zapyta o hasło.",
        "p_boot": "Uruchamianie", "p_boot_sub": "To, co widać, gdy komputer się włącza. Zmiana trwa chwilę w terminalu.",
        "lg_breeze": "Plasma", "lg_breeze_d": "Standardowy ekran KDE z tapetą OrkaLinux",
        "lg_glass": "Szkło", "lg_glass_d": "Duży zegar u góry, matowe pole hasła na środku",
        "lg_side": "Panel z boku", "lg_side_d": "Zegar i logowanie na ciemnym panelu, tapeta po prawej",
        "bt_bar": "Pasek", "bt_bar_d": "Logo i cienki pasek ładowania (domyślny)",
        "bt_dots": "Kropki", "bt_dots_d": "Logo i kręcące się kropki na dole",
        "bt_text": "Tekst", "bt_text_d": "Bez ekranu startowego - komunikaty startu jak w Archu",
        "dot_size": "Rozmiar kropek", "dot_apply": "Zastosuj", "dot_size_d": "Wybierz rozmiar, zobacz go na podglądzie Kropek i kliknij Zastosuj. To włącza też ekran startowy z kropkami.", "ds_micro": "Mikro", "ds_small": "Małe", "ds_medium": "Średnie", "ds_large": "Duże", "ds_giga": "Giga",
        "in_use": "Używany",
        "login_note": "Zobaczysz go po wylogowaniu albo restarcie. Blokada ekranu (Meta+L) to osobny ekran Plasmy.",
        "by": "autor: {a}",
        "l_orka": "OrkaLinux", "l_orka_d": "Pływający pasek na dole",
        "l_win": "Windows", "l_win_d": "Ikony na środku, pasek na całą szerokość",
        "l_mac": "macOS", "l_mac_d": "Pasek u góry z menu i dok",
        "l_classic": "Klasyczny", "l_classic_d": "Menu po lewej, nazwy okien",
        "layout_q": "Zmienić układ panelu?", "layout_q2": "Obecne panele (i widżety na nich) zostaną podmienione. Ikony na pulpicie i pliki zostają.",
        "change": "Zmień",
        "dark": "Ciemny", "light": "Jasny", "mode": "Tryb",
        "accent": "Kolor akcentu", "accent_auto": "Z tapety",
        "lock_too": "Ustaw też na ekranie blokady", "own_wall": "Wybierz własny obrazek...",
        "pick_image": "Wybierz tapetę", "images": "Obrazki",
        "fx_wobbly": "Galaretkowe okna", "fx_wobbly_d": "Okna falują jak galaretka, kiedy je przeciągasz",
        "fx_lamp": "Magiczna lampa", "fx_lamp_d": "Zminimalizowane okna wsysają się w panel",
        "fx_blur": "Rozmycie za przezroczystymi oknami", "fx_blur_d": "Panel, menu i kitty wyglądają jak matowe szkło",
        "fx_move": "Przezroczyste okna przy przesuwaniu", "fx_move_d": "Przeciągane okno robi się lekko przezroczyste",
        "speed": "Szybkość animacji", "s_off": "Wyłączone", "s_fast": "Szybko", "s_normal": "Normalnie", "s_slow": "Wolno",
        "failed": "Nie udało się.", "failed_plasma": "Plasma nie odpowiada. Czy pulpit działa?",
    },
    "de": {
        "title": "OrkaLinux Appearance", "subtitle": "Dein Desktop mit ein paar Klicks",
        "p_layout": "Layout", "p_layout_sub": "Wähle, wie die Leiste aussieht. Programme und Dateien bleiben, wie sie sind.",
        "p_colors": "Farben", "p_colors_sub": "Dunkler oder heller Modus und die Akzentfarbe.",
        "p_wall": "Hintergrund", "p_wall_sub": "Klicke auf ein Bild, um es zu setzen. Undertow wechselt selbst zwischen hell und dunkel.",
        "p_fx": "Effekte", "p_fx_sub": "Fensteranimationen und wie schnell sich alles bewegt.",
        "p_login": "Anmeldung", "p_login_sub": "Wie der Bildschirm aussieht, auf dem du dein Passwort eingibst. Zum Ändern brauchst du dein Passwort.",
        "p_boot": "Start", "p_boot_sub": "Was du beim Hochfahren siehst. Das Ändern dauert im Terminal eine Minute.",
        "lg_breeze": "Plasma", "lg_breeze_d": "Der Standard von KDE mit OrkaLinux-Hintergrund",
        "lg_glass": "Glas", "lg_glass_d": "Große Uhr oben, mattes Passwortfeld in der Mitte",
        "lg_side": "Seitenleiste", "lg_side_d": "Uhr und Anmeldung auf einer dunklen Leiste, Hintergrund rechts",
        "bt_bar": "Balken", "bt_bar_d": "Logo und ein dünner Ladebalken (Standard)",
        "bt_dots": "Punkte", "bt_dots_d": "Logo und kreisende Punkte unten",
        "bt_text": "Text", "bt_text_d": "Kein Startbildschirm - Startmeldungen wie bei Arch",
        "dot_size": "Punktgröße", "dot_apply": "Anwenden", "dot_size_d": "Wähle eine Größe, sieh sie dir in der Vorschau an und klicke auf Anwenden. Das aktiviert auch den Startbildschirm mit Punkten.", "ds_micro": "Mikro", "ds_small": "Klein", "ds_medium": "Mittel", "ds_large": "Groß", "ds_giga": "Giga",
        "in_use": "Aktiv",
        "login_note": "Du siehst ihn nach dem Abmelden oder Neustart. Die Bildschirmsperre (Meta+L) ist ein eigener Plasma-Bildschirm.",
        "by": "von {a}",
        "l_orka": "OrkaLinux", "l_orka_d": "Schwebende Leiste unten",
        "l_win": "Windows", "l_win_d": "Symbole in der Mitte, volle Breite",
        "l_mac": "macOS", "l_mac_d": "Leiste oben mit Menüs und ein Dock",
        "l_classic": "Klassisch", "l_classic_d": "Menü links, Fensternamen",
        "layout_q": "Leisten-Layout ändern?", "layout_q2": "Die aktuellen Leisten (und Widgets darauf) werden ersetzt. Desktop-Symbole und Dateien bleiben.",
        "change": "Ändern",
        "dark": "Dunkel", "light": "Hell", "mode": "Modus",
        "accent": "Akzentfarbe", "accent_auto": "Aus dem Hintergrund",
        "lock_too": "Auch für den Sperrbildschirm", "own_wall": "Eigenes Bild wählen...",
        "pick_image": "Hintergrundbild wählen", "images": "Bilder",
        "fx_wobbly": "Wabbelnde Fenster", "fx_wobbly_d": "Fenster wackeln beim Ziehen wie Wackelpudding",
        "fx_lamp": "Wunderlampe", "fx_lamp_d": "Minimierte Fenster werden in die Leiste gesaugt",
        "fx_blur": "Unschärfe hinter transparenten Fenstern", "fx_blur_d": "Leiste, Menüs und kitty wie Milchglas",
        "fx_move": "Durchsichtige Fenster beim Verschieben", "fx_move_d": "Ein gezogenes Fenster wird leicht durchsichtig",
        "speed": "Animationstempo", "s_off": "Aus", "s_fast": "Schnell", "s_normal": "Normal", "s_slow": "Langsam",
        "failed": "Das hat nicht geklappt.", "failed_plasma": "Plasma antwortet nicht. Läuft der Desktop?",
    },
    "fr": {
        "title": "Apparence OrkaLinux", "subtitle": "Ton bureau à ton goût en quelques clics",
        "p_layout": "Disposition", "p_layout_sub": "Choisis l'allure du panneau. Tes applis et fichiers ne bougent pas.",
        "p_colors": "Couleurs", "p_colors_sub": "Mode sombre ou clair et couleur d'accent.",
        "p_wall": "Fond d'écran", "p_wall_sub": "Clique sur une image pour l'appliquer. Undertow passe tout seul du clair au sombre.",
        "p_fx": "Effets", "p_fx_sub": "Animations des fenêtres et vitesse.",
        "p_login": "Connexion", "p_login_sub": "L'écran où tu tapes ton mot de passe. Le changer demande ton mot de passe.",
        "p_boot": "Démarrage", "p_boot_sub": "Ce que tu vois quand l'ordinateur démarre. Le changement prend une minute dans le terminal.",
        "lg_breeze": "Plasma", "lg_breeze_d": "L'écran standard de KDE avec le fond OrkaLinux",
        "lg_glass": "Verre", "lg_glass_d": "Grande horloge en haut, champ de mot de passe givré au centre",
        "lg_side": "Panneau latéral", "lg_side_d": "Horloge et connexion sur un panneau sombre, fond à droite",
        "bt_bar": "Barre", "bt_bar_d": "Logo et une fine barre de chargement (par défaut)",
        "bt_dots": "Points", "bt_dots_d": "Logo et des points qui tournent en bas",
        "bt_text": "Texte", "bt_text_d": "Sans écran de démarrage - messages comme sous Arch",
        "dot_size": "Taille des points", "dot_apply": "Appliquer", "dot_size_d": "Choisis une taille, regarde-la dans l'aperçu puis clique sur Appliquer. Cela active aussi l'écran de démarrage à points.", "ds_micro": "Micro", "ds_small": "Petits", "ds_medium": "Moyens", "ds_large": "Grands", "ds_giga": "Géants",
        "in_use": "Utilisé",
        "login_note": "Tu le verras après déconnexion ou redémarrage. Le verrouillage (Meta+L) est un écran Plasma à part.",
        "by": "par {a}",
        "l_orka": "OrkaLinux", "l_orka_d": "Barre flottante en bas",
        "l_win": "Windows", "l_win_d": "Icônes au centre, barre pleine largeur",
        "l_mac": "macOS", "l_mac_d": "Barre en haut avec menus et un dock",
        "l_classic": "Classique", "l_classic_d": "Menu à gauche, noms des fenêtres",
        "layout_q": "Changer la disposition ?", "layout_q2": "Les panneaux actuels (et leurs widgets) seront remplacés. Les icônes du bureau et les fichiers restent.",
        "change": "Changer",
        "dark": "Sombre", "light": "Clair", "mode": "Mode",
        "accent": "Couleur d'accent", "accent_auto": "Depuis le fond d'écran",
        "lock_too": "Aussi sur l'écran de verrouillage", "own_wall": "Choisir ma propre image...",
        "pick_image": "Choisir un fond d'écran", "images": "Images",
        "fx_wobbly": "Fenêtres en gelée", "fx_wobbly_d": "Les fenêtres ondulent quand tu les déplaces",
        "fx_lamp": "Lampe magique", "fx_lamp_d": "Les fenêtres réduites sont aspirées dans le panneau",
        "fx_blur": "Flou derrière les fenêtres transparentes", "fx_blur_d": "Panneau, menus et kitty en verre dépoli",
        "fx_move": "Fenêtres transparentes pendant le déplacement", "fx_move_d": "Une fenêtre déplacée devient un peu transparente",
        "speed": "Vitesse des animations", "s_off": "Désactivées", "s_fast": "Rapide", "s_normal": "Normale", "s_slow": "Lente",
        "failed": "Ça n'a pas marché.", "failed_plasma": "Plasma ne répond pas. Le bureau tourne-t-il ?",
    },
}

LAUNCHERS = [
    "org.kde.dolphin.desktop",
    "firefox.desktop",
    "discord.desktop",
    "kitty.desktop",
    "com.spotify.Client.desktop",
]

JS_COMMON = """
var launchers = [];
var wanted = %s;
for (var w = 0; w < wanted.length; w++) {
    if (applicationExists(wanted[w])) { launchers.push("applications:" + wanted[w]); }
}
var old = panels();
for (var i = 0; i < old.length; i++) { old[i].remove(); }
function startMenu(panel, plugin) {
    var menu = panel.addWidget(plugin);
    menu.currentConfigGroup = ["General"];
    menu.writeConfig("icon", "orka-start");
    if (plugin == "org.kde.plasma.kickoff") {
        menu.writeConfig("primaryActions", 2);
        menu.writeConfig("systemFavorites", ["reboot", "shutdown"]);
    }
    return menu;
}
function tasks(panel, plugin, fill) {
    var t = panel.addWidget(plugin);
    t.currentConfigGroup = ["General"];
    t.writeConfig("launchers", launchers);
    if (fill === false) { t.writeConfig("fill", false); }
    return t;
}
""" % json.dumps(LAUNCHERS)

LAYOUTS = {
    "orka": """
var p = new Panel;
p.location = "bottom";
p.height = 2 * Math.floor(gridUnit * 2.5 / 2);
p.floating = true;
p.lengthMode = "fill";
startMenu(p, "org.kde.plasma.kickoff");
tasks(p, "org.kde.plasma.icontasks");
p.addWidget("org.kde.plasma.marginsseparator");
p.addWidget("org.kde.plasma.systemtray");
p.addWidget("org.kde.plasma.digitalclock");
p.addWidget("org.kde.plasma.showdesktop");
""",
    "windows": """
var p = new Panel;
p.location = "bottom";
p.height = 2 * Math.floor(gridUnit * 2.4 / 2);
p.floating = false;
p.lengthMode = "fill";
p.addWidget("org.kde.plasma.panelspacer");
startMenu(p, "org.kde.plasma.kickoff");
tasks(p, "org.kde.plasma.icontasks", false);
p.addWidget("org.kde.plasma.panelspacer");
p.addWidget("org.kde.plasma.systemtray");
p.addWidget("org.kde.plasma.digitalclock");
p.addWidget("org.kde.plasma.showdesktop");
""",
    "mac": """
var top = new Panel;
top.location = "top";
top.height = 2 * Math.floor(gridUnit * 1.7 / 2);
top.floating = false;
startMenu(top, "org.kde.plasma.kickoff");
top.addWidget("org.kde.plasma.appmenu");
top.addWidget("org.kde.plasma.panelspacer");
top.addWidget("org.kde.plasma.systemtray");
top.addWidget("org.kde.plasma.digitalclock");
var dock = new Panel;
dock.location = "bottom";
dock.height = 2 * Math.floor(gridUnit * 3.2 / 2);
dock.alignment = "center";
dock.lengthMode = "fit";
dock.floating = true;
dock.hiding = "dodgewindows";
tasks(dock, "org.kde.plasma.icontasks");
""",
    "classic": """
var p = new Panel;
p.location = "bottom";
p.height = 2 * Math.floor(gridUnit * 2.2 / 2);
p.floating = false;
p.lengthMode = "fill";
startMenu(p, "org.kde.plasma.kicker");
tasks(p, "org.kde.plasma.taskmanager");
p.addWidget("org.kde.plasma.systemtray");
p.addWidget("org.kde.plasma.digitalclock");
p.addWidget("org.kde.plasma.showdesktop");
""",
}

ACCENTS = ["#4f58f0", "#18b4e0", "#8a4dff", "#e0559a", "#ff5c7a", "#ff9a3d", "#ffc857", "#3ddc97"]

SPEEDS = [0.0, 0.5, 1.0, 2.0]


def draw_layout_preview(kind, cr, w, h, dark=True):
    import cairo
    r = 10
    cr.new_sub_path()
    cr.arc(w - r, r, r, -1.5708, 0)
    cr.arc(w - r, h - r, r, 0, 1.5708)
    cr.arc(r, h - r, r, 1.5708, 3.1416)
    cr.arc(r, r, r, 3.1416, 4.7124)
    cr.close_path()
    bg = cairo.LinearGradient(0, 0, w, h)
    bg.add_color_stop_rgb(0, 0.10, 0.42, 0.85)
    bg.add_color_stop_rgb(1, 0.40, 0.22, 0.90)
    cr.set_source(bg)
    cr.fill_preserve()
    cr.save()
    cr.clip()

    def bar(x, y, bw, bh, rad, alpha=0.85):
        cr.new_sub_path()
        cr.arc(x + bw - rad, y + rad, rad, -1.5708, 0)
        cr.arc(x + bw - rad, y + bh - rad, rad, 0, 1.5708)
        cr.arc(x + rad, y + bh - rad, rad, 1.5708, 3.1416)
        cr.arc(x + rad, y + rad, rad, 3.1416, 4.7124)
        cr.close_path()
        cr.set_source_rgba(0.06, 0.07, 0.14, alpha)
        cr.fill()

    def dots(x, y, n, size=6, gap=4, color=(1, 1, 1, 0.85)):
        for i in range(n):
            cr.set_source_rgba(*color)
            cr.rectangle(x + i * (size + gap), y, size, size)
            cr.fill()

    cr.set_source_rgba(1, 1, 1, 0.18)
    cr.rectangle(w * 0.18, h * 0.16, w * 0.5, h * 0.48)
    cr.fill()

    if kind == "orka":
        bar(w * 0.04, h - 22, w * 0.92, 16, 6)
        dots(w * 0.04 + 6, h - 17, 6)
        dots(w * 0.96 - 26, h - 17, 2, color=(1, 1, 1, 0.5))
    elif kind == "windows":
        bar(0, h - 16, w, 16, 0, 0.92)
        dots(w / 2 - 34, h - 11, 7)
        dots(w - 26, h - 11, 2, color=(1, 1, 1, 0.5))
    elif kind == "mac":
        bar(0, 0, w, 10, 0, 0.92)
        dots(6, 2, 3, size=5, gap=6, color=(1, 1, 1, 0.6))
        bar(w / 2 - 44, h - 22, 88, 16, 6)
        dots(w / 2 - 38, h - 17, 7)
    else:
        bar(0, h - 16, w, 16, 0, 0.92)
        cr.set_source_rgba(0.31, 0.35, 0.94, 1)
        cr.rectangle(4, h - 13, 12, 10)
        cr.fill()
        for i in range(3):
            cr.set_source_rgba(1, 1, 1, 0.25 if i else 0.45)
            cr.rectangle(22 + i * 34, h - 12, 30, 8)
            cr.fill()
        dots(w - 26, h - 11, 2, color=(1, 1, 1, 0.5))
    cr.restore()


HELPER = "/usr/sbin/orka-wyglad-helper"
SDDM_CONF = "/etc/sddm.conf.d/orkalinux.conf"
LOGIN_THEMES = [("breeze", "lg_breeze"), ("orkalinux-glass", "lg_glass"), ("orkalinux-side", "lg_side")]
BOOT_THEMES = [("orkalinux", "bt_bar"), ("orkalinux-dots", "bt_dots"), ("text", "bt_text")]
DOT_SIZES = [("micro", 5), ("small", 8), ("medium", 12), ("large", 18), ("giga", 28)]
DOTS_SCRIPT = "/usr/share/plymouth/themes/orkalinux-dots/orkalinux-dots.script"


def rounded(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -1.5708, 0)
    cr.arc(x + w - r, y + h - r, r, 0, 1.5708)
    cr.arc(x + r, y + h - r, r, 1.5708, 3.1416)
    cr.arc(x + r, y + r, r, 3.1416, 4.7124)
    cr.close_path()


def undertow_bg(cr, w, h):
    import cairo
    rounded(cr, 0, 0, w, h, 10)
    cr.clip()
    bg = cairo.LinearGradient(0, 0, 0, h)
    bg.add_color_stop_rgb(0, 0.016, 0.020, 0.118)
    bg.add_color_stop_rgb(0.55, 0.055, 0.070, 0.420)
    bg.add_color_stop_rgb(1, 0.21, 0.12, 0.79)
    cr.set_source(bg)
    cr.paint()


def draw_login_preview(kind, cr, w, h):
    undertow_bg(cr, w, h)
    white = (1, 1, 1)

    def block(x, y, bw, bh, alpha, r=3, color=white):
        rounded(cr, x, y, bw, bh, min(r, bh / 2))
        cr.set_source_rgba(*color, alpha)
        cr.fill()

    def circle(cx, cy, r, alpha):
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.set_source_rgba(1, 1, 1, alpha)
        cr.fill()

    if kind == "breeze":
        circle(w / 2, h * 0.38, 16, 0.85)
        block(w / 2 - 26, h * 0.38 + 22, 52, 6, 0.8)
        block(w / 2 - 50, h * 0.38 + 36, 100, 14, 0.25, 4)
        block(w / 2 + 52, h * 0.38 + 36, 14, 14, 0.45, 4)
        block(w - 44, h - 14, 34, 5, 0.5)
    elif kind == "orkalinux-glass":
        block(w / 2 - 36, 14, 72, 20, 0.9, 4)
        block(w / 2 - 28, 38, 56, 5, 0.6)
        circle(w / 2, h * 0.55, 13, 0.3)
        block(w / 2 - 22, h * 0.55 + 18, 44, 5, 0.85)
        block(w / 2 - 54, h * 0.55 + 30, 108, 16, 0.22, 8)
        cr.arc(w / 2 + 46, h * 0.55 + 38, 6, 0, 6.2832)
        cr.set_source_rgba(0.31, 0.35, 0.94, 1)
        cr.fill()
        for i in range(3):
            block(w - 30 - i * 22, h - 14, 18, 7, 0.3, 3)
    else:
        block(0, 0, w * 0.36, h, 0.82, 0, (0.027, 0.043, 0.15))
        block(12, 18, 56, 18, 0.9, 4)
        block(12, 40, 44, 5, 0.6)
        circle(24, h - 64, 10, 0.3)
        block(12, h - 48, 40, 5, 0.85)
        block(12, h - 38, w * 0.36 - 24, 14, 0.22, 7)
        block(12, h - 14, 30, 6, 0.3, 3)
    cr.reset_clip()


def draw_boot_preview(kind, cr, w, h, t, dot=8):
    import math
    rounded(cr, 0, 0, w, h, 10)
    cr.set_source_rgb(0.06, 0.07, 0.13)
    cr.fill()
    if kind == "text":
        rounded(cr, 0, 0, w, h, 10)
        cr.set_source_rgb(0, 0, 0)
        cr.fill()
        cr.select_font_face("Monospace")
        cr.set_font_size(7.5)
        cr.set_source_rgb(0.85, 0.87, 1)
        cr.move_to(10, 16)
        cr.show_text("OrkaLinux - by _inc0gnit0")
        lines = ["Started Journal Service", "Reached target Local File Systems",
                 "Started Network Manager", "Started Bluetooth service",
                 "Reached target Graphical Interface", "Started Simple Desktop Display Manager"]
        shown = int((t * 2.5) % (len(lines) + 3))
        for i, text in enumerate(lines[:shown]):
            y = 32 + i * 13
            cr.set_source_rgb(0.85, 0.87, 1)
            cr.move_to(10, y)
            cr.show_text("[")
            cr.set_source_rgb(0.30, 0.85, 0.45)
            cr.show_text("  OK  ")
            cr.set_source_rgb(0.85, 0.87, 1)
            cr.show_text("] " + text)
        return
    cx, cy = w / 2, h * 0.42
    cr.set_source_rgba(1, 1, 1, 0.92)
    cr.rectangle(cx - 6, cy - 20, 6, 32)
    cr.rectangle(cx + 4, cy - 26, 6, 44)
    cr.rectangle(cx - 22, cy + 2, 46, 6)
    cr.fill()
    cr.save()
    cr.translate(cx, cy - 6)
    cr.rotate(-0.30)
    cr.rectangle(-26, -3, 50, 6)
    cr.restore()
    cr.fill()
    if kind == "orkalinux":
        tw = 70
        ty = cy + 34
        cr.set_source_rgba(1, 1, 1, 0.15)
        rounded(cr, cx - tw / 2, ty, tw, 3, 1.5)
        cr.fill()
        p = 0.5 - 0.5 * math.cos(2 * math.pi * ((t / 2.8) % 1))
        cr.set_source_rgba(0.55, 0.60, 1.0, 1)
        rounded(cr, cx - tw / 2 + (tw - 22) * p, ty, 22, 3, 1.5)
        cr.fill()
    else:
        dy = h * 0.80
        for i in range(5):
            ph = ((t - i * 0.14) / 2.2) % 1
            a = 2 * math.pi * (ph - 0.16 * math.sin(2 * math.pi * ph))
            cr.arc(cx + dot * 0.875 * math.sin(a), dy - dot * 0.875 * math.cos(a), dot * 0.175, 0, 6.2832)
            cr.set_source_rgba(1, 1, 1, 1 - i * 0.12)
            cr.fill()


def current_login_theme():
    try:
        with open(SDDM_CONF, encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("Current="):
                    return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return "breeze"


def text_boot():
    for p in ("/etc/default/grub", "/etc/kernel/cmdline"):
        try:
            with open(p, encoding="utf-8") as f:
                for line in f:
                    if "plymouth.enable=0" in line and not line.lstrip().startswith("#"):
                        return True
        except OSError:
            pass
    return False


def current_boot_theme():
    if text_boot():
        return "text"
    try:
        with open("/etc/plymouth/plymouthd.conf", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("Theme="):
                    return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return "orkalinux"


def current_dot_size():
    try:
        with open(DOTS_SCRIPT, encoding="utf-8") as f:
            for line in f:
                if line.startswith("dot_size = "):
                    return int(line.split("=")[1].strip(" ;\n"))
    except (OSError, ValueError):
        pass
    return 8


def wallpaper_packages():
    lang = orka.system_lang()
    seen = set()
    found = []
    dirs = ["/usr/share/desktop-base/orkalinux-theme/wallpaper"] + sorted(glob.glob("/usr/share/wallpapers/*"))
    for path in dirs:
        real = os.path.realpath(path)
        if real in seen or not os.path.isdir(real):
            continue
        seen.add(real)
        name = os.path.basename(path)
        author = ""
        try:
            with open(os.path.join(real, "metadata.json"), encoding="utf-8") as f:
                plugin = json.load(f).get("KPlugin", {})
                name = plugin.get("Name[%s]" % lang, plugin.get("Name", name))
                authors = plugin.get("Authors") or []
                author = ", ".join(a.get("Name", "") for a in authors if a.get("Name"))
        except (OSError, ValueError, AttributeError):
            pass
        sub = "images_dark" if orka.is_dark_mode() and os.path.isdir(os.path.join(real, "contents/images_dark")) else "images"
        images = glob.glob(os.path.join(real, "contents", sub, "*"))
        if not images:
            continue

        def width(p):
            try:
                return int(os.path.basename(p).split("x")[0])
            except ValueError:
                return 99999
        found.append((real, name, author, min(images, key=width)))
    return found


class OrkaWyglad(orka.PagedWindow):
    def __init__(self):
        t = orka.Texts(TEXTS)
        super().__init__("orka-wyglad", t["title"], t["subtitle"], "orka-wyglad")
        self.t = t
        self.add_page("layout", self.t["p_layout"], "preferences-desktop", self.page_layout(), self.t["p_layout_sub"])
        self.add_page("colors", self.t["p_colors"], "preferences-desktop-color", self.page_colors(), self.t["p_colors_sub"])
        self.add_page("wall", self.t["p_wall"], "preferences-desktop-wallpaper", self.page_wallpaper(), self.t["p_wall_sub"])
        self.add_page("fx", self.t["p_fx"], "preferences-desktop-effects", self.page_effects(), self.t["p_fx_sub"])
        self.add_page("login", self.t["p_login"], "system-lock-screen", self.page_login(), self.t["p_login_sub"])
        self.add_page("boot", self.t["p_boot"], "system-reboot", self.page_boot(), self.t["p_boot_sub"])
        self.show_all()


    def page_layout(self):
        grid = Gtk.Grid(column_spacing=14, row_spacing=14, column_homogeneous=True)
        for i, kind in enumerate(("orka", "windows", "mac", "classic")):
            btn = Gtk.Button()
            btn.get_style_context().add_class("tile")
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            area = Gtk.DrawingArea()
            area.set_size_request(240, 140)
            area.connect("draw", lambda a, cr, k=kind: draw_layout_preview(
                k, cr, a.get_allocated_width(), a.get_allocated_height()))
            box.pack_start(area, False, False, 0)
            key = {"orka": "l_orka", "windows": "l_win", "mac": "l_mac", "classic": "l_classic"}[kind]
            box.pack_start(orka.label(self.t[key], "tile-name"), False, False, 0)
            box.pack_start(orka.label(self.t[key + "_d"], "tile-desc"), False, False, 0)
            btn.add(box)
            btn.connect("clicked", lambda *_, k=kind: self.apply_layout(k))
            grid.attach(btn, i % 2, i // 2, 1, 1)
        return grid

    def apply_layout(self, kind):
        if not self.confirm(self.t["layout_q"], self.t["layout_q2"], self.t["change"], self.t["cancel"]):
            return
        if not orka.plasma_script(JS_COMMON + LAYOUTS[kind]):
            self.message(self.t["failed"], self.t["failed_plasma"], Gtk.MessageType.ERROR)


    def page_colors(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.pack_start(orka.label(self.t["mode"], "section"), False, False, 0)
        modes = Gtk.Box(spacing=14, homogeneous=True)
        self.mode_buttons = {}
        for dark in (True, False):
            btn = Gtk.Button()
            btn.get_style_context().add_class("tile")
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            area = Gtk.DrawingArea()
            area.set_size_request(220, 110)
            area.connect("draw", self.draw_mode_preview, dark)
            box.pack_start(area, False, False, 0)
            box.pack_start(orka.label(self.t["dark" if dark else "light"], "tile-name", xalign=0.5), False, False, 0)
            btn.add(box)
            btn.connect("clicked", lambda *_, d=dark: self.set_mode(d))
            modes.pack_start(btn, True, True, 0)
            self.mode_buttons[dark] = btn
        self.mark_mode(orka.is_dark_mode())
        page.pack_start(modes, False, False, 0)

        page.pack_start(orka.label(self.t["accent"], "section"), False, False, 6)
        row = Gtk.FlowBox()
        row.set_selection_mode(Gtk.SelectionMode.NONE)
        row.set_max_children_per_line(10)
        for color in ACCENTS:
            row.add(self.swatch(color))
        auto = orka.button(self.t["accent_auto"], "ghost", self.set_accent, None)
        auto.set_valign(Gtk.Align.CENTER)
        row.add(auto)
        page.pack_start(row, False, False, 0)
        return page

    def draw_mode_preview(self, area, cr, dark):
        w, h = area.get_allocated_width(), area.get_allocated_height()
        bg = (0.09, 0.10, 0.17) if dark else (0.93, 0.94, 0.98)
        fg = (0.93, 0.93, 0.98) if dark else (0.10, 0.11, 0.17)
        side = (0.13, 0.14, 0.24) if dark else (0.86, 0.88, 0.96)
        cr.set_source_rgb(*bg)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        cr.set_source_rgb(*side)
        cr.rectangle(0, 0, w * 0.28, h)
        cr.fill()
        for i in range(4):
            cr.set_source_rgba(*fg, 0.8 if i == 0 else 0.35)
            cr.rectangle(w * 0.34, 16 + i * 20, w * (0.55 - i * 0.08), 8)
            cr.fill()
        cr.set_source_rgb(0.31, 0.35, 0.94)
        cr.rectangle(w * 0.34, h - 26, 60, 14)
        cr.fill()

    def mark_mode(self, dark):
        for d, btn in self.mode_buttons.items():
            ctx = btn.get_style_context()
            (ctx.add_class if d == dark else ctx.remove_class)("selected")

    def set_mode(self, dark):
        self.mark_mode(dark)
        if not orka.apply_dark_mode(dark):
            self.message(self.t["failed"], kind=Gtk.MessageType.ERROR)

    def swatch(self, color):
        btn = Gtk.Button()
        btn.set_size_request(44, 44)
        btn.set_tooltip_text(color)
        css = Gtk.CssProvider()
        css.load_from_data((
            "button { background-image: none; background-color: %s; border-radius: 22px;"
            " border: 3px solid rgba(255,255,255,0.15); min-width: 36px; min-height: 36px; }"
            " button:hover { border-color: #ffffff; }" % color).encode())
        btn.get_style_context().add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)
        btn.connect("clicked", lambda *_: self.set_accent(color))
        return btn

    def set_accent(self, color):
        if color is None:
            ok = orka.kwrite("kdeglobals", ["General"], "accentColorFromWallpaper", True)
        else:
            orka.kwrite("kdeglobals", ["General"], "accentColorFromWallpaper", False)
            try:
                ok = subprocess.run(["plasma-apply-colorscheme", "--accent-color", color],
                                    capture_output=True, timeout=30).returncode == 0
            except (OSError, subprocess.SubprocessError):
                ok = False
            if not ok:
                rgb = ",".join(str(int(color[i:i + 2], 16)) for i in (1, 3, 5))
                ok = orka.kwrite("kdeglobals", ["General"], "AccentColor", rgb)
        if not ok:
            self.message(self.t["failed"], kind=Gtk.MessageType.ERROR)


    def page_wallpaper(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        top = Gtk.Box(spacing=12)
        self.lock_too = Gtk.CheckButton(label=self.t["lock_too"])
        self.lock_too.set_active(True)
        top.pack_start(self.lock_too, False, False, 0)
        top.pack_end(orka.button(self.t["own_wall"], "ghost", self.pick_own_wallpaper), False, False, 0)
        page.pack_start(top, False, False, 0)

        self.wall_box = Gtk.FlowBox()
        self.wall_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.wall_box.set_max_children_per_line(4)
        self.wall_box.set_min_children_per_line(2)
        self.wall_box.set_column_spacing(12)
        self.wall_box.set_row_spacing(12)
        self.wall_box.set_homogeneous(True)
        page.pack_start(self.wall_box, False, False, 0)
        self.wall_queue = wallpaper_packages()
        GLib.idle_add(self.load_next_wallpaper)
        return page

    def load_next_wallpaper(self):
        if not self.wall_queue:
            return GLib.SOURCE_REMOVE
        path, name, author, image = self.wall_queue.pop(0)
        try:
            pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(image, 200, 112, False)
        except GLib.Error:
            return GLib.SOURCE_CONTINUE
        btn = Gtk.Button()
        btn.get_style_context().add_class("tile")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(Gtk.Image.new_from_pixbuf(pix), False, False, 0)
        lab = orka.label(name, "tile-name", xalign=0.5)
        lab.set_ellipsize(3)
        lab.set_max_width_chars(24)
        box.pack_start(lab, False, False, 0)
        if author:
            by = orka.label(self.t["by"].format(a=author), "tile-desc", xalign=0.5)
            by.set_ellipsize(3)
            by.set_max_width_chars(28)
            box.pack_start(by, False, False, 0)
        btn.add(box)
        btn.connect("clicked", lambda *_: self.set_wallpaper(path + "/"))
        btn.show_all()
        self.wall_box.add(btn)
        return GLib.SOURCE_CONTINUE

    def pick_own_wallpaper(self):
        dialog = Gtk.FileChooserDialog(title=self.t["pick_image"], transient_for=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_button(self.t["cancel"], Gtk.ResponseType.CANCEL)
        dialog.add_button(self.t["apply"], Gtk.ResponseType.OK)
        filt = Gtk.FileFilter()
        filt.set_name(self.t["images"])
        filt.add_mime_type("image/*")
        dialog.add_filter(filt)
        pictures = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)
        if pictures:
            dialog.set_current_folder(pictures)
        if dialog.run() == Gtk.ResponseType.OK:
            self.set_wallpaper(dialog.get_filename())
        dialog.destroy()

    def set_wallpaper(self, path):
        url = "file://" + path
        js = """
var ds = desktops();
for (var i = 0; i < ds.length; i++) {
    ds[i].wallpaperPlugin = "org.kde.image";
    ds[i].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    ds[i].writeConfig("Image", %s);
}
""" % json.dumps(url)
        if not orka.plasma_script(js):
            self.message(self.t["failed"], self.t["failed_plasma"], Gtk.MessageType.ERROR)
            return
        if self.lock_too.get_active():
            orka.kwrite("kscreenlockerrc", ["Greeter", "Wallpaper", "org.kde.image", "General"], "Image", url)


    def theme_tile(self, key, draw, on_click, in_use):
        """Kafelek z podglądem, nazwą, opisem i znaczkiem "Używany"."""
        btn = Gtk.Button()
        btn.get_style_context().add_class("tile")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        area = Gtk.DrawingArea()
        area.set_size_request(240, 140)
        area.connect("draw", lambda a, cr: draw(cr, a.get_allocated_width(), a.get_allocated_height()))
        box.pack_start(area, False, False, 0)
        name = Gtk.Box(spacing=8)
        name.pack_start(orka.label(self.t[key], "tile-name"), False, False, 0)
        badge = orka.label(self.t["in_use"], "badge-ok")
        badge.set_valign(Gtk.Align.CENTER)
        badge.set_no_show_all(True)
        badge.set_visible(in_use)
        name.pack_start(badge, False, False, 0)
        box.pack_start(name, False, False, 0)
        box.pack_start(orka.label(self.t[key + "_d"], "tile-desc", wrap=True), False, False, 0)
        btn.add(box)
        btn.set_sensitive(not orka.IS_LIVE)
        btn.connect("clicked", lambda *_: on_click())
        if in_use:
            btn.get_style_context().add_class("selected")
        return btn, badge, area

    def mark_theme(self, tiles, chosen):
        for name, (btn, badge, _area) in tiles.items():
            badge.set_visible(name == chosen)
            ctx = btn.get_style_context()
            if name == chosen:
                ctx.add_class("selected")
            else:
                ctx.remove_class("selected")

    def page_login(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        grid = Gtk.Grid(column_spacing=14, row_spacing=14, column_homogeneous=True)
        current = current_login_theme()
        self.login_tiles = {}
        for i, (name, key) in enumerate(LOGIN_THEMES):
            tile = self.theme_tile(key, lambda cr, w, h, n=name: draw_login_preview(n, cr, w, h),
                                   lambda n=name: self.set_login(n), name == current)
            self.login_tiles[name] = tile
            grid.attach(tile[0], i % 2, i // 2, 1, 1)
        page.pack_start(grid, False, False, 0)
        page.pack_start(orka.label(self.t["login_note"], "dim", wrap=True), False, False, 0)
        if orka.IS_LIVE:
            page.pack_start(orka.label(self.t["live_only_installed"], "dim", wrap=True), False, False, 0)
        return page

    def set_login(self, name):
        if name == current_login_theme():
            return
        orka.run_in_terminal(self, ["sudo", HELPER, "login", name], self.t,
                             lambda: self.mark_theme(self.login_tiles, current_login_theme()))

    def page_boot(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        grid = Gtk.Grid(column_spacing=14, row_spacing=14, column_homogeneous=True)
        current = current_boot_theme()
        self.boot_tiles = {}
        self.boot_t = 0.0
        self.dot_size = current_dot_size()
        for i, (name, key) in enumerate(BOOT_THEMES):
            tile = self.theme_tile(key, lambda cr, w, h, n=name: draw_boot_preview(n, cr, w, h, self.boot_t,
                                                                                    self.dot_size),
                                   lambda n=name: self.set_boot(n), name == current)
            self.boot_tiles[name] = tile
            tile[2].add_tick_callback(self.on_boot_tick)
            grid.attach(tile[0], i % 2, i // 2, 1, 1)
        page.pack_start(grid, False, False, 0)

        page.pack_start(orka.label(self.t["dot_size"], "section"), False, False, 0)
        row = Gtk.Box(spacing=8)
        self.dot_buttons = {}
        self.dot_lock = False
        for key, px in DOT_SIZES:
            b = Gtk.ToggleButton(label=self.t["ds_" + key])
            b.get_style_context().add_class("tab")
            b.set_active(px == self.dot_size)
            b.set_sensitive(not orka.IS_LIVE)
            b.connect("toggled", self.on_dot_toggled, key, px)
            self.dot_buttons[px] = b
            row.pack_start(b, False, False, 0)
        self.dot_apply = Gtk.Button(label=self.t["dot_apply"])
        self.dot_apply.get_style_context().add_class("primary")
        self.dot_apply.connect("clicked", lambda *_: self.apply_dots())
        row.pack_end(self.dot_apply, False, False, 0)
        page.pack_start(row, False, False, 0)
        self.update_dot_apply()
        page.pack_start(orka.label(self.t["dot_size_d"], "dim", wrap=True), False, False, 0)
        if orka.IS_LIVE:
            page.pack_start(orka.label(self.t["live_only_installed"], "dim", wrap=True), False, False, 0)
        return page

    def mark_dots(self, px):
        self.dot_lock = True
        for size, b in self.dot_buttons.items():
            b.set_active(size == px)
        self.dot_lock = False

    def on_dot_toggled(self, button, key, px):
        if self.dot_lock:
            return
        self.mark_dots(px)
        self.dot_size = px
        self.update_dot_apply()

    def update_dot_apply(self):
        same = self.dot_size == current_dot_size() and current_boot_theme() == "orkalinux-dots"
        self.dot_apply.set_sensitive(not same and not orka.IS_LIVE)

    def apply_dots(self):
        key = dict((px, k) for k, px in DOT_SIZES)[self.dot_size]

        def done():
            self.dot_size = current_dot_size()
            self.mark_dots(self.dot_size)
            self.mark_theme(self.boot_tiles, current_boot_theme())
            self.update_dot_apply()
        orka.run_in_terminal(self, ["sudo", HELPER, "dots", key], self.t, done)

    def on_boot_tick(self, widget, clock):
        self.boot_t = clock.get_frame_time() / 1_000_000
        widget.queue_draw()
        return GLib.SOURCE_CONTINUE

    def set_boot(self, name):
        if name == current_boot_theme():
            return
        orka.run_in_terminal(self, ["sudo", HELPER, "boot", name], self.t,
                             lambda: (self.mark_theme(self.boot_tiles, current_boot_theme()),
                                      self.update_dot_apply()))


    def page_effects(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        effects = [
            ("wobblywindowsEnabled", "fx_wobbly", False),
            ("magiclampEnabled", "fx_lamp", False),
            ("blurEnabled", "fx_blur", True),
            ("translucencyEnabled", "fx_move", False),
        ]
        for key, text, default in effects:
            row = Gtk.Box(spacing=14)
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            texts.pack_start(orka.label(self.t[text], "big"), False, False, 0)
            texts.pack_start(orka.label(self.t[text + "_d"], "dim"), False, False, 0)
            row.pack_start(texts, True, True, 0)
            switch = Gtk.Switch()
            switch.set_valign(Gtk.Align.CENTER)
            current = orka.kread("kwinrc", ["Plugins"], key, "true" if default else "false")
            switch.set_active(current.lower() == "true")
            switch.connect("notify::active", self.on_effect, key)
            row.pack_end(switch, False, False, 0)
            page.pack_start(orka.card(row), False, False, 0)

        speed_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        speed_box.pack_start(orka.label(self.t["speed"], "big"), False, False, 0)
        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 3, 1)
        scale.set_draw_value(False)
        for i, key in enumerate(("s_off", "s_fast", "s_normal", "s_slow")):
            scale.add_mark(i, Gtk.PositionType.BOTTOM, self.t[key])
        try:
            factor = float(orka.kread("kdeglobals", ["KDE"], "AnimationDurationFactor", "1"))
        except ValueError:
            factor = 1.0
        scale.set_value(min(range(4), key=lambda i: abs(SPEEDS[i] - factor)))
        scale.connect("value-changed", self.on_speed)
        speed_box.pack_start(scale, False, False, 0)
        page.pack_start(orka.card(speed_box), False, False, 6)
        return page

    def on_effect(self, switch, _param, key):
        on = switch.get_active()
        orka.kwrite("kwinrc", ["Plugins"], key, on)
        orka.kwin_effect(key[:-len("Enabled")], on)

    def on_speed(self, scale):
        pos = int(round(scale.get_value()))
        if abs(scale.get_value() - pos) > 0.01:
            scale.set_value(pos)
            return
        orka.kwrite("kdeglobals", ["KDE"], "AnimationDurationFactor", SPEEDS[pos])
        orka.kwin_reconfigure()


if __name__ == "__main__":
    OrkaWyglad()
    orka.run()
