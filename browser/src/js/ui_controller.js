
import {createJoystick} from './joystick';
require ('../packages/notifications/notifications');
import '../packages/notifications/notifications.css';


import '../packages/slide-out/slide-out';

export class UIController{
    constructor(firebase) {
        //this.bot_controller = new BotController(firebase);
        this.ui_elements = {
            "videoSwitch": document.getElementById("video-switch"),
            "cameraButton": document.getElementById("camera-button"),
            "eventsTable": document.getElementById("events-table"),
            "joystick": document.getElementById("joystick-control"),
            "statusUpdate": document.getElementById("status-update"),
            "modeSelect": document.getElementById("mode-select"),
            "controlPanel": document.getElementById("control-panel"),
            "eventsPanel": document.getElementById('events-panel'),
            "eventsMenuButton": document.getElementById("event-menu-trigger")
        };


        /**
         * Firebase DB refs
         * @type {firebase.database.Database | * | never}
         */

        this.database = firebase.database();
        this.controls = this.database.ref('/controls/');
        this.events = this.database.ref('/events/');
        this.status = this.database.ref('/status/');
        this.mode = this.database.ref('/auto_mode/');

        this.notificationObject = window.createNotification({
            closeOnClick: true,
            displayCloseButton: false,
            positionClass: 'nfc-bottom-right',
            onclick: false,
            showDuration: 3500,
            theme: 'success'
        });
        createJoystick(this.ui_elements.joystick);

        this.testButton = document.getElementById("test");

        this.slide_bar = new Slideout({
            'panel': this.ui_elements.controlPanel,
            'menu': this.ui_elements.eventsPanel,
            'padding': 0,
            'tolerance': 70
        });


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
        let self = this;

        function addRow(icon, message, datetime) {
            //console.log("Adding Row for message:" + message);
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
                let message = newChildData.val().message;
                addRow('<i class="fa fa-bell-o">', message, newChildData.val().datetime);
                self.notificationAlert("New Notification",  message);
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
            this.takePicture();
        });

        this.ui_elements.videoSwitch.addEventListener("change", () =>{
            this.controls.update({"video": this.ui_elements.autoSwitch.checked});
        });

        this.ui_elements.modeSelect.addEventListener("click", () => {
            let selected_res = (this.ui_elements.modeSelect[this.ui_elements.modeSelect.selectedIndex].value === "true");
            console.log("Selected Option: " + selected_res);
            this.controls.update({"auto_mode": selected_res})
        });

        this.ui_elements.controlPanel.addEventListener("click", () => {
            console.log("Control Listener Triggere");
            if (this.slide_bar.isOpen()) {
                this.slide_bar.toggle();
            }
        });

        this.ui_elements.eventsMenuButton.addEventListener("click", () => {
            console.log("Clicked");
            this.slide_bar.toggle();
        });

        this.updateEvents();
        this.checkStatus();
        this.setSwitchCurrentValues();
    }



    /**
     * Creates notifcation for display
     * @param title The title of the notification
     * @param message the message to display in the notification.
     * @param type The type of message being displayed
     */
    notificationAlert(title, message, type = "success") {
        this.notificationObject({
            title: title,
            message: message
        });
    }

    /**
     * Pings bot to check if its online
     */
    pingBot() {
        console.log("Ping Bot");
        this.controls.update({
            "ping": false
        })
    }

    /**
     * Checks the current status of the bot.
     */
    checkStatus() {
        let status_elm = this.ui_elements.statusUpdate;
        this.status.on('value', function (status_details) {
            let status_value = status_details.val();
            let status__tag = status_elm.getElementsByTagName("p")[0];
            if (status_value === false) {
                status__tag.innerText = "Waiting for status...";
            } else {
                status__tag.innerText = status_value;
            }
        })
    }
    /**
     * Sets switch values set from the Firebase Database, will overide any UI elements.
     */
    setSwitchCurrentValues() {
        let self = this;

        this.controls.child('video').on('value', function (video_value) {
            self.ui_elements.videoSwitch.checked = video_value.val();
        });
        // Sets switch auto/manual mode from Firebase.
        this.controls.child('auto_mode').on('value', function (mode_val) {
            self.ui_elements.modeSelect.value = mode_val.val();
        });
    }
}