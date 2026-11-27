import configparser
import math
import os
import shlex
import shutil
import subprocess
import sys
import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, Gtk

LANGS = ("en", "pl", "de", "fr")
LOGO_WHITE = "/usr/share/pixmaps/orkalinux/orkalinux-logo-white.png"
IS_LIVE = os.path.exists("/run/live/medium")
LANG_FILE = os.path.expanduser("~/.config/orkalinux/lang")
LANG_NAMES = {"en": "English", "pl": "Polski", "de": "Deutsch", "fr": "Français"}

ACCENT = "#4f58f0"


def system_lang():
    if IS_LIVE:
        try:
            with open(LANG_FILE) as f:
                code = f.read().strip()
            if code:
                return code if code in LANGS else "en"
        except OSError:
            pass
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var, "")
        if value and value not in ("C", "POSIX"):
            code = value.split(":")[0][:2]
            return code if code in LANGS else "en"
    return "en"


COMMON = {
    "en": {
        "close": "Close", "cancel": "Cancel", "apply": "Apply", "ok": "OK",
        "live_only_installed": "This works after OrkaLinux is installed. In the live system nothing is kept after a restart.",
        "term_done": "Done! This window will close in a moment.",
        "term_failed": "Something went wrong - check the messages above. Press Enter to close.",
        "no_terminal": "Could not open the terminal.",
    },
    "pl": {
        "close": "Zamknij", "cancel": "Anuluj", "apply": "Zastosuj", "ok": "OK",
        "live_only_installed": "To działa po zainstalowaniu OrkaLinux. W wersji live po restarcie nic nie zostaje.",
        "term_done": "Gotowe! Okno zaraz się zamknie.",
        "term_failed": "Coś poszło nie tak – sprawdź komunikaty powyżej. Enter zamyka okno.",
        "no_terminal": "Nie udało się otworzyć terminala.",
    },
    "de": {
        "close": "Schließen", "cancel": "Abbrechen", "apply": "Anwenden", "ok": "OK",
        "live_only_installed": "Das funktioniert, sobald OrkaLinux installiert ist. Im Live-System bleibt nach einem Neustart nichts erhalten.",
        "term_done": "Fertig! Das Fenster schließt sich gleich.",
        "term_failed": "Etwas ist schiefgelaufen - sieh dir die Meldungen oben an. Enter schließt das Fenster.",
        "no_terminal": "Das Terminal konnte nicht geöffnet werden.",
    },
    "fr": {
        "close": "Fermer", "cancel": "Annuler", "apply": "Appliquer", "ok": "OK",
        "live_only_installed": "Cela fonctionne une fois OrkaLinux installé. Dans le système live, rien n'est gardé après un redémarrage.",
        "term_done": "Terminé ! La fenêtre va se fermer.",
        "term_failed": "Un problème est survenu - regarde les messages ci-dessus. Entrée ferme la fenêtre.",
        "no_terminal": "Impossible d'ouvrir le terminal.",
    },
}


class Texts:

    def __init__(self, table, lang=None):
        self.lang = lang or system_lang()
        self.table = table

    def __getitem__(self, key):
        for lang in (self.lang, "en"):
            for source in (self.table.get(lang, {}), COMMON.get(lang, {})):
                if key in source:
                    return source[key]
        return key


CSS = """
window.orka, window.orka > box { background-color: #070b26; }

.hero-title { color: #ffffff; font-size: 26px; font-weight: 800; }
.hero-sub { color: rgba(255, 255, 255, 0.70); font-size: 12px; }

/* Zakładki pod nagłówkiem – w stylu kart z OrkaLinux Hello */
.tabs { background-color: #070b26; }
button.tab {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 7px 16px;
    box-shadow: none;
    text-shadow: none;
    -gtk-icon-shadow: none;
    transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
button.tab label { color: rgba(255, 255, 255, 0.80); font-weight: bold; }
button.tab image { color: rgba(255, 255, 255, 0.80); }
button.tab:hover { background-color: rgba(90, 110, 255, 0.18); border-color: rgba(140, 155, 255, 0.60); }
button.tab:checked {
    background-image: linear-gradient(90deg, #2b3bff, #6a2bff);
    border-color: transparent;
    box-shadow: 0 4px 14px rgba(60, 70, 255, 0.35);
}
button.tab:checked label, button.tab:checked image { color: #ffffff; }

.page-title { color: #ffffff; font-size: 18px; font-weight: 800; }
.page-sub { color: rgba(255, 255, 255, 0.60); font-size: 12px; }
.section { color: #8f9cff; font-weight: bold; font-size: 12px; }
.text { color: #d7dcff; }
.dim { color: rgba(255, 255, 255, 0.55); font-size: 11px; }
.big { color: #ffffff; font-size: 15px; font-weight: bold; }
.ok { color: #3ddc97; font-weight: bold; }
.warn { color: #ffc857; font-weight: bold; }

/* Karty */
.card {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 16px;
    transition: all 220ms ease-out;
}
button.tile {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.045);
    border: 2px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 10px;
    box-shadow: none;
    text-shadow: none;
    -gtk-icon-shadow: none;
    transition: all 180ms ease-out;
}
button.tile:hover { background-color: rgba(79, 88, 240, 0.14); border-color: rgba(140, 155, 255, 0.45); }
button.tile.selected { background-color: rgba(79, 88, 240, 0.22); border-color: #6c78ff; }
button.tile:disabled { opacity: 0.55; }
button.tile label { color: #ffffff; }
.tile-name { color: #ffffff; font-weight: bold; }
.tile-desc { color: rgba(255, 255, 255, 0.55); font-size: 11px; }
.badge { background-color: #4f58f0; color: #ffffff; border-radius: 10px; padding: 1px 8px; font-size: 10px; font-weight: bold; }
.badge-ok { background-color: rgba(61, 220, 151, 0.18); color: #3ddc97; border-radius: 10px; padding: 1px 8px; font-size: 10px; font-weight: bold; }

/* Przyciski */
button.primary {
    background-image: linear-gradient(90deg, #2b3bff, #6a2bff);
    border: none;
    border-radius: 10px;
    padding: 7px 20px;
    text-shadow: none;
    box-shadow: none;
}
button.primary label { color: #ffffff; font-weight: bold; }
button.primary:hover { background-image: linear-gradient(90deg, #4050ff, #7d45ff); }
button.primary:disabled { background-image: none; background-color: rgba(255, 255, 255, 0.08); }
button.primary:disabled label { color: rgba(255, 255, 255, 0.35); }
button.ghost {
    background-image: none;
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 7px 18px;
    text-shadow: none;
    box-shadow: none;
}
button.ghost label { color: #ffffff; }
button.ghost:hover { background-color: rgba(255, 255, 255, 0.16); }
button.danger {
    background-image: none;
    background-color: rgba(255, 92, 122, 0.12);
    border: 1px solid rgba(255, 92, 122, 0.35);
    border-radius: 10px;
    padding: 7px 18px;
    text-shadow: none;
    box-shadow: none;
}
button.danger label { color: #ff8098; }
button.danger:hover { background-color: rgba(255, 92, 122, 0.22); }

switch { border-radius: 14px; background-image: none; background-color: rgba(255, 255, 255, 0.15); border: none; }
switch:checked { background-color: #4f58f0; }
switch slider { border-radius: 14px; background-image: none; background-color: #ffffff; border: none; box-shadow: none; }

checkbutton label { color: #e3e7ff; }
scale trough { background-color: rgba(255, 255, 255, 0.12); border-radius: 4px; min-height: 6px; }
scale highlight { background-color: #4f58f0; border-radius: 4px; }
scale slider { background-color: #ffffff; border-radius: 10px; min-width: 18px; min-height: 18px; }
scale value, scale marks label { color: rgba(255, 255, 255, 0.6); }
levelbar trough { background-color: rgba(255, 255, 255, 0.10); border-radius: 6px; min-height: 10px; }
levelbar block.filled { background-color: #4f58f0; border-radius: 6px; }

entry { background-color: rgba(255, 255, 255, 0.06); color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 6px 8px; }
scrolledwindow, viewport, list, flowbox, flowboxchild { background-color: transparent; }
list row { background-color: transparent; }

.footer { background-color: #070a1a; border-top: 1px solid rgba(255, 255, 255, 0.07); }

.scrim { background-color: rgba(3, 5, 20, 0.62); }
.sheet {
    background-color: #0f1438;
    border: 1px solid rgba(140, 155, 255, 0.30);
    border-radius: 18px;
    padding: 22px 24px 18px 24px;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.55);
}
.sheet-title { color: #ffffff; font-size: 16px; font-weight: bold; }
.sheet-text { color: rgba(225, 230, 255, 0.80); }
.sheet-icon { color: #8a93ff; }
.sheet-error .sheet-icon { color: #ff8098; }
.sheet-details, .sheet-details label { color: rgba(255, 255, 255, 0.55); }
.mono { font-family: monospace; font-size: 11px; color: rgba(225, 230, 255, 0.75); }

dialog.orka, dialog.orka box, dialog.orka .dialog-action-area { background-color: #0b1033; }
dialog.orka label { color: #e3e7ff; }
messagedialog.orka, messagedialog.orka box { background-color: #0b1033; }
messagedialog.orka label { color: #e3e7ff; }
"""


LIGHT_CSS = """
window.orka, window.orka > box, .tabs { background-color: #f3f5fc; }
button.tab { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.12); }
button.tab label, button.tab image { color: rgba(22, 26, 54, 0.80); }
button.tab:hover { background-color: #eef0ff; border-color: #8a93ff; }
button.tab:checked { border-color: transparent; }
button.tab:checked label, button.tab:checked image { color: #ffffff; }

.page-title, .big { color: #161a36; }
.page-sub { color: rgba(22, 26, 54, 0.62); }
.section { color: #3b46d6; }
.text { color: #252a4a; }
.dim { color: rgba(22, 26, 54, 0.58); }
.ok { color: #138a5a; }
.warn { color: #b7791f; }

.card { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.12); }
button.tile { background-color: #ffffff; border-color: rgba(30, 40, 120, 0.10); }
button.tile:hover { background-color: #eef0ff; border-color: rgba(108, 120, 255, 0.60); }
button.tile.selected { background-color: rgba(79, 88, 240, 0.12); border-color: #6c78ff; }
button.tile label, .tile-name { color: #161a36; }
.tile-desc { color: rgba(22, 26, 54, 0.58); }
.badge-ok { background-color: rgba(19, 138, 90, 0.12); color: #138a5a; }

button.primary:disabled { background-color: rgba(20, 30, 90, 0.10); }
button.primary:disabled label { color: rgba(22, 26, 54, 0.40); }
button.ghost { background-color: rgba(30, 40, 120, 0.06); border-color: rgba(30, 40, 120, 0.14); }
button.ghost label, button.ghost image { color: #161a36; }
button.ghost:hover { background-color: rgba(30, 40, 120, 0.12); }
button.danger label { color: #d0324f; }

switch { background-color: rgba(20, 30, 90, 0.18); }
switch:checked { background-color: #4f58f0; }
checkbutton label { color: #252a4a; }
scale trough { background-color: rgba(20, 30, 90, 0.12); }
scale value, scale marks label { color: rgba(22, 26, 54, 0.60); }
levelbar trough { background-color: rgba(20, 30, 90, 0.10); }
entry { background-color: #ffffff; color: #161a36; border-color: rgba(30, 40, 120, 0.20); }

.footer { background-color: #e8ebf8; border-top-color: rgba(20, 30, 90, 0.10); }

.scrim { background-color: rgba(10, 15, 50, 0.35); }
.sheet { background-color: #ffffff; border-color: rgba(79, 88, 240, 0.30); box-shadow: 0 18px 50px rgba(10, 15, 60, 0.25); }
.sheet-title { color: #161a36; }
.sheet-text { color: rgba(22, 26, 54, 0.80); }
.sheet-icon { color: #4f58f0; }
.sheet-error .sheet-icon { color: #d0324f; }
.sheet-details, .sheet-details label { color: rgba(22, 26, 54, 0.55); }
.mono { color: rgba(22, 26, 54, 0.80); }
"""

_light_provider = None


def set_light(on):
    global _light_provider
    screen = Gdk.Screen.get_default()
    if on and _light_provider is None:
        _light_provider = Gtk.CssProvider()
        _light_provider.load_from_data(LIGHT_CSS.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_screen(screen, _light_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)
    elif not on and _light_provider is not None:
        Gtk.StyleContext.remove_provider_for_screen(screen, _light_provider)
        _light_provider = None


_css_loaded = False


def load_css(extra=""):
    global _css_loaded
    if _css_loaded:
        return
    provider = Gtk.CssProvider()
    provider.load_from_data((CSS + extra).encode("utf-8"))
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
    _css_loaded = True
    set_light(not is_dark_mode())


WAVES = [
    (10.0, 150.0, 0.45, 0.56, (0.055, 0.070, 0.420), 0.80),
    (13.0, 220.0, -0.30, 0.70, (0.115, 0.086, 0.660), 0.85),
    (8.0, 105.0, 0.70, 0.84, (0.205, 0.122, 0.790), 0.92),
]


class Waves(Gtk.DrawingArea):

    def __init__(self, tint=(0.10, 0.16, 0.95)):
        super().__init__()
        self.t = 0.0
        self.tint = tint
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


def save_lang(code):
    try:
        os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
        with open(LANG_FILE, "w") as f:
            f.write(code + "\n")
    except OSError:
        pass


def lang_combo():
    combo = Gtk.ComboBoxText()
    for code, name in LANG_NAMES.items():
        combo.append(code, name)
    combo.set_active_id(system_lang())
    combo.set_valign(Gtk.Align.START)

    def changed(c):
        code = c.get_active_id()
        if code and code != system_lang():
            save_lang(code)
            os.execv(sys.executable, [sys.executable] + sys.argv)
    combo.connect("changed", changed)
    return combo


def hero(title, subtitle, icon_name, height=170, extra=None):
    overlay = Gtk.Overlay()
    waves = Waves()
    waves.set_size_request(-1, height)
    overlay.add(waves)
    row = Gtk.Box(spacing=16)
    row.set_margin_start(32)
    row.set_margin_end(24)
    row.set_margin_top(18)
    row.set_margin_bottom(30)
    icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
    icon.set_pixel_size(88)
    row.pack_start(icon, False, False, 0)
    texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    texts.set_valign(Gtk.Align.CENTER)
    t = Gtk.Label(label=title, xalign=0)
    t.get_style_context().add_class("hero-title")
    s = Gtk.Label(label=subtitle, xalign=0)
    s.get_style_context().add_class("hero-sub")
    texts.pack_start(t, False, False, 0)
    texts.pack_start(s, False, False, 0)
    row.pack_start(texts, True, True, 0)
    if extra:
        row.pack_end(extra, False, False, 0)
    overlay.add_overlay(row)
    return overlay


def label(text, cls=None, wrap=False, xalign=0.0, selectable=False):
    lab = Gtk.Label(label=text, xalign=xalign)
    if wrap:
        lab.set_line_wrap(True)
        lab.set_max_width_chars(70)
    if selectable:
        lab.set_selectable(True)
    if cls:
        for c in cls.split():
            lab.get_style_context().add_class(c)
    return lab


def button(text, cls="ghost", callback=None, *args):
    btn = Gtk.Button(label=text)
    btn.get_style_context().add_class(cls)
    if callback:
        btn.connect("clicked", lambda *_: callback(*args))
    return btn


def card(child, margin=0):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box.get_style_context().add_class("card")
    box.pack_start(child, True, True, 0)
    if margin:
        box.set_margin_bottom(margin)
    return box


class PagedWindow(Gtk.Window):

    def __init__(self, app_id, title, subtitle, icon_name, width=980, height=680):
        GLib.set_prgname(app_id)
        super().__init__()
        load_css()
        self.set_title(title)
        self.set_icon_name(icon_name)
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.get_style_context().add_class("orka")
        self.connect("destroy", Gtk.main_quit)

        self.overlay = Gtk.Overlay()
        self.add(self.overlay)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.overlay.add(root)
        self._sheet_loop = None
        self.connect("key-press-event", self._on_key)
        self.connect("destroy", lambda *_: self._sheet_loop.quit() if self._sheet_loop else None)
        root.pack_start(hero(title, subtitle, icon_name, extra=lang_combo() if IS_LIVE else None), False, False, 0)

        self.tabs = Gtk.Box(spacing=8)
        self.tabs.get_style_context().add_class("tabs")
        self.tabs.set_margin_top(16)
        self.tabs.set_margin_start(28)
        self.tabs.set_margin_end(28)
        root.pack_start(self.tabs, False, False, 0)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(220)
        self.stack.set_margin_top(10)
        root.pack_start(self.stack, True, True, 0)
        self._pages = {}
        self._switching = False

    def add_page(self, name, title, icon_name, widget, subtitle=None):
        tab = Gtk.ToggleButton()
        tab.get_style_context().add_class("tab")
        box = Gtk.Box(spacing=8)
        img = Gtk.Image.new_from_icon_name(first_icon([icon_name + "-symbolic", icon_name]), Gtk.IconSize.SMALL_TOOLBAR)
        box.pack_start(img, False, False, 0)
        box.pack_start(Gtk.Label(label=title), False, False, 0)
        tab.add(box)
        tab.connect("toggled", self._on_tab, name)
        self.tabs.pack_start(tab, False, False, 0)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_top(18)
        page.set_margin_bottom(24)
        page.set_margin_start(28)
        page.set_margin_end(28)
        if subtitle:
            page.pack_start(label(subtitle, "page-sub", wrap=True), False, False, 0)
        page.pack_start(widget, True, True, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(page)
        self.stack.add_named(scroll, name)
        self._pages[name] = tab
        if len(self._pages) == 1:
            tab.set_active(True)

    def show_page(self, name):
        if name in self._pages:
            self._pages[name].set_active(True)

    def _on_tab(self, tab, name):
        if self._switching:
            return
        self._switching = True
        if tab.get_active():
            for other_name, other in self._pages.items():
                if other_name != name:
                    other.set_active(False)
            self.stack.set_visible_child_name(name)
        else:
            tab.set_active(True)
        self._switching = False


    def sheet(self, title, text=None, buttons=(), entry_hint=None, kind="info", details=None, entry_text=None):
        scrim = Gtk.EventBox()
        scrim.get_style_context().add_class("scrim")
        card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card_box.get_style_context().add_class("sheet")
        card_box.get_style_context().add_class("sheet-" + kind)
        card_box.set_halign(Gtk.Align.CENTER)
        card_box.set_valign(Gtk.Align.CENTER)
        card_box.set_size_request(440, -1)
        scrim.add(card_box)

        head = Gtk.Box(spacing=12)
        icon = {"info": "dialog-information", "question": "dialog-question",
                "error": "dialog-error", "ok": "emblem-success"}.get(kind, "dialog-information")
        img = Gtk.Image.new_from_icon_name(first_icon([icon + "-symbolic", icon]), Gtk.IconSize.DND)
        img.set_valign(Gtk.Align.START)
        img.get_style_context().add_class("sheet-icon")
        head.pack_start(img, False, False, 0)
        lab = label(title, "sheet-title", wrap=True)
        lab.set_max_width_chars(40)
        head.pack_start(lab, True, True, 0)
        card_box.pack_start(head, False, False, 0)
        if text:
            t = label(text, "sheet-text", wrap=True)
            t.set_max_width_chars(52)
            card_box.pack_start(t, False, False, 0)
        if details:
            exp = Gtk.Expander(label="...")
            exp.get_style_context().add_class("sheet-details")
            d = label(details, "mono", wrap=True, selectable=True)
            d.set_max_width_chars(60)
            exp.add(d)
            card_box.pack_start(exp, False, False, 0)
        entry = None
        if entry_hint is not None:
            entry = Gtk.Entry()
            entry.set_placeholder_text(entry_hint)
            if entry_text:
                entry.set_text(entry_text)
            entry.set_activates_default(True)
            card_box.pack_start(entry, False, False, 4)

        result = {"value": None}
        row = Gtk.Box(spacing=8)
        row.set_halign(Gtk.Align.END)
        row.set_margin_top(6)
        last = None
        for text_, cls, value in buttons:
            b = button(text_, cls, lambda v=value: self._close_sheet(result, v))
            row.pack_start(b, False, False, 0)
            last = b
        card_box.pack_start(row, False, False, 0)
        if entry is not None and last is not None:
            entry.connect("activate", lambda *_: last.clicked())

        self.overlay.add_overlay(scrim)
        scrim.show_all()
        (entry or last or scrim).grab_focus()
        self._sheet_result = result
        self._sheet_cancel = buttons[0][2] if buttons else None
        self._sheet_loop = GLib.MainLoop()
        self._sheet_loop.run()
        self._sheet_loop = None
        text_value = entry.get_text() if entry is not None else None
        if scrim.get_parent() is not None:
            self.overlay.remove(scrim)
        scrim.destroy()
        return result["value"], text_value

    def _close_sheet(self, result, value):
        result["value"] = value
        if self._sheet_loop is not None:
            self._sheet_loop.quit()

    def _on_key(self, widget, event):
        if self._sheet_loop is not None and event.keyval == Gdk.KEY_Escape:
            self._close_sheet(self._sheet_result, self._sheet_cancel)
            return True
        return False

    def message(self, text, secondary=None, kind=Gtk.MessageType.INFO, details=None):
        k = "error" if kind == Gtk.MessageType.ERROR else "info"
        self.sheet(text, secondary, [("OK", "primary", True)], kind=k, details=details)

    def confirm(self, text, secondary, yes, no, danger=False):
        value, _ = self.sheet(text, secondary, [(no, "ghost", False), (yes, "danger" if danger else "primary", True)],
                              kind="question")
        return bool(value)

    def ask_text(self, title, hint, ok, cancel, text=None):
        value, text = self.sheet(title, None, [(cancel, "ghost", False), (ok, "primary", True)], entry_hint=hint,
                                 kind="question", entry_text=text)
        return text if value else None


def first_icon(names):
    theme = Gtk.IconTheme.get_default()
    for name in names:
        if theme.has_icon(name):
            return name
    return names[-1]


def run_in_terminal(parent, args, texts, on_exit=None):
    """Długie operacje idą w terminalu kitty – widać postęp i ewentualny błąd.
    Po sukcesie okno zamyka się samo, po błędzie czeka na Enter.
    on_exit: wywoływane (w wątku GTK), gdy terminal się zamknie."""
    command = shlex.join(args) if isinstance(args, (list, tuple)) else args
    done = shlex.quote(texts["term_done"])
    failed = shlex.quote(texts["term_failed"])
    script = f"if {command}; then echo; echo {done}; sleep 3; else echo; echo {failed}; read -r _; fi"
    for term in (["kitty", "sh", "-c", script],
                 ["konsole", "-e", "sh", "-c", script]):
        if shutil.which(term[0]):
            proc = subprocess.Popen(term)
            if on_exit is not None:
                threading.Thread(target=lambda: (proc.wait(), GLib.idle_add(on_exit)), daemon=True).start()
            return True
    if parent is not None:
        parent.message(texts["no_terminal"], kind=Gtk.MessageType.ERROR)
    return False


def output(args, timeout=20):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def package_installed(name):
    out = output(["dpkg-query", "-W", "-f=${Status}", name], 10)
    return out.strip().endswith("installed") and "not-installed" not in out


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


LOOK_DARK = "org.orkalinux.desktop"
LOOK_LIGHT = "org.orkalinux.light.desktop"


def apply_dark_mode(dark):
    try:
        subprocess.Popen(["plasma-apply-lookandfeel", "-a", LOOK_DARK if dark else LOOK_LIGHT])
    except OSError:
        return False
    set_gtk_dark(dark)
    set_light(not dark)
    return True


def kread(file, groups, key, default=""):
    out = output(["kreadconfig6", "--file", file] + sum((["--group", g] for g in groups), [])
                 + ["--key", key, "--default", str(default)], 10)
    return out.strip() if out else str(default)


def kwrite(file, groups, key, value):
    args = ["kwriteconfig6", "--notify", "--file", file] + sum((["--group", g] for g in groups), [])
    if isinstance(value, bool):
        args += ["--type", "bool"]
        value = "true" if value else "false"
    try:
        subprocess.run(args + ["--key", key, str(value)], timeout=10)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def dbus_call(bus_name, path, interface, method, params=None, timeout=30000):
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        return bus.call_sync(bus_name, path, interface, method, params, None,
                             Gio.DBusCallFlags.NONE, timeout, None)
    except GLib.Error:
        return None


def plasma_script(js):
    return dbus_call("org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell",
                     "evaluateScript", GLib.Variant("(s)", (js,))) is not None


def kwin_reconfigure():
    return dbus_call("org.kde.KWin", "/KWin", "org.kde.KWin", "reconfigure") is not None


def kwin_effect(name, on):
    method = "loadEffect" if on else "unloadEffect"
    return dbus_call("org.kde.KWin", "/Effects", "org.kde.kwin.Effects", method,
                     GLib.Variant("(s)", (name,))) is not None


def human_size(num):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num < 1024 or unit == "TB":
            return f"{num:.0f} {unit}" if unit in ("B", "KB") else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"


def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path, onerror=lambda e: None):
        for name in files:
            try:
                total += os.lstat(os.path.join(root, name)).st_size
            except OSError:
                pass
    return total


def run():
    Gtk.main()
