import QtQuick 2.0

import calamares.slideshow 1.0



Presentation {

    id: presentation

    Timer {

        interval: 3000

        running: true

        repeat: true

        onTriggered: presentation.goToNextSlide()

    }

    Slide {

        Image {

            source: "Karmelek1.jpeg"

            anchors.fill: parent

            fillMode: Image.PreserveAspectCrop

        }

    }

    Slide {

        Image {

            source: "Karmelek2.jpeg"

            anchors.fill: parent

            fillMode: Image.PreserveAspectCrop

        }

    }

    Slide {

        Image {

            source: "Karmelek3.jpeg"

            anchors.fill: parent

            fillMode: Image.PreserveAspectCrop

        }

    }

    Slide {

        Image {

            source: "Karmelek4.jpeg"

            anchors.fill: parent

            fillMode: Image.PreserveAspectCrop

        }

    }

    Slide {

        Image {

            source: "Karmelek5.jpeg"

            anchors.fill: parent

            fillMode: Image.PreserveAspectCrop
        }
    }
    Slide {
        Image {
            source: "Karmelek6.jpeg"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }
    }
    Slide {
        Image {
            source: "Karmelek7.jpeg"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }
    }
    Slide {
        Image {
            source: "Karmelek8.jpeg"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }
    }
    Slide {
        Image {
            source: "Karmelek9.jpeg"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }
    }
}
