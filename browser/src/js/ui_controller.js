
import {createJoystick} from './joystick';
require ('../packages/notifications/notifications');
import { LuminousGallery } from 'luminous-lightbox';
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
            "controlContainer": document.getElementById("controls-container"),
            "videoStreamContainer": document.getElementById("video-stream-container"),
            "imageGallery": document.getElementById("image-gallery-trigger"),
            "imageGalleryContent": document.getElementById("gallery-content"),
            "galleryPanel": document.getElementById("image-panel")
        };

        // getYouTubeLiveStream();
        this._disableEnableControls();

        /**
         * Firebase DB refs
         * @type {firebase.database.Database | * | never}
         */

        this.firebase = firebase;
        this.database = firebase.database();
        this.controls = this.database.ref('/controls/');
        this.events = this.database.ref('/events/');
        this.status = this.database.ref('/status/');
        this.mode = this.database.ref('/auto_mode/');
        this.images_storage = firebase.storage().ref('/');
        this.galleryLoaded = false;
        this.gallery = null;

        this.notificationObject = null;

        this.joystickController = createJoystick(this.ui_elements.joystickController);

        this.sideMenus();
        this.handleJoystickMovements(1000);
        this.setListeners();
        this.pingBot();
        this.handleNotifications()
    }

    /**
     * Method creates and and controls browser notification elements.
     */
    handleNotifications() {
        this.notificationObject = window.createNotification({
            closeOnClick: true,
            displayCloseButton: false,
            positionClass: 'nfc-bottom-right',
            onclick: false,
            showDuration: 3500,
            theme: 'success'
        });

        const messaging = firebase.messaging();
        messaging.requestPermission().then(() => {
            console.log("Notification Permission Granted");
            return messaging.getToken();
        }).then((token) => {
            console.log("Token: " + token);
            this.database.ref("/").update({
                "token": token
            });
        }).catch((error) => {
            console.log("Could not obtain permission for notifications" + error);
        });

        messaging.onMessage((payload) => {
            console.log('onMessage: ', payload);
            let notification_data = payload.notification;
            this.notificationAlert(notification_data.title, notification_data.body, "warning");
        });
    }

    sideMenus() {
        let events_bar = new Slideout({
            'panel': this.ui_elements.controlPanel,
            'menu': this.ui_elements.eventsPanel,
            'padding': 0,
            'tolerance': 70
        });

        this.ui_elements.eventsMenuButton.addEventListener("click", () => {
            events_bar.toggle();
            events_bar.menu.style.zIndex = "2";
        });

        let gallery_bar = new Slideout({
            'side': 'right',
            'panel': this.ui_elements.controlPanel,
            'menu': this.ui_elements.galleryPanel,
            'padding': 0,
            'tolerance': 70

        });

        this.ui_elements.imageGallery.addEventListener("click", () => {
           gallery_bar.toggle();
           gallery_bar.menu.style.zIndex = "2";
           if (!this.galleryLoaded) {
               this.loadImageGallery();
               this.galleryLoaded = true;
           }
        });

        this.ui_elements.controlPanel.addEventListener("click", () => {
            if (events_bar.isOpen()) {
                events_bar.toggle();
                events_bar.menu.style.zIndex = "0";
            }
            if (gallery_bar.isOpen()) {
                gallery_bar.toggle();
                gallery_bar.menu.style.zIndex = "0";
            }
        });
    }

    loadImageGallery() {
        let self = this;
        let image_list = document.getElementById("image-list");

        function buildGalleryElm(img_src, img_title) {
            return `<a class="list-item image-lightbox" href="${img_src}">
                    <div class="card is-shady">
                    <div class="card-image">
                        <figure class="image is-4by3">
                            <img src="${img_src}" alt="${img_title}?w=1600" data-target="modal-image2">
                        </figure>
                    </div>
                    <div class="card-content">
                        <div class="content">
                            <h4>${img_title}</h4>
                        </div>
                    </div>
                </div></a>`
        }

        let images_ref = this.database.ref('/images');

        images_ref.on('child_added', (image_details) => {
            console.log(image_details.val());
            let image_array = image_details.val().split('/');
            let image_src = image_array[image_array.length - 1];
            self.images_storage.child(image_src).getDownloadURL().then((url) => {
                fetch(url).then((image_data) => {
                    console.log(image_data);
                    let html = new DOMParser().parseFromString(buildGalleryElm(image_data.url, image_src), 'text/html');
                    image_list.appendChild(html.documentElement);
                }).finally(() => {
                    self.gallery = new LuminousGallery(document.querySelectorAll(".image-lightbox",
                        {
                            arrowNavigation: true,
                            injectBaseStyles: false
                        }));
                });
            });

        });


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

        caretElements.forward.addEventListener("click", () => {
            this.move("forward");
        });
        caretElements.backward.addEventListener("click", () => {
            this.move("backward");
        });
        caretElements.right.addEventListener("click", () => {
            this.move("right");
        });
        caretElements.left.addEventListener("click", () => {
            this.move("left");
        });

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
                let event = newChildData.val();
                addRow('<i class="fa fa-bell-o">', event.message, event.datetime);
                self.notificationAlert("Latest Notification",  event.message, event.type);
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
            console.log(this.ui_elements.modeSelect[this.ui_elements.modeSelect.selectedIndex].value);
            let selected_res = this.ui_elements.modeSelect[this.ui_elements.modeSelect.selectedIndex].value;
            if (selected_res === "true" || selected_res === "false") {
                selected_res = (this.ui_elements.modeSelect[this.ui_elements.modeSelect.selectedIndex].value === "true");
            } else {
                selected_res = 0;
            }
            console.log("Selected Option: " + selected_res);
            this.controls.update({"auto_mode": selected_res})
        });

        // this.ui_elements.controlPanel.addEventListener("click", () => {
        //     if (this.events_bar.isOpen()) {
        //         this.events_bar.toggle();
        //     }
        //     if (this.gallery_bar.isOpen()) {
        //         this.gallery_bar.toggle();
        //     }
        // });
        //
        // this.ui_elements.eventsMenuButton.addEventListener("click", () => {
        //     this.events_bar.toggle();
        // });
        //
        // this.ui_elements.imageGallery.addEventListener("click", () => {
        //     //this.loadImageGallery();
        //     this.gallery_bar.toggle();
        //
        // });

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
        this.notificationObject.theme = type;
        console.log(this.notificationObject);
        this.notificationObject({
            title: title,
            message: message
        });
    }

    /**
     * Pings bot to check if its online
     */
    pingBot() {
        let self = this;
        console.log("Ping Bot");
        this.controls.update({
            "ping": false
        });
        this.status.set("Pinging Bot...");
        this.controls.child('ping').on('value', (pingValue) => {
            console.log(pingValue.val());
            self._disableEnableControls(!pingValue.val());
        })
    }

    /**
     * Disables/Enables UI controls
     * @param disable boolean weather to enable or disable controls
     * @private
     */
    _disableEnableControls(disable = true) {
        this.ui_elements.videoSwitch.disabled = disable;
        this.ui_elements.cameraButton.disabled = disable;
        this.ui_elements.modeSelect.disabled = disable;
    }

    /**
     * Checks the current status of the bot.
     */
    checkStatus() {
        let status_elm = this.ui_elements.statusUpdate;
        this.status.on('value', function (status_details) {
            let status_value = status_details.val();
            let status__tag = status_elm.getElementsByTagName("span")[0];
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
                self.ui_elements.videoStreamContainer.classList.remove("bounceInLeft");
                self.ui_elements.videoStreamContainer.classList.add("bounceOutLeft");
            } else {
                self.ui_elements.videoStreamContainer.classList.remove("bounceOutLeft");
                self.ui_elements.videoStreamContainer.classList.add("bounceInLeft");
            }
        });
        // Sets switch auto/manual mode from Firebase.
        this.controls.child('auto_mode').on('value', function (mode_val) {
            self.ui_elements.modeSelect.value = mode_val.val();
            console.log(mode_val.val());
            if (mode_val.val() || mode_val.val() === 0) { // Auto Mode
                self.ui_elements.controlContainer.classList.add("bounceOutRight");
                self.ui_elements.controlContainer.classList.remove("bounceInRight");
            } else {
                self.ui_elements.controlContainer.classList.add("bounceInRight");
                self.ui_elements.controlContainer.classList.remove("bounceOutRight");
            }

        });
    }
}