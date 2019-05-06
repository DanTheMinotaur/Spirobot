
import {createJoystick} from './joystick';
require ('../packages/notifications/notifications');
import '../packages/notifications/notifications.css';


import '../packages/slide-out/slide-out';

export class UIController{
    constructor(firebase) {
        /**
         * UI Element objects
         * @type {{controlPanel: HTMLElement, eventsPanel: HTMLElement, statusUpdate: HTMLElement, eventsTable: HTMLElement, joystick: HTMLElement, eventsMenuButton: HTMLElement, cameraButton: HTMLElement, videoSwitch: HTMLElement, modeSelect: HTMLElement}}
         */
        this.ui_elements = {
            "videoSwitch": document.getElementById("video-switch"),
            "cameraButton": document.getElementById("camera-button"),
            "eventsTable": document.getElementById("events-table"),
            "joystickController": document.getElementById("joystick-control"),
            "joystick": document.getElementById("joystick"),
            "statusUpdate": document.getElementById("status-update"),
            "modeSelect": document.getElementById("mode-select"),
            "controlPanel": document.getElementById("control-panel"),
            "eventsPanel": document.getElementById('events-panel'),
            "eventsMenuButton": document.getElementById("event-menu-trigger"),
            "videoContainer": document.getElementById("video-container"),
            "controlContainer": document.getElementById("controls-container")
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
        this.joystickController = createJoystick(this.ui_elements.joystickController);

        this.slide_bar = new Slideout({
            'panel': this.ui_elements.controlPanel,
            'menu': this.ui_elements.eventsPanel,
            'padding': 0,
            'tolerance': 70
        });
        this.handleJoystickMovements(1000);
    }

    /**
     * Method sends movements from the joystick to Firebase, assigns an interval to keep transmitting movements at a certain time
     * @param interval delay between transmission of movements
     * @param threshold amount of movement for data to be transmitted
     */
    handleJoystickMovements(interval = 1000, threshold = 25) {
        let self = this;
        /**
         * Inner function which hanles movements from the joystick and transmits them to firebase.
         * up == y > 25
         * down == y < -25
         * left == x < -25
         * right == x > 25
         */

        let caretElements = {
            forward: self.ui_elements.joystick.getElementsByClassName("fa-caret-up")[0],
            backward: self.ui_elements.joystick.getElementsByClassName("fa-caret-down")[0],
            left: self.ui_elements.joystick.getElementsByClassName("fa-caret-left")[0],
            right: self.ui_elements.joystick.getElementsByClassName("fa-caret-right")[0],
        };
        let highlightClass = "highlight-caret";

        function checkMovements(threshold = 25) {
            let currentPosition = self.joystickController.getPosition();
            let highlightedArrow = document.querySelector("." + highlightClass);

            if (highlightedArrow != null) {
                highlightedArrow.classList.remove(highlightClass);
            }

            if (currentPosition.y >= threshold) {
                self.move("forward");
                caretElements.forward.classList.add(highlightClass);
            } else if (currentPosition.y <= -threshold) {
                self.move("backward");
                self.ui_elements.joystick.getElementsByClassName("fa-caret-down");
                caretElements.backward.classList.add(highlightClass);
            } else if (currentPosition.x <= -threshold) {
                self.move("left");
                caretElements.left.classList.add(highlightClass);
            } else if (currentPosition.x >= threshold) {
                self.move("right");
                caretElements.right.classList.add(highlightClass);
            }
        }

        setInterval( () => checkMovements(threshold), interval);
    }

    /**
     * Method will send movement
     * @param movement Direction of movement to send
     */
    move(movement = false) {
        console.log("Moving Bot: " + movement);
        this.controls.update(
            {
                "move": movement
            }
        );
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
            console.log("Events Full Data: " + eventsData);
            for (let key in eventsData) {
                try {
                    addRow('<i class="fa fa-bell-o">', eventsData[key].message, eventsData[key].datetime);
                } catch (e) {
                    console.log("Error in data keys ");
                    console.log(e);
                }
            }
        });
        //this.events.off();
        this.events.limitToLast(1).on('child_added', function (newChildData) {
            //console.log(newChildData.val());
            try {
                let message = newChildData.val().message;
                addRow('<i class="fa fa-bell-o">', message, newChildData.val().datetime);
                self.notificationAlert("Latest Notification",  message);
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
            this.controls.update({"video": this.ui_elements.videoSwitch.checked});
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
        this.setSwitchs();
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
                status__tag.innerText = "Waiting for bot to come online...";
            } else {
                status__tag.innerText = status_value;
            }
        })
    }
    /**
     * Sets switch values set from the Firebase Database, will overide any UI elements.
     */
    setSwitchs() {
        let self = this;

        this.controls.child('video').on('value', function (video_value) {
            self.ui_elements.videoSwitch.checked = video_value.val();
            console.log(video_value.val());
            if (!self.ui_elements.videoSwitch.checked) {
                self.ui_elements.videoContainer.classList.remove("show");
                self.ui_elements.videoContainer.classList.add("hide", "animate", "bounceOutLeft");
            } else {
                self.ui_elements.videoContainer.classList.remove("hide");
                self.ui_elements.videoContainer.classList.add("show");
            }
        });
        // Sets switch auto/manual mode from Firebase.
        this.controls.child('auto_mode').on('value', function (mode_val) {
            self.ui_elements.modeSelect.value = mode_val.val();
        });
    }
}