/* OrkaLinux – pokaz slajdów podczas instalacji (Karmelek). */

import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    SystemPalette { id: pal }

    Timer {
        interval: 5000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Image {
            id: welcomeImage
            source: "slide1.jpg"
            width: 560; height: 330
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -30
        }
        Text {
            anchors.horizontalCenter: welcomeImage.horizontalCenter
            anchors.top: welcomeImage.bottom
            anchors.topMargin: 12
            width: 600
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            color: pal.windowText
            text: qsTr("Witaj w OrkaLinux!<br/>Reszta instalacji przebiega automatycznie i potrwa kilka minut.")
        }
    }

    Slide { Image { source: "slide2.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide3.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide4.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide5.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide6.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide7.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide8.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }
    Slide { Image { source: "slide9.jpg"; anchors.fill: parent; anchors.margins: 12; fillMode: Image.PreserveAspectFit } }

    function onActivate() { presentation.currentSlide = 0; }
    function onLeave() { }
}
