var assert = require('assert');
var fs = require('fs');

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
}
var parms = readConfig();

describe('TolaActivity Login screen', function() {

  it('should require user to authenticate', function() {
    browser.url(parms.baseurl);
    var title = browser.getTitle();
    assert.equal(title, 'Mercy Corps Sign-On');
  });

  it('should have a login field', function() {
    var login = $('#login');
    login.setValue(parms.username);
  });

  it('should have a password field', function() {
    var password = $('#password');
    password.setValue(parms.password);
  });

  it('should have a Log In button', function() {
    button = $('.inputsub');
    button.click();
  });

});

