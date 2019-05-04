
import {createJoystick} from './joystick';
import {BotController} from "./bot_contoller";
require ('../packages/notifications/notifications');
import '../packages/notifications/notifications.css';

export class UIController{
    constructor(firebase) {
        //this.bot_controller = new BotController(firebase);
        this.ui_elements = {
            "videoSwitch": document.getElementById("video-switch"),
            "cameraButton": document.getElementById("camera-button"),
            "eventsTable": document.getElementById("events-table"),
            "joystick": document.getElementById("joystick")

        };


        /**
         * Firebase DB refs
         * @type {firebase.database.Database | * | never}
         */
        this.database = firebase.database();
        this.controls = this.database.ref('/controls/');
        this.events = this.database.ref('/events/');
        this.status = this.database.ref('/status/')

        this.notificationObject = window.createNotification({
            closeOnClick: true,
            displayCloseButton: false,
            positionClass: 'nfc-bottom-right',
            onclick: false,
            showDuration: 3500,
            theme: 'success'
        });
        createJoystick(this.ui_elements.joystick);
    }

    /**
     * Method will send movement
     * @param movement Direction of movement to send
     */
    move(movement = null) {
        console.log("Moving Bot: " + movement);
        this.controls.update(
            {
                "move": movement
            }
        );
    }

    videoState(active) {
        if (typeof active == 'boolean') {
            console.log("Switching video to " + active);
            this.controls.update({
                "video": active
            });
        }
    }

    /**
     * Send command to firebase to instruct the bot to take a picture
     */
    takePicture() {
        this.controls.update({
            "picture": true
        });
    }

    /**
     * Handles event updates from Firebase live database.
     * @param eventsTableElem the event table to be updated
     */
    updateEvents(eventsTableElem = this.ui_elements.eventsTable) {

        function addRow(icon, message, datetime) {
            console.log("Adding Row for message:" + message);
            let row = eventsTableElem.insertRow(0);
            row.insertCell(0).innerHTML = icon;
            row.insertCell(1).innerHTML = message;
            row.insertCell(2).innerHTML = datetime;
        }

        this.events.on('value', function (eventsData) {
            eventsData = eventsData.val();

            for (let key in eventsData) {
                try {
                    addRow('<i class="fa fa-bell-o">', eventsData[key].message, eventsData[key].datetime);
                } catch (e) {
                    console.log("Error in data keys ");
                    console.log(e);
                }
            }
        });
        this.events.off();
        this.events.on('child_added', function (newChildData) {
            console.log(newChildData.val());
            try {
                addRow('<i class="fa fa-bell-o">', newChildData.val().message, newChildData.val().datetime);
            } catch (e) {
                console.log("Error in data keys ");
                console.log(e);
            }
        });
    }

    /**
     * Creates UI listener events for user interaction.
     */
    setListeners() {
        this.ui_elements.cameraButton.addEventListener("click", () => {
            console.log("Clicked Camera");
            this.bot_controller.takePicture();
        });
        this.updateEvents();
    }

    createNotification(title, message) {
        this.notificationObject({
            title: title,
            message: message
        })
    }

    setUIStatus() {
        return null;
    }

}