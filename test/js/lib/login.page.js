// login.page.js -- Page model and methods for login page
// for use in testing
function openLoginPage(url) {
  browser.url(url);
}

function setUserName(username) {
  let loginBox = $('#login');
  loginBox.setValue(username);
}

function setPassword(password) {
  let passwordBox = $('#password');
  passwordBox.setValue(password);
}

function clickLoginButton() {
  let loginButton = $('.inputsub');
  loginButton.click();
}

exports.openLoginPage = openLoginPage;
exports.setUserName = setUserName;
exports.setPassword = setPassword;
exports.clickLoginButton = clickLoginButton;
