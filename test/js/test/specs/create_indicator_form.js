var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;

describe('Create an Indicator form', function() {
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

  it('should exist', function() {
    IndPage.open();
    assert.equal('Program Indicators', IndPage.getPageName());
    IndPage.clickNewIndicatorButton();
    assert.equal('Create an Indicator', IndPage.getPageName());
  });

  it('should have an Indicator Service Templates dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#services');
    assert.equal(true, control.isVisible());
    TargetsTab.saveNewIndicator();
  });

  it('should have a Service Indicator dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#service_indicator');
    assert.equal(true, control.isVisible());
    TargetsTab.saveNewIndicator();
  });

  it('should have a Country dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#country');
    assert.equal(true, control.isVisible());
    TargetsTab.saveNewIndicator();
  });

  it('should have a Program dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#program');
    assert.equal(true, control.isVisible());
    TargetsTab.saveNewIndicator();
  });

  it('should have a save button', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('form').$('input[value="save"]');
    assert.equal(true, control.isVisible(),
      'Save button is not visible');
    control.click();
  });

  it('should confirm indicator created', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    TargetsTab.saveNewIndicator();
    let message = IndPage.getAlertMsg();
    expect(message.includes('Success, Basic Indicator Created!'),
      'Unexpected message during indicator creation');
  });

  it('should open Indicator detail form after clicking Save button', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    TargetsTab.saveNewIndicator();
    browser.waitForVisible('h4');
    let title = browser.$('h4').getText().trim();
    expect(title.includes('Goal indicator: Temporary'),
      'Unexpected title text on the indicator detail screen');
  });

  // Enhancements
  it('should have a Cancel button');
  it('should reset and close form when Cancel button clicked');
  it('should return to previous screen when Cancel button clicked');
  it('should have a Reset button to reset form');
}); // end create new indicator form tests
