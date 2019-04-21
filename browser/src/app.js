// Import Styles
require( './scss/my_sexy_style.scss');
import 'bulma/bulma.sass'

// Wait for main content to load
document.addEventListener("DOMContentLoaded", event => {
    try {
        let app = firebase.app();
        //let features = ['auth', 'database', 'messaging', 'storage'].filter(feature => typeof app[feature] === 'function');
        //document.getElementById('load').innerHTML = `Firebase SDK loaded with ${features.join(', ')}`;
        app.auth().onAuthStateChanged(function (user) {
            if (user) {
                console.log("User is signed in" + user.displayName);
            } else {
                console.log("Not Signed in");
            }

        });
    } catch (e) {
        console.error(e);
        //document.getElementById('load').innerHTML = 'Error loading the Firebase SDK, check the console.';
    }

    addEventListeners();
});

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