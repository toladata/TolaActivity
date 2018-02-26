var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

describe('Program Indicators landing page', function() {
  before(function() {
    // Disable timeouts
    this.timeout(0);
    browser.windowHandleMaximize();
  });

  it('should exist', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    // FIXME: pageName should be a property
    assert.equal('Program Indicators', IndPage.pageName());
  });

  it('should be present on page', function() {
    if (browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', delay, true);
    }
    IndPage.clickProgramsDropdown();
    IndPage.clickProgramsDropdown();
  });

  it('should have same number of items as the Programs table', function() {
    let progList = IndPage.getProgramsDropdownList();
    let progTable = IndPage.getProgramsTable();
    assert.equal(progList.length, progTable.length, 'row count mismatch');
  });

  it('should have same items as Programs table', function() {
    let progList = IndPage.getProgramsDropdownList();
    let listItems = new Array();
    for (let prog of progList) {
      let name = prog.split('-')[1].trim();
      listItems.push(name);
    }

    let progTable = IndPage.getProgramsTable();
    for (let i = 0; i < progTable.length; i++) {
      let rowText = progTable[i].split('\n')[0].trim();
      assert.equal(rowText, listItems[i]);
    };
  });

  // FIXME: Doesn't assert anything
  it('should filter programs table by selected program name', function() {
    let selectList = browser.$('select#id_programs_filter_dropdown');
    let progTable = selectList.$$('options');
    for (let listItem of progTable) {
      let s = listItem.getText();
      if (! s.includes('-- All --')) {
        browser.selectByVisibleText(s);
      }
    }
  }); // end programs dropdown tests

  describe('Indicators dropdown', function() {
    it('should be present on page', function() {
      IndPage.clickIndicatorsDropdown();
    });

    it('should have at least one entry', function() {
      let indList = IndPage.getIndicatorsDropdownList();
      assert(indList.length > 0);
    });
  }); // end indicators dropdown tests

  describe('Indicator Type dropdown', function() {
    it('should be present on page', function() {
      IndPage.clickIndicatorTypeDropdown();
    });

    it('should have at least one entry', function() {
      let indTypeList = IndPage.getIndicatorTypeList();
      assert(indTypeList.length > 0);
    });
  }); // end indicator type dropdown tests

  // FIXME: Still need to get WebDriver code out of this test
  // FIXME: Make sure this actually tests/asserts something
  it('should toggle PIs table by clicking PI Indicators button', function() {
    IndPage.clickIndicatorsLink();
    if(browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', delay, true);
    }
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

      button.click();
      if(browser.isVisible('div#ajaxloading')) {
        browser.waitForVisible('div#ajaxloading', delay, true);
      }
    }
  });

  // FIXME: Still need to get WebDriver code out of this test
  it('should have matching indicator counts on data button and in table', function() {
    IndPage.clickIndicatorsLink();
    let buttons = TargetsTab.getProgramIndicatorButtons();
    for (let button of buttons) {
      button.scroll();
      button.click();
      let buttonCnt = parseInt(button.getText());
      let targetId = button.getAttribute('data-target');
      let tableCnt = IndPage.getProgramIndicatorsTableCount(targetId);
      assert.equal(buttonCnt, tableCnt, "Indicator count mismatch");
    }
  }); // Try this flaky test up to 3 times before failing
});
