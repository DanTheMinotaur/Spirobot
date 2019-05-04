
/**
 * Class for controlling bot functionality using firebase live Database
 * @constructor Firebase Instance
 */
export class BotController{
    constructor(firebase) {
        this.database = firebase.database();
    }

    /**
     * Method will send movement
     * @param movement Direction of movement to send
     */
    move(movement = null) {
        console.log("Moving Bot: " + movement);
        this.database.ref('/').update(
            {
                "move": movement
            }
        );
    }
}
