var webdriver = require('selenium-webdriver');
var until = require('selenium-webdriver').until;
var test = require('selenium-webdriver/testing');
var assert = require('chai').assert;
var expect = require('chai').should;
var fs = require('fs');
var el;

// basic auth and session information
function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
}

async function newTolaSession(parms) {
  driver = new webdriver.Builder()
    .forBrowser(parms.browser)
    .build();
  await driver.get(parms.baseurl);
  el = await driver.getTitle();
  assert.equal(el, 'Mercy Corps Sign-On', el);
}

test.describe('TolaActivity invalid login', function() {

  var parms = readConfig();
  // inject bogus username
  parms.username = 'bubba';

  test.before(async function() {
    await newTolaSession(parms);
  });

  test.after(async function() {
    await driver.quit();
  });

  test.it('should have a Username field', async function() {
    el = await driver.findElement({name: 'login'});
    assert(el != undefined);
    await el.sendKeys(parms.username);
  });

  test.it('should have a Password field', async function() {
    el = await driver.findElement({name: 'password'});
    assert(el != undefined);
    await el.sendKeys(parms.password);
  });

  test.it('should have a Log In button', async function() {
    el = await driver.findElement({className: 'inputsub'})
    assert(el != undefined);
    await el.click();
  });

  test.it('should deny access if username is invalid', async function() {
    el = await driver.wait(until.elementLocated({id: 'error'}));
    assert(el != undefined);
    s = await el.getText();
    assert(s.startsWith('Login failed'));
  });
});
