
import {createJoystick} from './joystick';
import {BotController} from "./bot_contoller";
require ('../packages/notifications/notifications');
import '../packages/notifications/notifications.css';

export class UIController{
    constructor(firebase) {
        this.bot_controller = new BotController(firebase);
        this.ui_elements = {
            "videoSwitch": document.getElementById("video-switch"),
            "cameraButton": document.getElementById("camera-button"),
            "eventsTable": document.getElementById("events-table")

        };
        this.notificationObject = window.createNotification({
            closeOnClick: true,
            displayCloseButton: false,
            positionClass: 'nfc-bottom-right',
            onclick: false,
            showDuration: 3500,
            theme: 'success'
        });
        this.joystick = document.getElementById("joystick");
        createJoystick(this.joystick);
        this.bot_controller.updateEvents(this.ui_elements.eventsTable);
    }

    /**
     * Creates UI listener events for user interaction.
     */
    setListeners() {
        this.ui_elements.cameraButton.addEventListener("click", () => {
            console.log("Clicked Camera");
            this.bot_controller.takePicture();
        });
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