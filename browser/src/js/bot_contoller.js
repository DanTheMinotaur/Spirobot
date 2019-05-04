
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

    takePicture() {
        this.controls.update({
            "picture": true
        });
    }

    /**
     *
     * @param eventsElem the event table to be updated
     */
    updateEvents(eventsTableElem) {
        console.log("Events Called");
        console.log(eventsTableElem);
        this.events.on('value', function (eventsData) {
            eventsData = eventsData.val();

            console.log(typeof eventsData);

            for (let key in eventsData) {
                console.log(key);
                console.log(eventsData[key].message);
                let row = eventsTableElem.insertRow(0);
                row.insertCell(0).innerHTML = '<i class="fa fa-bell-o">';
                row.insertCell(1).innerHTML = eventsData[key].message;
                row.insertCell(2).innerHTML = eventsData[key].datetime;
                // eventsElem.appendChild(
                //     `<tr><td><i class="fa fa-bell-o"></i></td><td>${eventsData[key].message}</td><td>${eventsData[key].message}</td></tr>`
                // );
            }

        });
    }
}
