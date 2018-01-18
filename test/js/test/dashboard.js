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
    
async function newTolaSession(parms) {
  driver = new webdriver.Builder()
  .forBrowser(parms.browser)
  .build();
  await driver.get(parms.baseurl);
  el = await driver.getTitle();
  assert.equal(el, 'Mercy Corps Sign-On', el);
}

async function newTolaLogin(parms) {
  el = await driver.findElement({name: 'login'});
  await el.sendKeys(parms.username);

  el = await driver.findElement({name: 'password'});
  await el.sendKeys(parms.password);

  el = await driver.findElement({className: 'inputsub'})
  await el.click();
}

test.describe('TolaActivity Dashboard', async function() {
  var parms = readConfig();

  test.before(async function() {
    await newTolaSession(parms);
  });

  test.after(async function() {
    await driver.quit();
  });

  test.it('should require login authentication', async function() {
    await newTolaLogin(parms);
  });

  test.it('should exist'), async function() {
    el = await driver.findElement({className: 'a.navbar-brand'});
    assert(await el.click());
  }

  test.it('should have page header', async function() {
    el = await driver.wait(until.elementLocated({css: 'h4'}));
    assert(el.getText(), 'Tola-Activity Dashboard');
  });

  test.it('should have a TolaActivity link', async function() {
    let xp = '/html/body/nav/div/div[1]/a/img';
    el = await driver.findElement({xpath: xp});
    assert(await el.click());
  });
  test.it.skip('should have a Country Dashboard dropdown', async function() {
    el = driver.findElement({id: 'dropDownMenu1'});
    assert(await el.click());
  });

  test.it('should have a Filter by Program link', async function() {
    el = driver.findElement({id: 'dropdownMenu3'});
    assert(await el.click());
  });

  test.it('should have a Workflow dropdown', async function() {
    let xp = '/html/body/nav/div/div[2]/ul[1]/li[1]/a';
    el = driver.findElement({xpath: xp}).then(function(el) {
      assert(el.click());
    });
  });

  test.it('should have a Form Library dropdown', async function() {
    el = driver.findElement({linkText: 'Form Library'})
      .then(function(el) {
        assert(el.click());
      });
  });
  
  test.it('should have a Reports link', async function() {
    el = driver.findElement({linkText: 'Reports'})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.it.skip('should have a Profile link', async function() {
    let xp = '/html/body/nav/div/div[2]/ul[2]/li[1]/a';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.it('should have a Bookmarks link', async function() {
    let xp = '/html/body/nav/div/div[2]/ul[2]/li[2]/a';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.describe.skip('Indicator Evidence panel', async function() {
    test.it.skip('should be present on dashboard', async function() {
      el = await driver.findElement({linkText: 'Indicator Evidence'});
      return el;
    });
  }); // end indicator evidence panel tests

  test.describe('Strategic Objectives panel', async function() {
    test.it('should exist');
  }); // end strategic objectives panel tests

  test.describe('Sites panel', async function() {
    test.it('should exist');
    test.it('should show map of country selected in Country Dashboard dropdown');
    test.it('should be able to zoom in on the map');
    test.it('should be able to zoom out on the map');
    test.it('should display data points on the Sites map');
  }); // end sites panel tests

  test.describe('Program Projects by Status panel', async function() {
    test.it('should exist');
    test.it('should have a project status chart');
  }); // end program projects by status tests

  test.describe('Indicators performance panel', async function() {
    test.it('should exist');
    test.it('should have a KPI status chart');
  }); // end indicators performance panel tests
});
