'use strict';
var webdriver = require('selenium-webdriver');
var test = require('selenium-webdriver/testing');
var until = require('selenium-webdriver').until;
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

test.describe('TolaActivity Login screen', function() {
  test.before(function() {
    driver.get(parms.baseurl);
  });

  test.after(function() {
    driver.quit();
  });

  test.it('should require user to authenticate', async function() {
    el = await driver.getTitle().then(function(el) {
      assert.equal(el, 'Mercy Corps Sign-On', el);
    });
  });

  test.it('should have a login field', async function() {
    el = await driver.findElement({name: 'login'});
    el.sendKeys(parms.username);
  });

  test.it('should have a password field', async function() {
    el = await driver.findElement({name: 'password'});
    el.sendKeys(parms.password);
  });

  test.it('should have a Log In button', async function() {
    el = await driver.findElement({className: 'inputsub'});
    await el.click();
  });
}); // end login screen
