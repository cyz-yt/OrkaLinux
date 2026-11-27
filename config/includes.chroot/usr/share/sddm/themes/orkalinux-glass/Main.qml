import QtQuick 2.15

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#04051e"

    readonly property bool side: config.layout === "side"
    readonly property real s: Math.max(0.7, Math.min(1.3, height / 1080))
    readonly property color accent: "#4f58f0"

    readonly property string lang: {
        var ui = Qt.locale().uiLanguages;
        return (ui && ui.length ? ui[0] : Qt.locale().name).substring(0, 2);
    }
    readonly property var texts: ({
        "pl": { password: "Hasło", failed: "Złe hasło, spróbuj jeszcze raz", session: "Sesja",
                suspend: "Uśpij", reboot: "Uruchom ponownie", shutdown: "Wyłącz", caps: "Caps Lock jest włączony", checking: "Sprawdzam…" },
        "de": { password: "Passwort", failed: "Falsches Passwort, versuch es nochmal", session: "Sitzung",
                suspend: "Standby", reboot: "Neu starten", shutdown: "Ausschalten", caps: "Feststelltaste ist an", checking: "Wird geprüft…" },
        "fr": { password: "Mot de passe", failed: "Mauvais mot de passe, réessaie", session: "Session",
                suspend: "Veille", reboot: "Redémarrer", shutdown: "Éteindre", caps: "Verr. Maj est activé", checking: "Vérification…" },
        "en": { password: "Password", failed: "Wrong password, try again", session: "Session",
                suspend: "Sleep", reboot: "Restart", shutdown: "Shut down", caps: "Caps Lock is on", checking: "Checking…" }
    })
    readonly property var t: texts[lang] !== undefined ? texts[lang] : texts["en"]

    property int userIndex: userModel.lastIndex >= 0 ? userModel.lastIndex : 0
    property string userName: ""
    property string userReal: ""
    property string userIcon: ""
    property int sessionIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
    property string sessionName: ""
    property bool failed: false
    property bool busy: false

    function login() {
        if (root.busy)
            return
        root.busy = true
        root.failed = false
        sddm.login(root.userName, password.text, root.sessionIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false
            root.failed = true
            password.text = ""
            shake.restart()
            password.forceActiveFocus()
        }
    }

    Repeater {
        id: users
        model: userModel
        Item {
            property bool current: index === root.userIndex
            function pick() {
                root.userName = model.name
                root.userReal = (model.realName && model.realName.length > 0) ? model.realName : model.name
                root.userIcon = model.icon ? String(model.icon) : ""
            }
            onCurrentChanged: if (current) pick()
            Component.onCompleted: if (current) pick()
        }
    }
    Repeater {
        id: sessions
        model: sessionModel
        Item {
            property bool current: index === root.sessionIndex
            onCurrentChanged: if (current) root.sessionName = model.name
            Component.onCompleted: if (current) root.sessionName = model.name
        }
    }

    Image {
        anchors.fill: parent
        source: config.background
        fillMode: Image.PreserveAspectCrop
        smooth: true
        asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        visible: !root.side
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#8c04051e" }
            GradientStop { position: 0.5; color: "#3304051e" }
            GradientStop { position: 1.0; color: "#b304051e" }
        }
    }
    Rectangle {
        id: panel
        visible: root.side
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        width: Math.max(420, root.width * 0.3)
        color: "#e6070b26"
        Rectangle {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            width: 1
            color: "#33ffffff"
        }
    }

    Column {
        id: clock
        spacing: 4 * root.s
        y: root.side ? 90 * root.s : 110 * root.s
        x: root.side ? 64 * root.s : (root.width - width) / 2

        property date now: new Date()
        Timer {
            interval: 1000
            running: true
            repeat: true
            onTriggered: clock.now = new Date()
        }
        Text {
            anchors.horizontalCenter: root.side ? undefined : parent.horizontalCenter
            text: clock.now.toLocaleTimeString(Qt.locale(), "HH:mm")
            color: "#ffffff"
            font.pixelSize: (root.side ? 96 : 120) * root.s
            font.weight: Font.Light
        }
        Text {
            anchors.horizontalCenter: root.side ? undefined : parent.horizontalCenter
            text: clock.now.toLocaleDateString(Qt.locale(), "dddd, d MMMM")
            color: "#d9dcff"
            font.pixelSize: 22 * root.s
        }
    }

    Column {
        id: form
        spacing: 14 * root.s
        width: 360 * root.s
        x: root.side ? 64 * root.s : (root.width - width) / 2
        y: root.side ? root.height - height - 150 * root.s : root.height * 0.5 - 40 * root.s

        Rectangle {
            anchors.horizontalCenter: root.side ? undefined : parent.horizontalCenter
            width: 96 * root.s
            height: width
            radius: width / 2
            color: "#33ffffff"
            border.color: "#59ffffff"
            border.width: 1
            Canvas {
                id: avatar
                anchors.fill: parent
                anchors.margins: 2
                readonly property string fallback: "file:///usr/share/orkalinux/avatar.png"
                readonly property string src: root.userIcon.length > 0
                    ? (root.userIcon.indexOf("file:") === 0 ? root.userIcon : "file://" + root.userIcon)
                    : fallback
                onSrcChanged: { loadImage(src); requestPaint() }
                onImageLoaded: requestPaint()
                Component.onCompleted: { loadImage(fallback); loadImage(src) }
                onPaint: {
                    var ctx = getContext("2d")
                    ctx.reset()
                    var img = (isImageLoaded(src) && !isImageError(src)) ? src : fallback
                    if (!isImageLoaded(img))
                        return
                    ctx.save()
                    ctx.beginPath()
                    ctx.arc(width / 2, height / 2, width / 2, 0, 2 * Math.PI)
                    ctx.closePath()
                    ctx.clip()
                    ctx.drawImage(img, 0, 0, width, height)
                    ctx.restore()
                }
            }
        }
        Text {
            anchors.horizontalCenter: root.side ? undefined : parent.horizontalCenter
            text: root.userReal
            color: "#ffffff"
            font.pixelSize: 24 * root.s
            font.bold: true
        }

        Rectangle {
            width: parent.width
            height: 48 * root.s
            radius: height / 2
            color: "#29ffffff"
            border.color: root.failed ? "#ff8098" : (password.activeFocus ? "#b38a93ff" : "#4dffffff")
            border.width: root.failed ? 2 : 1
            opacity: root.busy ? 0.6 : 1.0
            transform: Translate { id: shakeX }
            SequentialAnimation {
                id: shake
                NumberAnimation { target: shakeX; property: "x"; to: -12 * root.s; duration: 50 }
                NumberAnimation { target: shakeX; property: "x"; to: 12 * root.s; duration: 70 }
                NumberAnimation { target: shakeX; property: "x"; to: -8 * root.s; duration: 70 }
                NumberAnimation { target: shakeX; property: "x"; to: 8 * root.s; duration: 70 }
                NumberAnimation { target: shakeX; property: "x"; to: 0; duration: 50 }
            }

            TextInput {
                id: password
                anchors.left: parent.left
                anchors.right: go.left
                anchors.leftMargin: 20 * root.s
                anchors.rightMargin: 10 * root.s
                anchors.verticalCenter: parent.verticalCenter
                echoMode: TextInput.Password
                passwordCharacter: "●"
                color: "#ffffff"
                font.pixelSize: 16 * root.s
                clip: true
                focus: true
                readOnly: root.busy
                onTextChanged: if (text.length > 0) root.failed = false
                Keys.onReturnPressed: root.login()
                Keys.onEnterPressed: root.login()
                Component.onCompleted: forceActiveFocus()
            }
            Text {
                anchors.left: password.left
                anchors.verticalCenter: parent.verticalCenter
                visible: password.text.length === 0
                text: root.t.password
                color: "#99ffffff"
                font.pixelSize: 16 * root.s
            }
            Rectangle {
                id: go
                anchors.right: parent.right
                anchors.rightMargin: 5 * root.s
                anchors.verticalCenter: parent.verticalCenter
                width: 38 * root.s
                height: width
                radius: width / 2
                color: goMouse.containsMouse ? Qt.lighter(root.accent, 1.15) : root.accent
                Text {
                    anchors.centerIn: parent
                    text: "→"
                    color: "#ffffff"
                    font.pixelSize: 20 * root.s
                    font.bold: true
                }
                MouseArea {
                    id: goMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.login()
                }
            }
        }

        Text {
            anchors.horizontalCenter: root.side ? undefined : parent.horizontalCenter
            text: root.busy ? root.t.checking : (root.failed ? root.t.failed : (keyboard.capsLock ? root.t.caps : " "))
            color: root.busy ? "#ccffffff" : (root.failed ? "#ff8098" : "#ffc857")
            font.pixelSize: 14 * root.s
            font.bold: root.failed
        }

        Flow {
            width: parent.width
            spacing: 8 * root.s
            visible: users.count > 1
            Repeater {
                model: userModel
                Rectangle {
                    height: 30 * root.s
                    width: chipText.implicitWidth + 28 * root.s
                    radius: height / 2
                    color: index === root.userIndex ? "#664f58f0" : (chipMouse.containsMouse ? "#33ffffff" : "#1fffffff")
                    border.color: "#33ffffff"
                    Text {
                        id: chipText
                        anchors.centerIn: parent
                        text: (model.realName && model.realName.length > 0) ? model.realName : model.name
                        color: "#ffffff"
                        font.pixelSize: 13 * root.s
                    }
                    MouseArea {
                        id: chipMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            root.userIndex = index
                            root.failed = false
                            password.forceActiveFocus()
                        }
                    }
                }
            }
        }
    }

    Row {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: (root.side ? 64 : 40) * root.s
        anchors.bottomMargin: (root.side ? 36 + 34 + 12 : 36) * root.s
        Rectangle {
            height: 34 * root.s
            width: sessText.implicitWidth + 30 * root.s
            radius: height / 2
            color: sessMouse.containsMouse ? "#33ffffff" : "#1fffffff"
            visible: sessions.count > 1
            Text {
                id: sessText
                anchors.centerIn: parent
                text: root.t.session + ": " + root.sessionName + "  ▾"
                color: "#e6e9ff"
                font.pixelSize: 13 * root.s
            }
            MouseArea {
                id: sessMouse
                anchors.fill: parent
                hoverEnabled: true
                onClicked: root.sessionIndex = (root.sessionIndex + 1) % sessions.count
            }
        }
    }

    Row {
        id: power
        spacing: 10 * root.s
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 36 * root.s
        x: root.side ? 64 * root.s : root.width - width - 40 * root.s

        Repeater {
            model: [
                { label: root.t.suspend, icon: "system-suspend", can: sddm.canSuspend, act: 0 },
                { label: root.t.reboot, icon: "system-reboot", can: sddm.canReboot, act: 1 },
                { label: root.t.shutdown, icon: "system-shutdown", can: sddm.canPowerOff, act: 2 }
            ]
            Rectangle {
                visible: modelData.can
                height: 34 * root.s
                width: powerRow.implicitWidth + 26 * root.s
                radius: height / 2
                color: powerMouse.containsMouse ? "#40ffffff" : "#1fffffff"
                Row {
                    id: powerRow
                    anchors.centerIn: parent
                    spacing: 6 * root.s
                    Image {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 16 * root.s
                        height: width
                        source: "/usr/share/icons/breeze-dark/actions/22/" + modelData.icon + ".svg"
                        sourceSize.width: 32
                        sourceSize.height: 32
                    }
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: modelData.label
                        color: "#e6e9ff"
                        font.pixelSize: 13 * root.s
                    }
                }
                MouseArea {
                    id: powerMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        if (modelData.act === 0) sddm.suspend()
                        else if (modelData.act === 1) sddm.reboot()
                        else sddm.powerOff()
                    }
                }
            }
        }
    }
}
