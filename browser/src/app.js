// Import Styles
require( './scss/my_sexy_style.scss');
import 'bulma/bulma.sass'
const loginTemplate = require('./js/login.html.handlebars');
const adminTemplate = require('./js/control-panel.html.handlebars');

// Wait for main content to load
document.addEventListener("DOMContentLoaded", event => {
    const appJS = document.getElementById("app");
    try {
        let app = firebase.app();
        app.auth().onAuthStateChanged(function (user) {
            if (user) {
                console.log("User is signed in" + user.displayName);
                console.log(adminTemplate);
                appJS.innerHTML = adminTemplate(user);
            } else {
                console.log("Not Signed in");
                appJS.innerHTML = loginTemplate({});
            }

        });
    } catch (e) {
        console.error(e);
    }

    addEventListeners();
});

function handlebarsCompiler(template, data) {
    let compiledTemplate = Handlebars.compile(template);
    return compiledTemplate(data);
}

function addEventListeners() {
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
        document.getElementById("display-name").innerText = user.displayName;
        document.write(user);
    }).catch(e => {
        console.log(e); // Log Error
    });
}