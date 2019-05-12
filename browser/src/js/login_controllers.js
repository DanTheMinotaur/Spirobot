/**
 * Add Listener events for login screen
 */
export function addLoginListeners() {
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
 * Loads Google Login Popup
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

/**
 * Handles user login via email
 * @param email
 * @param password
 */
function loginEmail(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password).catch((error) => {
        console.log("Could Not Login: ", error);
        displayLoginError(error);
    });
}

/**
 * Handles and displays login errors for user
 * @param error the firebase error response
 */
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
export function logoutListener(app, firebaseAuth) {
    document.getElementById("logout").addEventListener("click", () => {
        firebaseAuth.signOut();
    })
}