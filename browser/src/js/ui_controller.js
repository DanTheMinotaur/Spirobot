
import {createJoystick} from './joystick';
import {BotController} from "./bot_contoller";

export class UIController{
    constructor(firebase) {
        this.bot_controller = new BotController(firebase);
        this.ui_elements = {
            "video_switch": document.getElementById("video-switch"),
            "camera_button": document.getElementById("camera-button"),

        };
        this.joystick = document.getElementById("joystick");
        //this.setListeners();
        createJoystick(this.joystick);
        console.log(this.bot_controller);
    }

    /**
     * Creates UI listener events for user interaction.
     */
    setListeners() {
        this.ui_elements.camera_button.addEventListener("click", () => {
            console.log("Clicked Camera");
            this.bot_controller.takePicture();
        });
    }

    setUIStatus() {
        return null;
    }
}