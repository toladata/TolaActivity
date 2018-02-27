var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

describe('Indicator creation detail form', function() {
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
    assert.equal('Program Indicators', IndPage.pageName());

    IndPage.createBasicIndicator();
    browser.waitForVisible('h4');
    let title = browser.$('h4').getText().trim();
    expect(title.includes('Goal indicator: Temporary'),
      'Unexpected title text on the indicator detail screen');
  });

  describe('Summary tab', function() {
    it('should exist', function() {
        expect(browser.isVisible('=Summary')); 
    });
    it('should have Program field matching input data');
  }); // end summary tab tests

  describe('Performance tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Performance')); 
    });
  }); // end performance tab tests

  describe('Targets tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Targets')); 
    });
  }); // end targets tab tests

  describe('Data Acquisition tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Data Acquisition')); 
    });
  }); // end data acquistion tab tests

  describe('Analysis and Reporting tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Analysis and Reporting')); 
    });
  }); // end analysis tab tests

  describe('Approval tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Approval')); 
    });
  }); // end approval tab tests

  it('should have a Help link');
  it('should have a Save Changes button');
  it('should have a Reset button');
  it('should have a Cancel button');
  it('should trigger cancel action by pressing Escape key');
  it('should restore form to pre-edit state when Reset button is clicked');

}); // end create indicator detail page tests
