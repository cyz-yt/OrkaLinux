#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import threading
import time

sys.path.insert(0, "/usr/share/orkalinux/lib")
import orka
from orka import Gtk, GLib

HELPER = "/usr/sbin/orka-kopia-helper"

TEXTS = {
    "en": {
        "c_title": "Creating a restore point", "c_keep": "You can keep using the computer. The first one can take several minutes, the next ones are much quicker.", "elapsed": "Time: {t}", "st_prep": "Getting the disk ready...", "st_size": "Checking how big the system is...", "st_copy": "Copying system files...", "st_save": "Saving the restore point...", "st_clean": "Removing old restore points...", "st_restore": "Restoring files...", "sched": "Automatic restore points", "sched_d": "Older ones are removed by themselves. Only the first point is a full copy, the next ones take just what changed.", "every_daily": "Every day", "every_weekly": "Every week", "every_monthly": "Every month", "every_boot": "Every time the computer starts", "keep": "Keep", "disk": "Disk", "disk_d": "Restore points are kept on {dev}, the same disk as the system.", "disk_free": "{free} free of {total}", "disk_points": "Restore points: {n}",
        "restore_reboot": "Restarting into OrkaLinux Recovery...", "restoring": "Restoring the system to {date}", "restore_keep": "Don't turn off the computer. This can take several minutes.", "restore_done": "Done! The computer restarts in a few seconds.",
        "title": "OrkaLinux Backup", "subtitle": "Restore points: go back in time when something breaks",
        "p_points": "Restore points", "p_settings": "Settings",
        "p_points_sub": "A restore point is a snapshot of the system (apps, settings, drivers). Your own files in the home folder are not part of it and never get removed.",
        "off_title": "Restore points are off", "off_text": "Turn them on and OrkaLinux will keep a few snapshots of the system on this disk.",
        "turn_on": "Turn on", "create": "Create restore point", "refresh": "Refresh",
        "loading": "Loading restore points...", "empty": "No restore points yet.",
        "restore": "Restore", "delete": "Delete",
        "desc_q": "Describe this restore point", "desc_hint": "e.g. Before installing drivers",
        "edit_desc": "Change description", "save": "Save", "first_point": "First restore point",
        "creating": "Creating a restore point... The first one can take several minutes.",
        "created": "Restore point created.", "failed": "It didn't work.", "failed_d": "Details are below and in /var/log/orka-kopia.log. Send them to me on Discord.", "denied": "No password - nothing was changed.",
        "restore_q": "Restore the system to {date}?",
        "restore_q2": "Apps, settings and drivers go back to how they were then. Your files stay. The computer restarts into OrkaLinux Recovery and restores the system there - save your work first.",
        "delete_q": "Delete the restore point from {date}?", "delete_q2": "This can't be undone.",
        "tag_O": "manual", "tag_D": "daily", "tag_W": "weekly", "tag_M": "monthly", "tag_B": "at boot", "tag_H": "hourly",
        "auto": "A restore point before updates", "auto_d": "Before installing or updating software (at most once a day).",
        "need_on": "Turn on restore points first.",
    },
    "pl": {
        "c_title": "Tworzę punkt przywracania", "c_keep": "Możesz dalej korzystać z komputera. Pierwszy może potrwać kilka minut, kolejne idą dużo szybciej.", "elapsed": "Czas: {t}", "st_prep": "Przygotowuję dysk...", "st_size": "Sprawdzam, ile zajmuje system...", "st_copy": "Kopiuję pliki systemu...", "st_save": "Zapisuję punkt przywracania...", "st_clean": "Usuwam stare punkty przywracania...", "st_restore": "Przywracam pliki...", "sched": "Automatyczne punkty przywracania", "sched_d": "Starsze znikają same. Tylko pierwszy punkt to pełna kopia, kolejne zajmują tyle, ile się zmieniło.", "every_daily": "Codziennie", "every_weekly": "Co tydzień", "every_monthly": "Co miesiąc", "every_boot": "Przy każdym uruchomieniu komputera", "keep": "Zostaw", "disk": "Dysk", "disk_d": "Punkty przywracania leżą na {dev}, na tym samym dysku co system.", "disk_free": "{free} wolne z {total}", "disk_points": "Punkty przywracania: {n}",
        "restore_reboot": "Uruchamiam ponownie do OrkaLinux Recovery...", "restoring": "Przywracam system do stanu z {date}", "restore_keep": "Nie wyłączaj komputera. To może potrwać kilka minut.", "restore_done": "Gotowe! Komputer zaraz się zrestartuje.",
        "title": "Kopia zapasowa OrkaLinux", "subtitle": "Punkty przywracania: cofnij system, gdy coś się zepsuje",
        "p_points": "Punkty przywracania", "p_settings": "Ustawienia",
        "p_points_sub": "Punkt przywracania to zdjęcie systemu (programy, ustawienia, sterowniki). Twoje pliki w katalogu domowym nie wchodzą do niego i nigdy nie są usuwane.",
        "off_title": "Punkty przywracania są wyłączone", "off_text": "Włącz je, a OrkaLinux będzie trzymać kilka kopii systemu na tym dysku.",
        "turn_on": "Włącz", "create": "Utwórz punkt przywracania", "refresh": "Odśwież",
        "loading": "Wczytuję punkty przywracania...", "empty": "Nie ma jeszcze żadnego punktu.",
        "restore": "Przywróć", "delete": "Usuń",
        "desc_q": "Opisz ten punkt przywracania", "desc_hint": "np. Przed instalacją sterowników",
        "edit_desc": "Zmień opis", "save": "Zapisz", "first_point": "Pierwszy punkt przywracania",
        "creating": "Tworzę punkt przywracania... Pierwszy może potrwać kilka minut.",
        "created": "Punkt przywracania utworzony.", "failed": "Nie udało się.", "failed_d": "Szczegóły są niżej i w /var/log/orka-kopia.log. Wyślij mi je na Discordzie.", "denied": "Bez hasła – nic nie zmieniono.",
        "restore_q": "Przywrócić system do stanu z {date}?",
        "restore_q2": "Programy, ustawienia i sterowniki wrócą do tamtego stanu. Twoje pliki zostają. Komputer uruchomi się ponownie w OrkaLinux Recovery i tam przywróci system – zapisz wcześniej swoją pracę.",
        "delete_q": "Usunąć punkt przywracania z {date}?", "delete_q2": "Tego nie da się cofnąć.",
        "tag_O": "ręczny", "tag_D": "codzienny", "tag_W": "cotygodniowy", "tag_M": "comiesięczny", "tag_B": "przy starcie", "tag_H": "co godzinę",
        "auto": "Punkt przywracania przed aktualizacjami", "auto_d": "Przed instalacją albo aktualizacją programów (najwyżej raz dziennie).",
        "need_on": "Najpierw włącz punkty przywracania.",
    },
    "de": {
        "c_title": "Erstelle Wiederherstellungspunkt", "c_keep": "Du kannst den Computer weiter benutzen. Der erste kann einige Minuten dauern, die nächsten gehen viel schneller.", "elapsed": "Zeit: {t}", "st_prep": "Bereite die Festplatte vor...", "st_size": "Prüfe, wie groß das System ist...", "st_copy": "Kopiere Systemdateien...", "st_save": "Speichere den Wiederherstellungspunkt...", "st_clean": "Entferne alte Wiederherstellungspunkte...", "st_restore": "Stelle Dateien wieder her...", "sched": "Automatische Wiederherstellungspunkte", "sched_d": "Ältere verschwinden von selbst. Nur der erste Punkt ist eine volle Kopie, die nächsten belegen nur das, was sich geändert hat.", "every_daily": "Jeden Tag", "every_weekly": "Jede Woche", "every_monthly": "Jeden Monat", "every_boot": "Bei jedem Start des Computers", "keep": "Behalten", "disk": "Festplatte", "disk_d": "Wiederherstellungspunkte liegen auf {dev}, derselben Festplatte wie das System.", "disk_free": "{free} frei von {total}", "disk_points": "Wiederherstellungspunkte: {n}",
        "restore_reboot": "Starte neu in OrkaLinux Recovery...", "restoring": "Stelle das System auf den Stand vom {date} wieder her", "restore_keep": "Schalte den Computer nicht aus. Das kann einige Minuten dauern.", "restore_done": "Fertig! Der Computer startet gleich neu.",
        "title": "OrkaLinux Sicherung", "subtitle": "Wiederherstellungspunkte: zurück in der Zeit, wenn etwas kaputtgeht",
        "p_points": "Wiederherstellungspunkte", "p_settings": "Einstellungen",
        "p_points_sub": "Ein Wiederherstellungspunkt ist ein Abbild des Systems (Programme, Einstellungen, Treiber). Deine Dateien im Home-Ordner gehören nicht dazu und werden nie gelöscht.",
        "off_title": "Wiederherstellungspunkte sind aus", "off_text": "Schalte sie ein, dann behält OrkaLinux ein paar Systemabbilder auf dieser Festplatte.",
        "turn_on": "Einschalten", "create": "Wiederherstellungspunkt erstellen", "refresh": "Aktualisieren",
        "loading": "Lade Wiederherstellungspunkte...", "empty": "Noch keine Wiederherstellungspunkte.",
        "restore": "Wiederherstellen", "delete": "Löschen",
        "desc_q": "Beschreibe diesen Wiederherstellungspunkt", "desc_hint": "z. B. Vor der Treiberinstallation",
        "edit_desc": "Beschreibung ändern", "save": "Speichern", "first_point": "Erster Wiederherstellungspunkt",
        "creating": "Erstelle Wiederherstellungspunkt... Der erste kann einige Minuten dauern.",
        "created": "Wiederherstellungspunkt erstellt.", "failed": "Das hat nicht geklappt.", "failed_d": "Details stehen unten und in /var/log/orka-kopia.log. Schick sie mir auf Discord.", "denied": "Kein Passwort - nichts geändert.",
        "restore_q": "System auf den Stand vom {date} zurücksetzen?",
        "restore_q2": "Programme, Einstellungen und Treiber kehren zu diesem Stand zurück. Deine Dateien bleiben. Der Computer startet in OrkaLinux Recovery neu und stellt das System dort wieder her - speichere vorher deine Arbeit.",
        "delete_q": "Wiederherstellungspunkt vom {date} löschen?", "delete_q2": "Das lässt sich nicht rückgängig machen.",
        "tag_O": "manuell", "tag_D": "täglich", "tag_W": "wöchentlich", "tag_M": "monatlich", "tag_B": "beim Start", "tag_H": "stündlich",
        "auto": "Wiederherstellungspunkt vor Updates", "auto_d": "Vor dem Installieren oder Aktualisieren von Software (höchstens einmal am Tag).",
        "need_on": "Schalte zuerst die Wiederherstellungspunkte ein.",
    },
    "fr": {
        "c_title": "Création d'un point de restauration", "c_keep": "Tu peux continuer à utiliser l'ordinateur. Le premier peut prendre plusieurs minutes, les suivants vont bien plus vite.", "elapsed": "Temps : {t}", "st_prep": "Préparation du disque...", "st_size": "Calcul de la taille du système...", "st_copy": "Copie des fichiers système...", "st_save": "Enregistrement du point de restauration...", "st_clean": "Suppression des anciens points de restauration...", "st_restore": "Restauration des fichiers...", "sched": "Points de restauration automatiques", "sched_d": "Les plus anciens partent tout seuls. Seul le premier point est une copie complète, les suivants ne prennent que ce qui a changé.", "every_daily": "Chaque jour", "every_weekly": "Chaque semaine", "every_monthly": "Chaque mois", "every_boot": "À chaque démarrage de l'ordinateur", "keep": "Garder", "disk": "Disque", "disk_d": "Les points de restauration sont sur {dev}, le même disque que le système.", "disk_free": "{free} libres sur {total}", "disk_points": "Points de restauration : {n}",
        "restore_reboot": "Redémarrage dans OrkaLinux Recovery...", "restoring": "Restauration du système à l'état du {date}", "restore_keep": "N'éteins pas l'ordinateur. Cela peut prendre plusieurs minutes.", "restore_done": "Terminé ! L'ordinateur va redémarrer.",
        "title": "Sauvegarde OrkaLinux", "subtitle": "Points de restauration : revenir en arrière quand quelque chose casse",
        "p_points": "Points de restauration", "p_settings": "Réglages",
        "p_points_sub": "Un point de restauration est une image du système (applis, réglages, pilotes). Tes fichiers du dossier personnel n'en font pas partie et ne sont jamais supprimés.",
        "off_title": "Les points de restauration sont désactivés", "off_text": "Active-les et OrkaLinux gardera quelques images du système sur ce disque.",
        "turn_on": "Activer", "create": "Créer un point de restauration", "refresh": "Actualiser",
        "loading": "Chargement des points de restauration...", "empty": "Aucun point de restauration pour l'instant.",
        "restore": "Restaurer", "delete": "Supprimer",
        "desc_q": "Décris ce point de restauration", "desc_hint": "ex. Avant d'installer les pilotes",
        "edit_desc": "Modifier la description", "save": "Enregistrer", "first_point": "Premier point de restauration",
        "creating": "Création du point de restauration... Le premier peut prendre plusieurs minutes.",
        "created": "Point de restauration créé.", "failed": "Ça n'a pas marché.", "failed_d": "Les détails sont ci-dessous et dans /var/log/orka-kopia.log. Envoie-les-moi sur Discord.", "denied": "Pas de mot de passe - rien n'a changé.",
        "restore_q": "Restaurer le système au {date} ?",
        "restore_q2": "Applis, réglages et pilotes reviennent à cet état. Tes fichiers restent. L'ordinateur redémarre dans OrkaLinux Recovery et y restaure le système - enregistre ton travail avant.",
        "delete_q": "Supprimer le point de restauration du {date} ?", "delete_q2": "Impossible d'annuler.",
        "tag_O": "manuel", "tag_D": "quotidien", "tag_W": "hebdo", "tag_M": "mensuel", "tag_B": "au démarrage", "tag_H": "horaire",
        "auto": "Un point de restauration avant les mises à jour", "auto_d": "Avant d'installer ou de mettre à jour des logiciels (une fois par jour max).",
        "need_on": "Active d'abord les points de restauration.",
    },
}


def helper(*args):
    try:
        if args and args[0] == "list":
            res = subprocess.run(["pkexec", HELPER, *args], capture_output=True, text=True)
        else:
            res = subprocess.run(["pkexec", HELPER, *args], text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return res.returncode, res.stdout
    except OSError as e:
        return 1, str(e)


STEPS = [
    (re.compile(r"Mount|Backup Device|Device", re.I), "st_prep"),
    (re.compile(r"Estimat", re.I), "st_size"),
    (re.compile(r"Sync|rsync|Creating new snapshot|building file list", re.I), "st_copy"),
    (re.compile(r"control file|saved successfully|Tagged snapshot", re.I), "st_save"),
    (re.compile(r"Remov|Delet", re.I), "st_clean"),
    (re.compile(r"Restoring", re.I), "st_restore"),
]


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return ("%.0f %s" if unit in ("B", "KB") else "%.1f %s") % (n, unit)
        n /= 1024.0


def tail(text, lines=14):
    return "\n".join((text or "").strip().splitlines()[-lines:])


def nice_date(name):
    try:
        return time.strftime("%d.%m.%Y %H:%M", time.strptime(name, "%Y-%m-%d_%H-%M-%S"))
    except ValueError:
        return name


class OrkaKopia(orka.PagedWindow):
    def __init__(self):
        t = orka.Texts(TEXTS)
        super().__init__("orka-kopia", t["title"], t["subtitle"], "orka-kopia", 900, 640)
        self.t = t
        self.state = None
        self.restoring = False
        self.connect("delete-event", lambda *_: self.restoring)
        self.points = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.settings = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add_page("points", t["p_points"], "document-revert", self.points, t["p_points_sub"])
        self.add_page("settings", t["p_settings"], "configure", self.settings)
        self.show_all()
        if orka.IS_LIVE:
            self.fill(self.points, [orka.card(orka.label(t["live_only_installed"], "text", wrap=True))])
            self.fill(self.settings, [orka.card(orka.label(t["live_only_installed"], "text", wrap=True))])
        else:
            self.reload()

    @staticmethod
    def fill(box, widgets):
        for child in box.get_children():
            box.remove(child)
        for w in widgets:
            box.pack_start(w, False, False, 0)
        box.show_all()

    def busy(self, text):
        row = Gtk.Box(spacing=12)
        spinner = Gtk.Spinner()
        spinner.start()
        row.pack_start(spinner, False, False, 0)
        row.pack_start(orka.label(text, "text", wrap=True), True, True, 0)
        self.fill(self.points, [orka.card(row)])


    def reload(self):
        self.busy(self.t["loading"])
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        code, out = helper("list")
        try:
            state = json.loads(out) if code == 0 else None
        except ValueError:
            state = None
        GLib.idle_add(self.show_state, state, code)

    def show_state(self, state, code):
        self.state = state
        if state is None:
            text = self.t["denied"] if code in (126, 127) else self.t["failed"]
            retry = orka.button(self.t["refresh"], "ghost", self.reload)
            retry.set_halign(Gtk.Align.START)
            self.fill(self.points, [orka.card(orka.label(text, "warn", wrap=True)), retry])
            self.build_settings()
            return False

        if not state["configured"]:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            box.pack_start(orka.label(self.t["off_title"], "big"), False, False, 0)
            box.pack_start(orka.label(self.t["off_text"], "text", wrap=True), False, False, 0)
            on = orka.button(self.t["turn_on"], "primary", self.turn_on)
            on.set_halign(Gtk.Align.START)
            box.pack_start(on, False, False, 6)
            self.fill(self.points, [orka.card(box)])
            self.build_settings()
            return False

        widgets = []
        top = Gtk.Box(spacing=10)
        top.pack_start(orka.button(self.t["create"], "primary", self.create), False, False, 0)
        top.pack_start(orka.button(self.t["refresh"], "ghost", self.reload), False, False, 0)
        widgets.append(top)
        snaps = sorted(state["snapshots"], key=lambda s: s["name"], reverse=True)
        if not snaps:
            widgets.append(orka.card(orka.label(self.t["empty"], "dim")))
        for snap in snaps:
            widgets.append(self.snapshot_row(snap))
        self.fill(self.points, widgets)
        self.build_settings()
        return False

    def snapshot_row(self, snap):
        row = Gtk.Box(spacing=14)
        icon = Gtk.Image.new_from_icon_name("orka-kopia", Gtk.IconSize.DND)
        icon.set_pixel_size(36)
        row.pack_start(icon, False, False, 0)
        texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        title = Gtk.Box(spacing=8)
        title.pack_start(orka.label(nice_date(snap["name"]), "big"), False, False, 0)
        for tag in snap["tags"]:
            badge = orka.label(self.t["tag_" + tag], "badge")
            badge.set_valign(Gtk.Align.CENTER)
            title.pack_start(badge, False, False, 0)
        texts.pack_start(title, False, False, 0)
        if snap["comment"]:
            texts.pack_start(orka.label(snap["comment"], "dim"), False, False, 0)
        row.pack_start(texts, True, True, 0)
        restore = orka.button(self.t["restore"], "danger", self.restore, snap)
        restore.set_valign(Gtk.Align.CENTER)
        delete = orka.button(self.t["delete"], "ghost", self.delete, snap)
        delete.set_valign(Gtk.Align.CENTER)
        rename = Gtk.Button()
        rename.get_style_context().add_class("ghost")
        rename.add(Gtk.Image.new_from_icon_name(orka.first_icon(["document-edit-symbolic", "document-edit"]),
                                                Gtk.IconSize.BUTTON))
        rename.set_tooltip_text(self.t["edit_desc"])
        rename.set_valign(Gtk.Align.CENTER)
        rename.connect("clicked", lambda *_: self.edit_comment(snap))
        row.pack_end(delete, False, False, 0)
        row.pack_end(restore, False, False, 0)
        row.pack_end(rename, False, False, 0)
        return orka.card(row)


    def in_background(self, text, args, done_text=None):
        self.busy(text)

        def work():
            code, out = helper(*args)
            GLib.idle_add(self.after, code, done_text, out)
        threading.Thread(target=work, daemon=True).start()

    def after(self, code, done_text, out=""):
        if code in (126, 127):
            self.message(self.t["denied"])
        elif code != 0:
            self.message(self.t["failed"], self.t["failed_d"], kind=Gtk.MessageType.ERROR, details=tail(out))
        elif done_text:
            self.message(done_text)
        self.reload()
        return False

    def turn_on(self):
        def first():
            code, out = helper("setup")
            if code != 0:
                return code, out
            return None
        self.run_live(self.t["c_title"], self.t["c_keep"], ["create", self.t["first_point"]],
                      self._create_done, before=first)

    def create(self):
        comment = self.ask_text(self.t["desc_q"], self.t["desc_hint"], self.t["create"], self.t["cancel"])
        if comment is not None:
            self.run_live(self.t["c_title"], self.t["c_keep"], ["create", comment.strip() or self.t["title"]],
                          self._create_done)

    def _create_done(self, code, out):
        self.after(code, self.t["created"] if code == 0 else None, out)
        return False


    def run_live(self, title, keep, args, done, before=None):
        """Karta z paskiem: pasek chodzi w kółko, a jak Timeshift poda procenty,
        pokazuje procenty. Pod spodem to, co Timeshift właśnie robi, i czas."""
        self.restoring = True
        self.r_frac = None
        self.r_start = time.time()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.pack_start(orka.label(title, "big"), False, False, 0)
        self.r_bar = Gtk.ProgressBar()
        self.r_bar.set_show_text(True)
        self.r_bar.set_text("")
        self.r_bar.set_pulse_step(0.04)
        box.pack_start(self.r_bar, False, False, 4)
        self.r_status = orka.label(self.t["st_prep"], "text", wrap=True)
        box.pack_start(self.r_status, False, False, 0)
        self.r_time = orka.label(self.t["elapsed"].format(t="0:00"), "dim")
        box.pack_start(self.r_time, False, False, 0)
        box.pack_start(orka.label(keep, "dim", wrap=True), False, False, 0)
        self.fill(self.points, [orka.card(box)])
        self.tabs.set_sensitive(False)
        GLib.timeout_add(100, self._pulse)
        threading.Thread(target=self._live, args=(args, done, before), daemon=True).start()

    def _pulse(self):
        if not self.restoring:
            return False
        if self.r_frac is None:
            self.r_bar.pulse()
        el = int(time.time() - self.r_start)
        self.r_time.set_text(self.t["elapsed"].format(t="%d:%02d" % (el // 60, el % 60)))
        return True

    def _status(self, line):
        for rx, key in STEPS:
            if rx.search(line):
                self.r_status.set_text(self.t[key])
                return False
        if not line.startswith("*") and len(line) > 3:
            self.r_status.set_text(line[:120])
        return False

    def _live(self, args, done, before):
        if before:
            res = before()
            if res:
                GLib.idle_add(self._live_done, done, res[0], res[1])
                return
        out = []
        try:
            proc = subprocess.Popen(["pkexec", HELPER, *args],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError as e:
            GLib.idle_add(self._live_done, done, 1, str(e))
            return
        buf = ""
        while True:
            chunk = os.read(proc.stdout.fileno(), 4096)
            if not chunk:
                break
            buf += chunk.decode("utf-8", "replace")
            parts = re.split(r"[\r\n]", buf)
            buf = parts.pop()
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                out.append(part)
                if part == "REBOOT":
                    GLib.idle_add(self.r_status.set_text, self.t["restore_reboot"])
                    continue
                m = re.search(r"(\d{1,3}(?:[.,]\d+)?)\s*%", part)
                pct = float(m.group(1).replace(",", ".")) if m else 0.0
                if pct > 0:
                    GLib.idle_add(self._progress, pct)
                elif not m:
                    GLib.idle_add(self._status, part)
        code = proc.wait()
        GLib.idle_add(self._live_done, done, code, "\n".join(out + [buf]))

    def _progress(self, pct):
        pct = max(0.0, min(pct, 100.0))
        self.r_frac = pct / 100
        self.r_bar.set_fraction(self.r_frac)
        self.r_bar.set_text("%d%%" % pct)
        return False

    def _live_done(self, done, code, out):
        self.restoring = False
        self.tabs.set_sensitive(True)
        return done(code, out)

    def edit_comment(self, snap):
        text = self.ask_text(self.t["edit_desc"], self.t["desc_hint"], self.t["save"], self.t["cancel"],
                             text=snap["comment"])
        if text is not None and text.strip() != snap["comment"]:
            self.in_background(self.t["loading"], ["comment", snap["name"], text.strip()])

    def restore(self, snap):
        date = nice_date(snap["name"])
        if not self.confirm(self.t["restore_q"].format(date=date), self.t["restore_q2"],
                            self.t["restore"], self.t["cancel"], danger=True):
            return
        self.run_live(self.t["restoring"].format(date=date), self.t["restore_keep"],
                      ["restore-boot", snap["name"]], self._restore_done)

    def _restore_done(self, code, out):
        if code == 0:
            self.r_bar.set_fraction(1.0)
            self.r_bar.set_text("100%")
            self.r_status.set_text(self.t["restore_done"])
            GLib.timeout_add_seconds(4, lambda: subprocess.Popen(["systemctl", "reboot"]) and False)
            return False
        self.after(code, None, out)
        return False

    def delete(self, snap):
        date = nice_date(snap["name"])
        if self.confirm(self.t["delete_q"].format(date=date), self.t["delete_q2"], self.t["delete"], self.t["cancel"],
                        danger=True):
            self.in_background(self.t["loading"], ["delete", snap["name"]])


    def build_settings(self):
        state = self.state or {}
        configured = bool(state.get("configured"))
        sched = state.get("schedule") or {}
        widgets = []
        self.set_lock = True

        def text_box(title, desc):
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            texts.pack_start(orka.label(title, "big"), False, False, 0)
            if desc:
                texts.pack_start(orka.label(desc, "dim", wrap=True), False, False, 0)
            return texts

        def switch_for(active, cb, *args):
            sw = Gtk.Switch()
            sw.set_valign(Gtk.Align.CENTER)
            sw.set_active(bool(active))
            sw.set_sensitive(configured)
            sw.connect("notify::active", cb, *args)
            return sw

        widgets.append(orka.label(self.t["sched"], "section"))
        widgets.append(orka.label(self.t["sched_d"], "dim", wrap=True))
        for kind in ("daily", "weekly", "monthly", "boot"):
            info = sched.get(kind) or {"on": kind == "daily" and state.get("daily"), "count": 5}
            row = Gtk.Box(spacing=14)
            row.pack_start(text_box(self.t["every_" + kind], None), True, True, 0)
            keep = Gtk.Box(spacing=8)
            keep.pack_start(orka.label(self.t["keep"], "dim"), False, False, 0)
            keep.pack_start(self.stepper(int(info.get("count") or 5), configured, kind), False, False, 0)
            keep.set_valign(Gtk.Align.CENTER)
            row.pack_end(switch_for(info.get("on"), self.on_schedule, kind), False, False, 0)
            row.pack_end(keep, False, False, 0)
            widgets.append(orka.card(row))

        row = Gtk.Box(spacing=14)
        row.pack_start(text_box(self.t["auto"], self.t["auto_d"]), True, True, 0)
        row.pack_end(switch_for(state.get("auto"), self.on_switch, "auto"), False, False, 0)
        widgets.append(orka.card(row))

        disk = state.get("disk") or {}
        if disk.get("total"):
            widgets.append(orka.label(self.t["disk"], "section"))
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.pack_start(orka.label(self.t["disk_free"].format(free=human(disk["free"]),
                                                                total=human(disk["total"])), "big"), False, False, 0)
            bar = Gtk.LevelBar()
            bar.set_value(1 - disk["free"] / float(disk["total"]))
            box.pack_start(bar, False, False, 2)
            box.pack_start(orka.label(self.t["disk_d"].format(dev=disk.get("device") or "/"), "dim", wrap=True),
                           False, False, 0)
            box.pack_start(orka.label(self.t["disk_points"].format(n=len(state.get("snapshots") or [])), "dim"),
                           False, False, 0)
            widgets.append(orka.card(box))

        if not configured:
            widgets.append(orka.label(self.t["need_on"], "dim"))
        self.fill(self.settings, widgets)
        self.set_lock = False

    def _set(self, *args):
        def work():
            code, _ = helper(*args)
            if code != 0:
                GLib.idle_add(self.after, code, None)
        threading.Thread(target=work, daemon=True).start()

    def on_schedule(self, switch, _param, kind):
        if not self.set_lock:
            self._set("schedule", kind, "on" if switch.get_active() else "off")

    def stepper(self, value, enabled, kind):
        """Liczba z przyciskami - i + w stylu reszty okna (Gtk.SpinButton
        z motywem wyglądał jak doklejony)."""
        box = Gtk.Box(spacing=6)
        box.set_valign(Gtk.Align.CENTER)
        num = orka.label(str(value), "big")
        num.set_width_chars(2)
        num.set_xalign(0.5)
        minus = orka.button("−", "ghost")
        plus = orka.button("+", "ghost")
        for b in (minus, plus):
            b.set_size_request(34, 34)
            b.set_valign(Gtk.Align.CENTER)
            b.set_sensitive(enabled)

        def change(delta):
            n = max(1, min(20, int(num.get_text()) + delta))
            num.set_text(str(n))
            minus.set_sensitive(enabled and n > 1)
            plus.set_sensitive(enabled and n < 20)
            if delta:
                self.on_keep(n, kind)
        minus.connect("clicked", lambda *_: change(-1))
        plus.connect("clicked", lambda *_: change(1))
        change(0)
        box.pack_start(minus, False, False, 0)
        box.pack_start(num, False, False, 0)
        box.pack_start(plus, False, False, 0)
        return box

    def on_keep(self, value, kind):
        if self.set_lock:
            return
        timers = self.__dict__.setdefault("keep_timers", {})
        if timers.get(kind):
            GLib.source_remove(timers[kind])

        def save():
            timers[kind] = None
            self._set("keep", kind, str(value))
            return False
        timers[kind] = GLib.timeout_add(700, save)

    def on_switch(self, switch, _param, key):
        if not self.set_lock:
            self._set(key, "on" if switch.get_active() else "off")


if __name__ == "__main__":
    OrkaKopia()
    orka.run()
