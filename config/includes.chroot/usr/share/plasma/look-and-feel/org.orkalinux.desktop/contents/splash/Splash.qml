import QtQuick

Rectangle {
    id: root
    property int stage

    gradient: Gradient {
        GradientStop { position: 0.0; color: "#03051a" }
        GradientStop { position: 1.0; color: "#0a1050" }
    }

    onStageChanged: {
        if (stage === 2) {
            intro.running = true
        }
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Image {
            id: logo
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -Math.round(root.height * 0.04)
            source: "images/orka.png"
            height: Math.round(root.height * 0.16)
            sourceSize.height: height
            fillMode: Image.PreserveAspectFit
            smooth: true
        }

        Rectangle {
            id: track
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: logo.bottom
            anchors.topMargin: Math.round(root.height * 0.06)
            width: Math.round(root.width * 0.14)
            height: 4
            radius: 2
            color: "#1d235c"

            Rectangle {
                height: parent.height
                radius: 2
                width: parent.width * Math.max(0, Math.min(root.stage, 6)) / 6
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#2b3bff" }
                    GradientStop { position: 1.0; color: "#6a2bff" }
                }
                Behavior on width {
                    NumberAnimation { duration: 450; easing.type: Easing.OutCubic }
                }
            }
        }
    }

    OpacityAnimator {
        id: intro
        target: content
        from: 0
        to: 1
        duration: 600
        easing.type: Easing.InOutQuad
    }
}
