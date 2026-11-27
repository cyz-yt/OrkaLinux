import io.calamares.ui 1.0
import io.calamares.core 1.0

import QtQuick 2.3
import QtQuick.Layouts 1.3

Rectangle {
    id: navigationBar
    color: "#0f1120"
    height: 64
    implicitHeight: 64

    readonly property color accent: Branding.styleString(Branding.SidebarBackgroundCurrent)
    readonly property color strongText: "#fffffe"
    readonly property bool lastStep: ViewManager.currentStepIndex === ViewManager.rowCount() - 1
    property int countdown: -1
    readonly property bool atSummary: ViewManager.currentStepIndex === ViewManager.rowCount() - 3
    readonly property bool installing: ViewManager.currentStepIndex === ViewManager.rowCount() - 2

    property string jobName: ""
    property int jobIndex: 0
    property int jobCount: 0
    Timer {
        interval: 1500
        repeat: true
        triggeredOnStart: true
        running: navigationBar.installing
        onTriggered: navigationBar.readJob()
    }
    function readJob() {
        var x = new XMLHttpRequest();
        x.onreadystatechange = function() {
            if (x.readyState !== XMLHttpRequest.DONE)
                return;
            var t = x.responseText || "";
            var i = t.lastIndexOf("Starting ");
            while (i >= 0) {
                var line = t.substring(i, t.indexOf("\n", i) < 0 ? t.length : t.indexOf("\n", i));
                var m = /^Starting (?:job|EMERGENCY JOB)\s+"?(.*?)"?\s*\(\s*(\d+)\s*\/\s*(\d+)\s*\)/.exec(line);
                if (m) {
                    navigationBar.jobName = m[1].replace(/\.+$/, "");
                    navigationBar.jobIndex = parseInt(m[2]);
                    navigationBar.jobCount = parseInt(m[3]);
                    return;
                }
                i = i > 0 ? t.lastIndexOf("Starting ", i - 1) : -1;
            }
        };
        x.open("GET", "file:///root/.cache/calamares/session.log");
        x.send();
    }
    Connections {
        target: ViewManager
        function onCurrentStepIndexChanged() { navigationBar.cancelCountdown() }
    }
    readonly property string lang: {
        var b = ViewManager.backLabel.replace("&", "");
        var known = { "Wstecz": "pl", "Zurück": "de", "Précédent": "fr", "Atrás": "es",
                      "Indietro": "it", "Voltar": "pt", "Назад": "uk" };
        return known[b] || "en";
    }
    Timer {
        id: tick
        interval: 1000
        repeat: true
        onTriggered: {
            navigationBar.countdown--;
            if (navigationBar.countdown <= 0) {
                stop();
                navigationBar.countdown = -1;
                ViewManager.next();
            }
        }
    }
    function startOrNext() {
        if (atSummary) {
            countdown = 3;
            tick.start();
        } else {
            ViewManager.next();
        }
    }
    function cancelCountdown() {
        tick.stop();
        countdown = -1;
    }
    readonly property bool counting: countdown >= 0
    readonly property var texts: ({
        "pl": ["Uwaga! Zaraz zmiany trafią na dysk – dane z wybranych partycji znikną na zawsze. Start za %1…", "Anuluj", "Zakończ", "Instalacja trwa. Nie wyłączaj komputera – w tym czasie możesz poczytać, co jest w OrkaLinux.", "Krok %1 z %2: %3"],
        "de": ["Achtung! Gleich wird auf die Festplatte geschrieben – Daten auf den gewählten Partitionen sind dann weg. Start in %1…", "Abbrechen", "Fertig", "Die Installation läuft. Schalte den Computer nicht aus – inzwischen kannst du lesen, was in OrkaLinux steckt.", "Schritt %1 von %2: %3"],
        "fr": ["Attention ! Le disque va être modifié – les données des partitions choisies seront perdues. Début dans %1…", "Annuler", "Terminer", "L'installation est en cours. N'éteins pas l'ordinateur – en attendant, découvre ce qu'il y a dans OrkaLinux.", "Étape %1 sur %2 : %3"],
        "es": ["¡Atención! Los cambios se van a escribir en el disco – los datos de las particiones elegidas se perderán para siempre. Empieza en %1…", "Cancelar", "Finalizar", "La instalación está en marcha. No apagues el ordenador – mientras tanto, mira lo que trae OrkaLinux.", "Paso %1 de %2: %3"],
        "it": ["Attenzione! Le modifiche stanno per essere scritte sul disco – i dati delle partizioni scelte andranno persi per sempre. Inizio tra %1…", "Annulla", "Fine", "L'installazione è in corso. Non spegnere il computer – nel frattempo scopri cosa c'è in OrkaLinux.", "Passo %1 di %2: %3"],
        "pt": ["Atenção! As alterações vão ser gravadas no disco – os dados das partições escolhidas serão perdidos para sempre. Começa em %1…", "Cancelar", "Concluir", "A instalação está em andamento. Não desligue o computador – enquanto isso, veja o que vem no OrkaLinux.", "Etapa %1 de %2: %3"],
        "uk": ["Увага! Зараз зміни буде записано на диск – дані з вибраних розділів зникнуть назавжди. Початок через %1…", "Скасувати", "Завершити", "Триває встановлення. Не вимикайте комп'ютер – тим часом подивіться, що є в OrkaLinux.", "Крок %1 з %2: %3"],
        "en": ["Warning! Changes are about to be written to the disk – data on the chosen partitions will be gone for good. Starting in %1…", "Cancel", "Done", "Installing. Don't turn off the computer – in the meantime, have a look at what's in OrkaLinux.", "Step %1 of %2: %3"]
    })
    readonly property var tr: texts[lang] || texts["en"]
    readonly property string warningText: tr[0]
    readonly property string cancelLabel: tr[1]
    readonly property string doneLabel: tr[2]
    readonly property string installingText: tr[3]
    readonly property string statusText: jobCount > 0
        ? tr[4].arg(jobIndex).arg(jobCount).arg(jobName) : installingText

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 1
        color: "#1c1f38"
    }

    component NavButton: Rectangle {
        id: btn
        property string label: ""
        property bool primary: false
        property bool flat: false
        signal clicked()

        implicitWidth: Math.max(110, caption.implicitWidth + 40)
        implicitHeight: 38
        radius: 19
        opacity: enabled ? 1.0 : 0.35
        color: primary ? (mouse.containsMouse ? Qt.lighter(navigationBar.accent, 1.12) : navigationBar.accent)
                       : (mouse.containsMouse && !flat ? "#1f2340" : "transparent")
        border.width: (primary || flat) ? 0 : 1
        border.color: "#3a4070"

        Behavior on color { ColorAnimation { duration: 120 } }

        Text {
            id: caption
            anchors.centerIn: parent
            text: btn.label.replace("&", "")
            color: btn.primary ? "#ffffff" : (btn.flat ? (mouse.containsMouse ? navigationBar.strongText : "#8a90b8") : "#eceefa")
            font.pointSize: 10
            font.bold: btn.primary
        }

        MouseArea {
            id: mouse
            anchors.fill: parent
            hoverEnabled: true
            enabled: btn.enabled
            cursorShape: Qt.PointingHandCursor
            onClicked: btn.clicked()
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 18
        anchors.rightMargin: 22
        spacing: 10

        NavButton {
            label: ViewManager.quitLabel
            enabled: ViewManager.quitEnabled
            visible: ViewManager.quitVisible && !navigationBar.lastStep && !navigationBar.counting
            onClicked: ViewManager.quit()
        }

        Text {
            visible: navigationBar.installing && !navigationBar.lastStep
            Layout.fillWidth: true
            Layout.leftMargin: 6
            text: navigationBar.statusText
            color: "#a0a6c4"
            font.pointSize: 10
            wrapMode: Text.WordWrap
            maximumLineCount: 2
            elide: Text.ElideRight
        }

        Text {
            visible: navigationBar.counting
            Layout.fillWidth: true
            Layout.leftMargin: 6
            text: navigationBar.warningText.arg(navigationBar.countdown)
            color: "#ff5c6c"
            font.pointSize: 10
            font.bold: true
            wrapMode: Text.WordWrap
            maximumLineCount: 2
            elide: Text.ElideRight
        }

        Item { Layout.fillWidth: true; visible: !navigationBar.counting && !navigationBar.installing }

        NavButton {
            label: navigationBar.cancelLabel
            primary: true
            visible: navigationBar.counting
            onClicked: navigationBar.cancelCountdown()
        }

        NavButton {
            label: ViewManager.backLabel
            enabled: ViewManager.backEnabled
            visible: ViewManager.backAndNextVisible && !navigationBar.lastStep && !navigationBar.counting
            onClicked: ViewManager.back()
        }

        NavButton {
            label: ViewManager.nextLabel
            primary: true
            enabled: ViewManager.nextEnabled
            visible: ViewManager.backAndNextVisible && !navigationBar.lastStep && !navigationBar.counting
            onClicked: navigationBar.startOrNext()
        }

        NavButton {
            label: navigationBar.doneLabel
            primary: true
            visible: navigationBar.lastStep
            onClicked: ViewManager.quit()
        }
    }
}
