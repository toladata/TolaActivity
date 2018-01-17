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

test.describe('TolaActivity Dashboard', function() {
  test.before(function() {
    driver.get(parms.baseurl);
  });

  test.after(function() {
    driver.quit();
  });

  test.it('should have a page title', function() {
    el = driver.getTitle().then(function(el) {
      assert.equal(el, 'TolaActivity', el);
    });
  });

  test.it('should have a TolaActivity link', function() {
    let xp = '/html/body/nav/div/div[1]/a/img';
    el = driver.findElement({xpath: xp}).then(function(el) {
      assert(el.click());
    });
  });
  
  // TODO: file enhancement request about the id dropdownMenu1
  test.it('should have a Country Dashboard dropdown', function() {
    let xp = '/html/body/div[1]/div[3]/div/div/div[2]/div/div[1]';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  // TODO: file enhancement request about the id dropdownMenu3
  test.it('should have a Filter by Program link', function() {
    let xp = '/html/body/div[1]/div[3]/div/div/div[2]/div/div[2]';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.it('should have a Workflow dropdown', function() {
    let xp = '/html/body/nav/div/div[2]/ul[1]/li[1]/a';
    el = driver.findElement({xpath: xp}).then(function(el) {
      assert(el.click());
    });
  });

  test.it('should have a Form Library dropdown', function() {
    el = driver.findElement({linkText: 'Form Library'})
      .then(function(el) {
        assert(el.click());
      });
  });
  
  test.it('should have a Reports link', function() {
    el = driver.findElement({linkText: 'Reports'})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.it.skip('should have a Profile link', function() {
    let xp = '/html/body/nav/div/div[2]/ul[2]/li[1]/a';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.it('should have a Bookmarks link', function() {
    let xp = '/html/body/nav/div/div[2]/ul[2]/li[2]/a';
    el = driver.findElement({xpath: xp})
      .then(function(el) {
        assert(el.click());
      });
  });

  test.describe('Indicator Evidence panel', function() {
    test.it('should be present on dashboard', async function() {
      el = await driver.findElement({linkText: 'Indicator Evidence'});
      return el;
    });
  }); // end indicator evidence panel tests

  test.describe('Strategic Objectives panel', function() {
    test.it('should exist');
  }); // end strategic objectives panel tests

  test.describe('Sites panel', function() {
    test.it('should exist');
    test.it('should show map of country selected in Country Dashboard dropdown');
    test.it('should be able to zoom in on the map');
    test.it('should be able to zoom out on the map');
    test.it('should display data points on the Sites map');
  }); // end sites panel tests

  test.describe('Program Projects by Status panel', function() {
    test.it('should exist');
    test.it('should have a project status chart');
  }); // end program projects by status tests

  test.describe('Indicators performance panel', function() {
    test.it('should exist');
    test.it('should have a KPI status chart');
  }); // end indicators performance panel tests
});
