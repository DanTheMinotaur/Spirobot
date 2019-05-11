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
        let title_name = document.title;

        // Check if user is logged in.
        app.auth().onAuthStateChanged(function (user) {
            if (user) {
                document.title = "Welcome " + title_name;
                appJS.innerHTML = adminTemplate(user);

                const ui = new UIController(app);

                logoutListener(appJS, app.auth());

            } else {
                document.title = "Login " + title_name;
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
    });
    let emailLogin = document.getElementById("emailLogin");
    emailLogin.addEventListener("click", (event) => {
       event.preventDefault();
       let email = document.getElementById("emailInput");
       let password = document.getElementById("passwordInput");
       loginEmail(email.value, password.value);
    });
}

/**
 * Loads Login Popup window
 */
function loginGoogle() {
    const provider = new firebase.auth.GoogleAuthProvider();

    firebase.auth().signInWithPopup(provider).then(loginResult => {
        const user = loginResult.user;  // User Auth Successful
        console.log(user);
    }).catch((error) => {
        console.log("Could Not Login: ", error); // Log Error
        displayLoginError(error);
    });
}

function loginEmail(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password).catch((error) => {
        console.log("Could Not Login: ", error);
        displayLoginError(error);
    });
}

function displayLoginError(error) {

    let loginErrorDisplay = document.getElementById("loginError");
        document.getElementById("closeLoginError").addEventListener("click", () => {
            loginErrorDisplay.style.display = "none";
    });
    let header = loginErrorDisplay.getElementsByTagName("p")[0];
    let body = loginErrorDisplay.getElementsByClassName("message-body")[0];
    if (error.code === "auth/user-not-found") {
        header.innerHTML = "No Account Found for User";
    } else if (error.code === "auth/wrong-password") {
        header.innerHTML = "Wrong Password";
    } else {
        header.innerHTML = "Login Error";
    }
    body.innerHTML = error.message;
    loginErrorDisplay.style.display = "block";
}

/**
 * Function for adding logout events to browser if a user is logged in.
 * @param app Firebase app object
 * @param firebaseAuth Firebase Auth Object.
 */
function logoutListener(app, firebaseAuth) {
    document.getElementById("logout").addEventListener("click", () => {
        firebaseAuth.signOut().then(() => {
            app.innerHTML = loginTemplate({});
        });
    })
}