#!/usr/bin/env python3
import math
import os
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
IS_LIVE = os.path.exists("/run/live/medium")

TRANSLATIONS = {
    "pl": {
        "title": "Witaj w OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Dziękujemy za wybranie OrkaLinux! To system oparty na Debianie 13 (Trixie) z pulpitem KDE Plasma. Możesz go wypróbować bez instalacji albo od razu zainstalować na dysku.",
        "welcome_text_installed": "Dziękujemy za zainstalowanie OrkaLinux! Cieszymy się, że jesteś częścią naszej społeczności – mamy nadzieję, że zostaniesz z nami na dłużej.",
        "btn_readme": "Readme", "desc_readme": "Co jest w systemie",
        "btn_release": "Info o wydaniu", "desc_release": "Nowości i znane problemy",
        "btn_site": "Strona projektu", "desc_site": "Pobieranie i aktualności",
        "btn_discord": "Discord", "desc_discord": "Pogadaj ze społecznością",
        "btn_youtube": "YouTube", "desc_youtube": "Filmy i poradniki",
        "btn_apps": "Aplikacje", "desc_apps": "Instaluj nowe programy",
        "btn_install": "Zainstaluj OrkaLinux",
        "autostart": "Uruchamiaj przy starcie",
        "close": "Zamknij",
        "readme_text": "OrkaLinux Beta @ORKA_VERSION_ID@\n================\n\nOrkaLinux to dystrybucja Linuksa oparta na Debianie 13 (Trixie)\nz pulpitem KDE Plasma, stworzona przez _inc0gnit0.\n\nCo jest zawarte w systemie:\n- Firefox - przeglądarka internetowa\n- Discord - komunikator\n- VLC - odtwarzacz multimediów\n- LibreOffice - pakiet biurowy\n- Fastfetch - informacje o systemie\n- Calamares - instalator systemu\n\nStrona projektu:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@) - Informacje o wydaniu\n========================================\n\nWersja: Beta @ORKA_VERSION_ID@\nBaza: Debian 13 (Trixie)\nPulpit: KDE Plasma 6.3\nKernel: Linux 6.12\n\nTo jest wersja BETA - może zawierać błędy.\nProsimy o zgłaszanie problemów na naszym Discordzie:\n@ORKA_DISCORD@\n\nZnane problemy:\n- Niektóre funkcje mogą nie działać poprawnie\n\nDziękujemy za testowanie OrkaLinux!",
    },
    "en": {
        "title": "Welcome to OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Thank you for choosing OrkaLinux! It is based on Debian 13 (Trixie) with the KDE Plasma desktop. Try it without installing, or install it to your disk right away.",
        "welcome_text_installed": "Thank you for installing OrkaLinux! We are glad you are part of our community – we hope you stay with us for a long time.",
        "btn_readme": "Read me", "desc_readme": "What is included",
        "btn_release": "Release info", "desc_release": "What's new, known issues",
        "btn_site": "Project website", "desc_site": "Downloads and news",
        "btn_discord": "Discord", "desc_discord": "Chat with the community",
        "btn_youtube": "YouTube", "desc_youtube": "Videos and guides",
        "btn_apps": "Applications", "desc_apps": "Install new software",
        "btn_install": "Install OrkaLinux",
        "autostart": "Launch at startup",
        "close": "Close",
        "readme_text": "OrkaLinux Beta @ORKA_VERSION_ID@\n================\n\nOrkaLinux is a Linux distribution based on Debian 13 (Trixie)\nwith KDE Plasma desktop, created by _inc0gnit0.\n\nWhat is included:\n- Firefox - web browser\n- Discord - messenger\n- VLC - media player\n- LibreOffice - office suite\n- Fastfetch - system information\n- Calamares - system installer\n\nProject website:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@) - Release Notes\n=================================\n\nVersion: Beta @ORKA_VERSION_ID@\nBase: Debian 13 (Trixie)\nDesktop: KDE Plasma 6.3\nKernel: Linux 6.12\n\nThis is a BETA version - may contain bugs.\nPlease report issues on our Discord:\n@ORKA_DISCORD@\n\nKnown issues:\n- Some features may not work correctly\n\nThank you for testing OrkaLinux!",
    },
    "de": {
        "title": "Willkommen bei OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Danke, dass Sie OrkaLinux gewählt haben! Es basiert auf Debian 13 (Trixie) mit dem KDE Plasma Desktop. Sie können es ohne Installation testen oder direkt installieren.",
        "welcome_text_installed": "Danke für die Installation von OrkaLinux! Wir freuen uns, dass Sie Teil unserer Community sind.",
        "btn_readme": "Readme", "desc_readme": "Was enthalten ist",
        "btn_release": "Versionshinweise", "desc_release": "Neues und bekannte Probleme",
        "btn_site": "Projektseite", "desc_site": "Downloads und News",
        "btn_discord": "Discord", "desc_discord": "Mit der Community chatten",
        "btn_youtube": "YouTube", "desc_youtube": "Videos und Anleitungen",
        "btn_apps": "Anwendungen", "desc_apps": "Neue Programme installieren",
        "btn_install": "OrkaLinux installieren",
        "autostart": "Beim Start ausführen",
        "close": "Schließen",
        "readme_text": "OrkaLinux Beta @ORKA_VERSION_ID@\n================\n\nOrkaLinux ist eine Linux-Distribution basierend auf Debian 13.\n\nProjektseite:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@) - Versionshinweise\n====================================\n\nVersion: Beta @ORKA_VERSION_ID@\nBasis: Debian 13 (Trixie)\nDesktop: KDE Plasma 6.3\nKernel: Linux 6.12",
    },
    "fr": {
        "title": "Bienvenue sur OrkaLinux!",
        "subtitle": "@ORKA_VERSION@ (@ORKA_CODENAME@) · by _inc0gnit0",
        "welcome_text_live": "Merci d'avoir choisi OrkaLinux! Il est basé sur Debian 13 (Trixie) avec le bureau KDE Plasma. Essayez-le sans installation ou installez-le directement.",
        "welcome_text_installed": "Merci d'avoir installé OrkaLinux! Nous sommes ravis que vous fassiez partie de notre communauté.",
        "btn_readme": "Lisez-moi", "desc_readme": "Ce qui est inclus",
        "btn_release": "Notes de version", "desc_release": "Nouveautés et problèmes",
        "btn_site": "Site du projet", "desc_site": "Téléchargements et actus",
        "btn_discord": "Discord", "desc_discord": "Discuter avec la communauté",
        "btn_youtube": "YouTube", "desc_youtube": "Vidéos et tutoriels",
        "btn_apps": "Applications", "desc_apps": "Installer des logiciels",
        "btn_install": "Installer OrkaLinux",
        "autostart": "Lancer au démarrage",
        "close": "Fermer",
        "readme_text": "OrkaLinux Beta @ORKA_VERSION_ID@\n================\n\nOrkaLinux est une distribution Linux basée sur Debian 13.\n\nSite du projet:\n@ORKA_URL@\n\nDiscord:\n@ORKA_DISCORD@",
        "release_text": "OrkaLinux @ORKA_VERSION@ (@ORKA_CODENAME@) - Notes de version\n=====================================\n\nVersion: Beta @ORKA_VERSION_ID@\nBase: Debian 13 (Trixie)\nBureau: KDE Plasma 6.3\nNoyau: Linux 6.12",
    },
}

LANG_NAMES = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
}

CARDS = [
    ("readme", ["help-about", "dialog-information"], "dialog:readme_text"),
    ("release", ["text-x-changelog", "text-x-generic"], "dialog:release_text"),
    ("site", ["internet-web-browser", "applications-internet"], SITE_URL),
    ("discord", ["discord", "applications-internet"], DISCORD_URL),
    ("youtube", ["youtube", "applications-multimedia", "video-x-generic"], YOUTUBE_URL),
    ("apps", ["plasmadiscover", "system-software-install", "applications-other"], "plasma-discover"),
]

WAVES = [
    (10.0, 140.0, 0.55, 0.62, 0.30),
    (14.0, 210.0, -0.35, 0.74, 0.40),
    (8.0, 95.0, 0.80, 0.86, 0.55),
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

dialog.orka, dialog.orka box, dialog.orka scrolledwindow, dialog.orka viewport { background-color: #0b1033; }
dialog.orka label { color: #e3e7ff; font-family: monospace; }
"""


def first_icon(names):
    theme = Gtk.IconTheme.get_default()
    for name in names:
        if theme.has_icon(name):
            return name
    return names[-1]


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
        bg = cairo.LinearGradient(0, 0, w * 0.3, h)
        bg.add_color_stop_rgb(0, 0.012, 0.020, 0.110)
        bg.add_color_stop_rgb(1, 0.035, 0.060, 0.420)
        cr.set_source(bg)
        cr.paint()
        for i, (amp, length, speed, level, alpha) in enumerate(WAVES):
            cr.move_to(0, h)
            x = 0.0
            while x <= w + 8:
                y = h * level + amp * math.sin(x / length + self.t * speed + i * 1.7)
                cr.line_to(x, y)
                x += 6
            cr.line_to(w, h)
            cr.close_path()
            cr.set_source_rgba(0.10, 0.16, 0.95, alpha)
            cr.fill()
        return False


class OrkaLinuxHello(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.lang = "pl"
        self.tr = TRANSLATIONS[self.lang]
        self.set_title(self.tr["title"])
        self.set_icon_name("orkalinux")
        self.set_default_size(860, -1)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.get_style_context().add_class("orka")

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.root)
        self.build_ui()

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
        self.root.pack_start(body, True, True, 0)

        welcome = Gtk.Label(label=self.tr["welcome_text_live" if IS_LIVE else "welcome_text_installed"])
        welcome.set_line_wrap(True)
        welcome.set_max_width_chars(90)
        welcome.set_xalign(0)
        welcome.get_style_context().add_class("welcome")
        body.pack_start(self.animated(welcome), False, False, 0)

        grid = Gtk.Grid(column_spacing=12, row_spacing=12, column_homogeneous=True)
        for i, (key, icons, action) in enumerate(CARDS):
            grid.attach(self.animated(self.build_card(key, icons, action)), i % 3, i // 3, 1, 1)
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
            install.connect("clicked", self.on_action, "calamares-install-debian")
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
        elif action.startswith("http"):
            subprocess.Popen(["xdg-open", action])
        else:
            subprocess.Popen([action])

    def show_text_dialog(self, text_key):
        title = self.tr["btn_readme" if text_key == "readme_text" else "btn_release"]
        dialog = Gtk.Dialog(title=title, transient_for=self, modal=True)
        dialog.get_style_context().add_class("orka")
        dialog.set_default_size(620, 440)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        label = Gtk.Label(label=self.tr[text_key], xalign=0, yalign=0, selectable=True)
        label.set_margin_top(16)
        label.set_margin_bottom(16)
        label.set_margin_start(18)
        label.set_margin_end(18)
        scrolled.add(label)
        dialog.get_content_area().pack_start(scrolled, True, True, 0)
        ok = dialog.add_button("OK", Gtk.ResponseType.OK)
        ok.get_style_context().add_class("ghost")
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def on_lang_changed(self, combo):
        lang = combo.get_active_id()
        if lang and lang != self.lang:
            self.lang = lang
            self.tr = TRANSLATIONS[lang]
            self.set_title(self.tr["title"])
            GLib.idle_add(self.build_ui)

    def on_autostart_toggled(self, switch, _param):
        if switch.get_active():
            os.makedirs(os.path.dirname(AUTOSTART_FILE), exist_ok=True)
            with open(AUTOSTART_FILE, "w") as f:
                f.write("[Desktop Entry]\nType=Application\nName=OrkaLinux Hello\n"
                        "Exec=/usr/share/orkalinux-hello/orkalinux-hello.py\nIcon=orkalinux\n"
                        "X-KDE-autostart-after=panel\n")
        elif os.path.exists(AUTOSTART_FILE):
            os.remove(AUTOSTART_FILE)


if __name__ == "__main__":
    win = OrkaLinuxHello()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
