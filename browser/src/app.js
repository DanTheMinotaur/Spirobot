// Import Styles
require( './scss/style.scss');

import 'bulma/bulma.sass'
import {createJoystick} from './js/joystick';

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

                const bot = new BotController(app);
                const joystick = createJoystick(document.getElementById("joystick"));
                setInterval(() => console.log(joystick.getPosition()), 16);

                bot.move("forward");


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
 * Class for controlling bot functionality using firebase live Database
 * @constructor Firebase Instance
 */
class BotController{
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