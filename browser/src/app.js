// Import Styles
require( './scss/style.scss');

import 'bulma/bulma.sass';
import {UIController} from "./js/ui_controller";

const loginTemplate = require('./templates/login.html.handlebars');
const adminTemplate = require('./templates/control-panel.html.handlebars');

// Wait for main content to load
document.addEventListener("DOMContentLoaded", event => {
    const appJS = document.getElementById("app");
    try {
        let app = firebase.app();

        // Check if user is logged in.
        app.auth().onAuthStateChanged(function (user) {
            if (user) {
                console.log("User is signed in" + user.photoURL);
                appJS.innerHTML = adminTemplate(user);

                //const bot = new BotController(app);
                const ui = new UIController(app);
                ui.setListeners();
                ui.notificationAlert("Test", "Hello");

            } else {
                console.log("Not Signed in");
                appJS.innerHTML = loginTemplate({});
                addLoginListeners();
            }
        });
    } catch (e) {
        console.error(e);
    }
});

/**
 * Add Listener events for login screen
 */
function addLoginListeners() {
    document.getElementById("googleLogin").addEventListener("click", loginGoogle);
}

/**
 * Loads Login Popup window
 */
function loginGoogle() {
    const provider = new firebase.auth.GoogleAuthProvider();

    firebase.auth().signInWithPopup(provider).then(loginResult => {
        const user = loginResult.user;  // User Auth Successful
        console.log(user);
    }).catch(e => {
        console.log(e); // Log Error
    });
}