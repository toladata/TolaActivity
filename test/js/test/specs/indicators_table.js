var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

describe('Program Indicators table', function() {
  before(function() {
    // Disable timeouts
    this.timeout(0);
    browser.windowHandleMaximize();

    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
  });

  // FIXME: Still need to get WebDriver code out of this test
  it('should toggle table when a PI Indicators button is clicked', function() {
    IndPage.open();
    if(browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', delay, true);
    }
    IndPage.clickIndicatorsLink();
    let buttons = TargetsTab.getProgramIndicatorButtons();
    for (let button of buttons) {
      let targetDiv = 'div' + button.getAttribute('data-target');
      let isVisible = browser.isVisible(targetDiv);
      // Starts out collapsed
      assert.equal(false, isVisible);

      // Open it and verify
      button.click();
      if(browser.isVisible('div#ajaxloading')) {
        browser.waitForVisible('div#ajaxloading', delay, true);
      }
      isVisible = browser.isVisible(targetDiv);
      assert.equal(true, isVisible);

      // Close it and verify
      button.click();
      if(browser.isVisible('div#ajaxloading')) {
        browser.waitForVisible('div#ajaxloading', delay, true);
      }
      isVisible = browser.isVisible(targetDiv);
      assert.equal(true, isVisible);
    }
  });

  it('should show a detail screen when an indicator name is clicked', function() {
    if (browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', delay, true);
    }
    IndPage.clickIndicatorsLink();
    // Make list of Indicators buttons
    let buttons = TargetsTab.getProgramIndicatorButtons();
    // Click the first one to expand the table
    let button = buttons[0];
    button.click();
    // Make list of indicator names in resulting table
    // FIXME: needs to be from table, not dropdown
    let indicatorNameList = IndPage.getIndicatorsDropdownList();
    // Click the first one
    if (browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', delay, true);
    }
    let indicatorName = indicatorNameList[0];
    TargetsTab.clickProgramIndicatorsButton(indicatorName);
  });

  it('should be able to create PI by clicking the New Indicator button', function() {
    TargetsTab.clickNewIndicatorButton();
    TargetsTab.saveNewIndicator();
    TargetsTab.setIndicatorName('New Indicator button test');
    TargetsTab.setUnitOfMeasure('Bugs fixed');
    TargetsTab.setLoPTarget(172);
    TargetsTab.setBaseline(173);
    TargetsTab.setTargetFrequency('Life of Program (LoP) only');
    TargetsTab.saveIndicatorChanges();
  });

  it('should increase PI count after adding new indicator', function() {
    TargetsTab.createBasicIndicator();
  });
  it('should be able to delete PI by clicking its Delete button');
  it('should decrease PI count after deleting indicator');
  it('should be able to edit PI by clicking its Edit button');
  it('should open the Grid/Print Report page when button is clicked');

  // These are enhancements
  it('should highlight PIs with no evidence');
  it('should disable Indicators button if program has no indicators');
  it('should be able to sort table by clicking a column header');
  it('should be able to select any/all list items');
  it('should be able to filter the resultset by Indicator Type');
});
