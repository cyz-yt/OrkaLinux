#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, Gio
import subprocess
import os

TRANSLATIONS = {
    "pl": {
        "title": "Witaj w OrkaLinux!",
        "subtitle": "OrkaLinux B1 (Deepwave) - by _inc0gnit0",
        "welcome_title": "Witaj w naszej społeczności!",
        "welcome_text_live": "Dziękujemy za wybranie OrkaLinux!\n\nOrkaLinux to system oparty na Debianie 12 (Bookworm)\nz pulpitem KDE Plasma. Mamy nadzieję, że spodoba\nCi się nasz system i zostaniesz z nami na dłużej!\n\nMożesz użyć systemu jako Live lub go zainstalować.",
        "welcome_text_installed": "Dziękujemy za zainstalowanie OrkaLinux!\nCieszymy się, że jesteś częścią naszej społeczności.\nMamy nadzieję, że będziesz zadowolony z systemu!",
        "doc_label": "DOKUMENTACJA",
        "support_label": "WSPARCIE",
        "project_label": "PROJEKT",
        "install_label": "INSTALACJA",
        "btn_readme": "Readme",
        "btn_release": "Info o wydaniu",
        "btn_discord": "Discord",
        "btn_site": "Strona projektu",
        "btn_youtube": "YouTube",
        "btn_install": "Zainstaluj OrkaLinux",
        "autostart": "Uruchamiaj przy starcie",
        "close": "Zamknij",
        "readme_text": "OrkaLinux Beta 1\n================\n\nOrkaLinux to dystrybucja Linuksa oparta na Debianie 12 (Bookworm)\nz pulpitem KDE Plasma, stworzona przez _inc0gnit0.\n\nCo jest zawarte w systemie:\n- Firefox - przeglądarka internetowa\n- Discord - komunikator\n- VLC - odtwarzacz multimediów\n- LibreOffice - pakiet biurowy\n- Fastfetch - informacje o systemie\n- Calamares - instalator systemu\n\nStrona projektu:\nhttps://sites.google.com/view/inc0gnit0/downloads/orka-linux\n\nDiscord:\nhttps://discord.gg/JkC9P6ebN2\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux Beta 1 - Informacje o wydaniu\n========================================\n\nWersja: Beta 1\nBaza: Debian 12 (Bookworm)\nPulpit: KDE Plasma 5.27\nKernel: Linux 6.1\n\nTo jest wersja BETA - może zawierać błędy.\nProsimy o zgłaszanie problemów na naszym Discordzie:\nhttps://discord.gg/JkC9P6ebN2\n\nZnane problemy:\n- Ekran ładowania może pokazywać logo Debiana\n- Niektóre funkcje mogą nie działać poprawnie\n\nDziękujemy za testowanie OrkaLinux!",
    },
    "en": {
        "title": "Welcome to OrkaLinux!",
        "subtitle": "OrkaLinux B1 (Deepwave) - by _inc0gnit0",
        "welcome_title": "Welcome to our community!",
        "welcome_text_live": "Thank you for choosing OrkaLinux!\n\nOrkaLinux is a system based on Debian 12 (Bookworm)\nwith KDE Plasma desktop. We hope you enjoy\nour system and stay with us for a long time!\n\nYou can use the system as Live or install it.",
        "welcome_text_installed": "Thank you for installing OrkaLinux!\nWe are glad you are part of our community.\nWe hope you enjoy the system!",
        "doc_label": "DOCUMENTATION",
        "support_label": "SUPPORT",
        "project_label": "PROJECT",
        "install_label": "INSTALLATION",
        "btn_readme": "Read me",
        "btn_release": "Release info",
        "btn_discord": "Discord",
        "btn_site": "Project website",
        "btn_youtube": "YouTube",
        "btn_install": "Install OrkaLinux",
        "autostart": "Launch at startup",
        "close": "Close",
        "readme_text": "OrkaLinux Beta 1\n================\n\nOrkaLinux is a Linux distribution based on Debian 12 (Bookworm)\nwith KDE Plasma desktop, created by _inc0gnit0.\n\nWhat is included:\n- Firefox - web browser\n- Discord - messenger\n- VLC - media player\n- LibreOffice - office suite\n- Fastfetch - system information\n- Calamares - system installer\n\nProject website:\nhttps://sites.google.com/view/inc0gnit0/downloads/orka-linux\n\nDiscord:\nhttps://discord.gg/JkC9P6ebN2\n\nYouTube:\nhttps://www.youtube.com/@_inc0gnit0",
        "release_text": "OrkaLinux Beta 1 - Release Notes\n=================================\n\nVersion: Beta 1\nBase: Debian 12 (Bookworm)\nDesktop: KDE Plasma 5.27\nKernel: Linux 6.1\n\nThis is a BETA version - may contain bugs.\nPlease report issues on our Discord:\nhttps://discord.gg/JkC9P6ebN2\n\nKnown issues:\n- Boot screen may show Debian logo\n- Some features may not work correctly\n\nThank you for testing OrkaLinux!",
    },
    "de": {
        "title": "Willkommen bei OrkaLinux!",
        "subtitle": "OrkaLinux B1 (Deepwave) - by _inc0gnit0",
        "welcome_title": "Willkommen in unserer Community!",
        "welcome_text_live": "Danke, dass Sie OrkaLinux gewählt haben!\n\nOrkaLinux basiert auf Debian 12 (Bookworm)\nmit KDE Plasma Desktop.\n\nSie können das System als Live nutzen oder installieren.",
        "welcome_text_installed": "Danke für die Installation von OrkaLinux!\nWir freuen uns, dass Sie Teil unserer Community sind.",
        "doc_label": "DOKUMENTATION",
        "support_label": "UNTERSTÜTZUNG",
        "project_label": "PROJEKT",
        "install_label": "INSTALLATION",
        "btn_readme": "Readme",
        "btn_release": "Versionshinweise",
        "btn_discord": "Discord",
        "btn_site": "Projektseite",
        "btn_youtube": "YouTube",
        "btn_install": "OrkaLinux installieren",
        "autostart": "Beim Start ausführen",
        "close": "Schließen",
        "readme_text": "OrkaLinux Beta 1\n================\n\nOrkaLinux ist eine Linux-Distribution basierend auf Debian 12.\n\nProjektseite:\nhttps://sites.google.com/view/inc0gnit0/downloads/orka-linux\n\nDiscord:\nhttps://discord.gg/JkC9P6ebN2",
        "release_text": "OrkaLinux Beta 1 - Versionshinweise\n====================================\n\nVersion: Beta 1\nBasis: Debian 12 (Bookworm)\nDesktop: KDE Plasma 5.27\nKernel: Linux 6.1",
    },
    "fr": {
        "title": "Bienvenue sur OrkaLinux!",
        "subtitle": "OrkaLinux B1 (Deepwave) - by _inc0gnit0",
        "welcome_title": "Bienvenue dans notre communauté!",
        "welcome_text_live": "Merci d'avoir choisi OrkaLinux!\n\nOrkaLinux est basé sur Debian 12 (Bookworm)\navec le bureau KDE Plasma.\n\nVous pouvez utiliser le système en Live ou l'installer.",
        "welcome_text_installed": "Merci d'avoir installé OrkaLinux!\nNous sommes ravis que vous fassiez partie de notre communauté.",
        "doc_label": "DOCUMENTATION",
        "support_label": "SUPPORT",
        "project_label": "PROJET",
        "install_label": "INSTALLATION",
        "btn_readme": "Lisez-moi",
        "btn_release": "Notes de version",
        "btn_discord": "Discord",
        "btn_site": "Site du projet",
        "btn_youtube": "YouTube",
        "btn_install": "Installer OrkaLinux",
        "autostart": "Lancer au démarrage",
        "close": "Fermer",
        "readme_text": "OrkaLinux Beta 1\n================\n\nOrkaLinux est une distribution Linux basée sur Debian 12.\n\nSite du projet:\nhttps://sites.google.com/view/inc0gnit0/downloads/orka-linux\n\nDiscord:\nhttps://discord.gg/JkC9P6ebN2",
        "release_text": "OrkaLinux Beta 1 - Notes de version\n=====================================\n\nVersion: Beta 1\nBase: Debian 12 (Bookworm)\nBureau: KDE Plasma 5.27\nNoyau: Linux 6.1",
    },
}

LANG_NAMES = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
}

IS_LIVE = os.path.exists("/run/live") or os.path.exists("/usr/share/live")

DARK_CSS = b"""
window, box, grid, scrolledwindow, viewport, dialog {
    background-color: #1a1a1a;
    color: #e0e0e0;
}
label { color: #e0e0e0; }
button {
    background-image: none;
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 4px 8px;
}
button:hover { background-color: #3d3d3d; }
separator { background-color: #3a3a3a; min-height: 1px; }
checkbutton label { color: #e0e0e0; }
combobox button { background-color: #2d2d2d; color: #e0e0e0; }
"""

LIGHT_CSS = b"""
window, box, grid, scrolledwindow, viewport, dialog {
    background-color: #f5f5f5;
    color: #222222;
}
label { color: #222222; }
button {
    background-image: none;
    background-color: #e8e8e8;
    color: #222222;
    border: 1px solid #bbbbbb;
    border-radius: 6px;
    padding: 4px 8px;
}
button:hover { background-color: #d0d0d0; }
separator { background-color: #cccccc; min-height: 1px; }
checkbutton label { color: #222222; }
"""

def is_dark_theme():
    try:
        settings = Gtk.Settings.get_default()
        theme = settings.get_property("gtk-theme-name").lower()
        if "dark" in theme:
            return True
        color_scheme = settings.get_property("gtk-application-prefer-dark-theme")
        if color_scheme:
            return True
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["kreadconfig5", "--group", "General", "--key", "ColorScheme"],
            capture_output=True, text=True)
        if "dark" in result.stdout.lower():
            return True
    except Exception:
        pass
    return False

class OrkaLinuxHello(Gtk.Window):
    def __init__(self):
        self.lang = "pl"
        self.dark = is_dark_theme()
        self.tr = TRANSLATIONS[self.lang]
        Gtk.Window.__init__(self, title=self.tr["title"])
        self.set_default_size(800, 650)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        self.css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        if self.dark:
            self.css_provider.load_from_data(DARK_CSS)
        else:
            self.css_provider.load_from_data(LIGHT_CSS)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_box.set_margin_top(20)
        self.main_box.set_margin_bottom(20)
        self.main_box.set_margin_start(20)
        self.main_box.set_margin_end(20)
        self.add(self.main_box)
        self.build_ui()

    def build_ui(self):
        for child in self.main_box.get_children():
            self.main_box.remove(child)

        top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        lang_combo = Gtk.ComboBoxText()
        for code, name in LANG_NAMES.items():
            lang_combo.append(code, name)
        lang_combo.set_active_id(self.lang)
        lang_combo.connect("changed", self.on_lang_changed)
        top_box.pack_start(lang_combo, False, False, 0)

        self.main_box.pack_start(top_box, False, False, 0)

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                "/usr/share/pixmaps/orkalinux/orkalinux-logo.png", 100, 100, True)
            logo = Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception:
            logo = Gtk.Image.new_from_icon_name("computer", Gtk.IconSize.DIALOG)
        self.main_box.pack_start(logo, False, False, 0)

        title = Gtk.Label()
        title.set_markup("<span font='22' weight='bold'>" + self.tr["welcome_title"] + "</span>")
        self.main_box.pack_start(title, False, False, 5)

        subtitle = Gtk.Label()
        subtitle.set_markup("<span font='10' color='gray'>" + self.tr["subtitle"] + "</span>")
        self.main_box.pack_start(subtitle, False, False, 0)

        self.main_box.pack_start(Gtk.Separator(), False, False, 5)

        welcome = Gtk.Label()
        if IS_LIVE:
            welcome.set_text(self.tr["welcome_text_live"])
        else:
            welcome.set_text(self.tr["welcome_text_installed"])
        welcome.set_justify(Gtk.Justification.CENTER)
        self.main_box.pack_start(welcome, False, False, 5)

        self.main_box.pack_start(Gtk.Separator(), False, False, 5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(grid, False, False, 0)

        for col, key in enumerate(["doc_label", "support_label", "project_label"]):
            lbl = Gtk.Label()
            lbl.set_markup("<b>" + self.tr[key] + "</b>")
            grid.attach(lbl, col, 0, 1, 1)

        btn_readme = Gtk.Button(label=self.tr["btn_readme"])
        btn_readme.set_size_request(200, 40)
        btn_readme.connect("clicked", self.show_text_dialog, "readme_text", "README")
        grid.attach(btn_readme, 0, 1, 1, 1)

        btn_release = Gtk.Button(label=self.tr["btn_release"])
        btn_release.set_size_request(200, 40)
        btn_release.connect("clicked", self.show_text_dialog, "release_text", "Release Info")
        grid.attach(btn_release, 0, 2, 1, 1)

        btn_discord = Gtk.Button(label=self.tr["btn_discord"])
        btn_discord.set_size_request(200, 40)
        btn_discord.connect("clicked", self.on_button_clicked, "https://discord.gg/JkC9P6ebN2")
        grid.attach(btn_discord, 1, 1, 1, 1)

        btn_youtube = Gtk.Button(label=self.tr["btn_youtube"])
        btn_youtube.set_size_request(200, 40)
        btn_youtube.connect("clicked", self.on_button_clicked, "https://www.youtube.com/@_inc0gnit0")
        grid.attach(btn_youtube, 1, 2, 1, 1)

        btn_site = Gtk.Button(label=self.tr["btn_site"])
        btn_site.set_size_request(200, 40)
        btn_site.connect("clicked", self.on_button_clicked, "https://sites.google.com/view/inc0gnit0/downloads/orka-linux")
        grid.attach(btn_site, 2, 1, 1, 1)

        if IS_LIVE:
            self.main_box.pack_start(Gtk.Separator(), False, False, 5)
            install_label = Gtk.Label()
            install_label.set_markup("<b>" + self.tr["install_label"] + "</b>")
            self.main_box.pack_start(install_label, False, False, 0)
            btn_install = Gtk.Button(label=self.tr["btn_install"])
            btn_install.set_size_request(300, 45)
            btn_install.set_halign(Gtk.Align.CENTER)
            btn_install.connect("clicked", self.on_button_clicked, "calamares")
            self.main_box.pack_start(btn_install, False, False, 0)

        self.main_box.pack_start(Gtk.Separator(), False, False, 5)

        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.autostart_check = Gtk.CheckButton(label=self.tr["autostart"])
        self.autostart_check.set_active(True)
        self.autostart_check.connect("toggled", self.on_autostart_toggled)
        bottom_box.pack_start(self.autostart_check, True, True, 0)
        close_btn = Gtk.Button(label=self.tr["close"])
        close_btn.set_size_request(100, 35)
        close_btn.connect("clicked", Gtk.main_quit)
        bottom_box.pack_end(close_btn, False, False, 0)
        self.main_box.pack_start(bottom_box, False, False, 0)

        self.show_all()

    def show_text_dialog(self, widget, text_key, title):
        text = self.tr[text_key]
        dialog = Gtk.Dialog(title=title, parent=self)
        dialog.set_default_size(600, 400)
        if self.dark:
            p = Gtk.CssProvider()
            p.load_from_data(DARK_CSS)
            dialog.get_style_context().add_provider(p, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_margin_top(10)
        scrolled.set_margin_bottom(10)
        scrolled.set_margin_start(10)
        scrolled.set_margin_end(10)
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        scrolled.add(label)
        dialog.get_content_area().pack_start(scrolled, True, True, 0)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def on_lang_changed(self, combo):
        lang = combo.get_active_id()
        if lang and lang != self.lang:
            self.lang = lang
            self.tr = TRANSLATIONS[lang]
            self.set_title(self.tr["title"])
            self.build_ui()

    def on_button_clicked(self, widget, action):
        if action.startswith("http"):
            subprocess.Popen(["xdg-open", action])
        elif action == "calamares":
            subprocess.Popen(["sudo", "calamares"])
        else:
            subprocess.Popen([action])

    def on_autostart_toggled(self, widget):
        autostart_file = os.path.expanduser("~/.config/autostart/orkalinux-hello.desktop")
        if widget.get_active():
            os.makedirs(os.path.dirname(autostart_file), exist_ok=True)
            with open(autostart_file, "w") as f:
                f.write("[Desktop Entry]\nType=Application\nName=OrkaLinux Hello\nExec=/usr/share/orkalinux-hello/orkalinux-hello.py\nHidden=false\n")
        else:
            if os.path.exists(autostart_file):
                os.remove(autostart_file)

win = OrkaLinuxHello()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
