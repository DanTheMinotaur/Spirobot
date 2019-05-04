
/**
 * Class for controlling bot functionality using firebase live Database
 * @constructor Firebase Instance
 */
export class BotController{
    constructor(firebase) {
        this.database = firebase.database();
        this.control_path = this.database.ref('/controls/');
        this.camera_button = document.getElementById("camera-button");
    }

    getStatusDetails() {
        
    }


    /**
     * Method will send movement
     * @param movement Direction of movement to send
     */
    move(movement = null) {
        console.log("Moving Bot: " + movement);
        this.control_path.update(
            {
                "move": movement
            }
        );
    }

    videoState(active) {
        if (typeof active == 'boolean') {
            console.log("Switching video to " + active);
            this.control_path.update({
                "video": active
            });
        }
    }

    takePicture() {
        this.control_path.update({
            "picture": true
        });
    }
}
