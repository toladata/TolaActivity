var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;

describe('Grid/Print Report page', function() {
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
    assert.equal('Program Indicators', IndPage.getPageName());
  });

  it('should have a Grid/Print Report button', function() {
    let progList = IndPage.getProgramsDropdownList();
    let prog = progList[1];
    IndPage.selectProgram(prog);
    assert(browser.isVisible('=Grid/Print Report'));
  });

  it('should open when the Grid/Print Report button is clicked', function() {
    IndPage.clickIndicatorsLink();
    let progList = IndPage.getProgramsDropdownList();
    let prog = progList[1];
    IndPage.selectProgram(prog);
    browser.$('=Grid/Print Report').click();
    let pageTitle = IndPage.getPageName();
    assert(pageTitle.includes('Indicator Print/Grid Report'), 
      'Did not receive expected report page title');
  });

  it('should have an Export All button', function() {
    IndPage.clickIndicatorsLink();
    let progList = IndPage.getProgramsDropdownList();
    let prog = progList[1];
    IndPage.selectProgram(prog);
    browser.$('=Grid/Print Report').click();

    // Scroll to the bottom of the page
    browser.scroll('div#footer');
    let button = browser.$('button[type="submit"]');
    let text = button.getText();
    assert(text.includes('Export All'), 'Did not find expected button text');
  });

  it('should export all report entries when Export All button is clicked');
});
