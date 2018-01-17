// TODO: Refactor me to get rid of all the repetitive code
// TODO: Think about how to test all of the help screens
// TODO: Many of these are more fluidly, natually expressed using
// expect(...)
// TODO: Write tests for the new indicator evidence form
// TODO: What happens when we feed the textareas // the BLNS?
// TODO: Focus testing on the platform(s) most used in the field were
// Tola is deployed. What browsers and what are their priorities?
// TODO: Selecting elements by linkText is fragile.
// TODO: Didn't find suitable unique name or id selectors on // key
// elements;
// TODO: Most of these assertions are bogus
// TODO: set of tests for the edit dialog
// TODO: Much more work to do on the Indicator creation detail //
// screen
// TODO: is clicking an indicator name functionally equivalent to
// clicking its Edit button?
// TODO: Focus testing on the platform(s) most used by Tola users.
// What browsers and what are their priorities?

var webdriver = require('selenium-webdriver');
var until = require('selenium-webdriver').until;
var test = require('selenium-webdriver/testing');
var assert = require('chai').assert;
var expect = require('chai').should;
var fs = require('fs');
let el;

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};
var parms = readConfig();

var driver = new webdriver.Builder()
  .forBrowser(parms.browser)
  .build();

test.describe('TolaActivity', function() {
  test.before(function() {
    driver.get(parms.baseurl);
  });

  test.after(function() {
    driver.quit();
  });

  test.describe('Login Screen', function() {
    test.it('should require user to authenticate', function() {
      el = driver.getTitle().then(function(el) {
        assert.equal(el, 'Mercy Corps Sign-On', el);
      });
    });

    test.it('should have a login field', function() {
      el = driver.findElement({name: 'login'})
        .then(function(el) {
          el.sendKeys(parms.username);
        });
    });

    test.it('should have a password field', function() {
      el = driver.findElement({name: 'password'})
        .then(function(el) {
          el.sendKeys(parms.password);
        });
    });

    test.it('should have a Log In button', function() {
      el = driver.findElement({className: 'inputsub'})
        .then(function(el) {
          el.click();
        });
    });

    test.it('should not permit access if username is invalid');
    test.it('should not permit access if password is invalid');
  }); // end login screen tests

