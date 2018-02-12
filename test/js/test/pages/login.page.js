/**
 * Page model and methods for testing the login page
 * @module pages/login
 */

/** Opens a browser window and navigates to the requested URL
 * @param {string} url - The URL to which to navigate
 * @returns Nothing
 */
function open(url) {
  browser.url(url);
}

/** Types the specified username into the username text box
 * @param {string} username - The login name to use
 * @returns Nothing
 */
function setUserName(username) {
  let loginBox = $('#login');
  loginBox.setValue(username);
}

/** Types the specified password into the password text box
 * @param {string} password - The password to use
 * @returns Nothing
 */
function setPassword(password) {
  let passwordBox = $('#password');
  passwordBox.setValue(password);
}

/** Clicks the login button on the sign-in page
 * @returns Nothing
 */
function clickLoginButton() {
  let loginButton = $('.inputsub');
  loginButton.click();
}

exports.open = open;
exports.setUserName = setUserName;
exports.setPassword = setPassword;
exports.clickLoginButton = clickLoginButton;
