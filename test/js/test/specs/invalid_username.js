var assert = require('assert');
var fs = require('fs');

// basic auth and session information
function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
}
var parms = readConfig();

describe('TolaActivity invalid username login', function() {
  // inject bogus username
  parms.username = 'HorseWithNoName';

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
    var button = $('.inputsub');
    button.click();
  });

  it('should deny access if password is invalid', function() {
    browser.waitUntil(function() {
      return browser.getText('#error').startsWith('Login failed:');
      }, 5000, 'expected login failure message');
  });
});
