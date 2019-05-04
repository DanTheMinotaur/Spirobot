
/**
 * Class for controlling bot functionality using firebase live Database
 * @constructor Firebase Instance
 */
export class BotController{
    constructor(firebase) {
        this.database = firebase.database();
        this.controls = this.database.ref('/controls/');
        this.events = this.database.ref('/events/');
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
    updateEvents(eventsTableElem) {

        function addRow(icon, message, datetime) {
            let row = eventsTableElem.insertRow(0);
            row.insertCell(0).innerHTML = icon;
            row.insertCell(1).innerHTML = message;
            row.insertCell(2).innerHTML = datetime;
        }
        console.log("Events Called");
        //console.log(eventsTableElem);
        this.events.on('value', function (eventsData) {
            eventsData = eventsData.val();

            console.log(typeof eventsData);

            for (let key in eventsData) {
                try {
                    addRow('<i class="fa fa-bell-o">', eventsData[key].message, eventsData[key].datetime);
                } catch (e) {
                    console.log("Error in data keys ");
                    console.log(e);
                }

            }
        });
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
}
