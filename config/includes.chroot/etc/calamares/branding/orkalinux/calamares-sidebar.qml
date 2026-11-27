import io.calamares.ui 1.0
import io.calamares.core 1.0

import QtQuick 2.3
import QtQuick.Layouts 1.3

Rectangle {
    id: topBar
    color: Branding.styleString(Branding.SidebarBackground)
    height: 64

    readonly property color accent: Branding.styleString(Branding.SidebarBackgroundCurrent)
    readonly property color textColor: Branding.styleString(Branding.SidebarText)
    readonly property color dimColor: "#5a6088"
    readonly property color strongText: "#fffffe"

    readonly property string lang: {
        var b = ViewManager.backLabel.replace("&", "");
        var known = { "Wstecz": "pl", "Zurück": "de", "Précédent": "fr", "Atrás": "es",
                      "Indietro": "it", "Voltar": "pt", "Назад": "uk" };
        return known[b] || "en";
    }
    readonly property var groupNames: ({
        "pl": ["Witaj", "Region", "Dysk", "Wygląd", "Konto", "Instalacja"],
        "de": ["Willkommen", "Region", "Festplatte", "Aussehen", "Konto", "Installation"],
        "fr": ["Bienvenue", "Région", "Disque", "Apparence", "Compte", "Installation"],
        "es": ["Bienvenida", "Región", "Disco", "Aspecto", "Cuenta", "Instalación"],
        "it": ["Benvenuto", "Regione", "Disco", "Aspetto", "Account", "Installazione"],
        "pt": ["Boas-vindas", "Região", "Disco", "Aparência", "Conta", "Instalação"],
        "uk": ["Вітаємо", "Регіон", "Диск", "Вигляд", "Акаунт", "Встановлення"],
        "en": ["Welcome", "Region", "Disk", "Look", "Account", "Install"]
    })
    readonly property var groupOfStep: [0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 5]
    readonly property int currentGroup: {
        var i = ViewManager.currentStepIndex;
        if (i < 0) return 0;
        return i < groupOfStep.length ? groupOfStep[i] : 5;
    }

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 1
        color: "#262a48"
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 22
        anchors.rightMargin: 22
        spacing: 18

        Image {
            Layout.alignment: Qt.AlignVCenter
            source: "file:/" + Branding.imagePath(Branding.ProductLogo)
            sourceSize.width: 32
            sourceSize.height: 32
            width: 32
            height: 32
            fillMode: Image.PreserveAspectFit
        }

        Column {
            Layout.alignment: Qt.AlignVCenter
            spacing: 2
            Text {
                text: "@ORKA_NAME@"
                color: topBar.strongText
                font.pointSize: 12
                font.bold: true
            }
            Text {
                text: "@ORKA_VERSION@ · @ORKA_CODENAME@"
                color: topBar.dimColor
                font.pointSize: 9
            }
        }

        Item { Layout.preferredWidth: 10 }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

        Repeater {
            model: 6

            Item {
                id: step
                Layout.fillWidth: true
                Layout.fillHeight: true

                readonly property bool done: index < topBar.currentGroup
                readonly property bool current: index == topBar.currentGroup

                Rectangle {
                    visible: index > 0
                    height: 2
                    radius: 1
                    anchors.verticalCenter: dot.verticalCenter
                    anchors.right: dot.left
                    anchors.rightMargin: 6
                    width: step.width / 2 - dot.width / 2 - 6
                    color: (step.done || step.current) ? topBar.accent : "#2c3156"
                }
                Rectangle {
                    visible: index < 5
                    height: 2
                    radius: 1
                    anchors.verticalCenter: dot.verticalCenter
                    anchors.left: dot.right
                    anchors.leftMargin: 6
                    width: step.width / 2 - dot.width / 2 - 6
                    color: step.done ? topBar.accent : "#2c3156"
                }

                Rectangle {
                    id: dot
                    width: 22
                    height: 22
                    radius: 11
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    color: step.current ? topBar.accent : (step.done ? "#1f2350" : "transparent")
                    border.width: step.current ? 0 : 2
                    border.color: step.done ? topBar.accent : "#3a4070"

                    Behavior on color { ColorAnimation { duration: 200 } }

                    Text {
                        anchors.centerIn: parent
                        text: step.done ? "✓" : (index + 1)
                        color: step.current ? "#ffffff" : (step.done ? "#aab1ff" : topBar.dimColor)
                        font.pointSize: 9
                        font.bold: true
                    }
                }

                Text {
                    anchors.horizontalCenter: dot.horizontalCenter
                    anchors.top: dot.bottom
                    anchors.topMargin: 4
                    width: step.width
                    horizontalAlignment: Text.AlignHCenter
                    elide: Text.ElideRight
                    text: (topBar.groupNames[topBar.lang] || topBar.groupNames["en"])[index]
                    color: step.current ? topBar.strongText : (step.done ? topBar.textColor : topBar.dimColor)
                    font.pointSize: 8
                    font.bold: step.current
                }
            }
        }
        }

        Rectangle {
            Layout.alignment: Qt.AlignVCenter
            width: 26
            height: 26
            radius: 13
            color: aboutMouse.containsMouse ? "#262a48" : "transparent"
            border.width: 1
            border.color: "#3a4070"
            Text {
                anchors.centerIn: parent
                text: "i"
                color: topBar.dimColor
                font.pointSize: 9
                font.bold: true
            }
            MouseArea {
                id: aboutMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: debug.about()
            }
        }
    }
}
