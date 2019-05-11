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
                // serviceWorkingPermission();
                console.log("User is signed in" + user.photoURL);
                appJS.innerHTML = adminTemplate(user);

                //const bot = new BotController(app);
                const ui = new UIController(app);

                logoutListener(appJS, app.auth());

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
    let googleLogin = document.getElementById("googleLogin");
    googleLogin.addEventListener("click", (event) => {
        event.preventDefault();
        loginGoogle();
    })
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

function logoutListener(app, firebaseAuth) {
    document.getElementById("logout").addEventListener("click", () => {
        firebaseAuth.signOut().then(() => {
            app.innerHTML = loginTemplate({});
        });
    })
}


// function serviceWorkingPermission() {
//     if ("serviceWorker" in navigator) {
//         navigator.serviceWorker
//             .register("./firebase-messaging-sw.js")
//             .then(function(registration) {
//                 console.log("Registration successful, scope is:", registration.scope);
//             })
//             .catch(function(err) {
//                 console.log("Service worker registration failed, error:", err);
//             });
//     }
// }