// Import Styles
require( './scss/style.scss');

import 'bulma/bulma.sass';
import {UIController} from "./js/ui_controller";
import {logoutListener, addLoginListeners} from "./js/login_controllers";

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