
import {createJoystick} from './joystick';
import {BotController} from "./bot_contoller";

export class UIController{
    constructor(firebase) {
        this.bot_controller = new BotController(firebase);
        this.ui_elements = {
            "videoSwitch": document.getElementById("video-switch"),
            "cameraButton": document.getElementById("camera-button"),
            "eventsTable": document.getElementById("events-table")

        };
        this.joystick = document.getElementById("joystick");
        createJoystick(this.joystick);
        console.log(this.bot_controller);
        console.log(this.ui_elements);
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

    eventRowFormatter(icon, message, datetime){

    }

    setUIStatus() {
        return null;
    }


    // _updateEvents() {
    //     this.bot_controller.events.on('value', function (eventsData) {
    //         eventsData = eventsData.val();
    //
    //         console.log(typeof eventsData);
    //
    //
    //         for (let key in eventsData) {
    //             console.log(key);
    //             console.log(eventsData[key].message);
    //             this.ui_elements.eventsTable.appendChild(
    //                 `<tr><td><i class="fa fa-bell-o"></i></td><td>${eventsData[key].message}</td><td>${eventsData[key].message}</td></tr>`
    //             );
    //         }
    //
    //     });
    // }
}