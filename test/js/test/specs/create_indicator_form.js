var assert = require('chai').assert;
var expect = require('chai').expect;
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
var IndPage = require('../pages/indicators.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;

describe('Create an Indicator form', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
        browser.windowHandleMaximize();
    
        let parms = util.readConfig();
        LoginPage.open(parms.baseurl);
        if (parms.baseurl.includes('mercycorps.org')) {
            LoginPage.username = parms.username;
            LoginPage.password = parms.password;
            LoginPage.login.click();
        } else if (parms.baseurl.includes('localhost')) {
            LoginPage.googleplus.click();
            if (LoginPage.title != 'TolaActivity') {
                LoginPage.gUsername = parms.username + '@mercycorps.org';
                LoginPage.gPassword = parms.password;
            }
        }
    });

  it('should exist', function() {
    NavBar.Indicators.click();
    assert.equal('Program Indicators', IndPage.getPageName());
    IndPage.clickNewIndicatorButton();
    assert.equal('Create an Indicator', IndPage.getPageName());
  });

  it('should have an Indicator Service Templates dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#services');
    assert.equal(true, control.isVisible());
    IndPage.saveNewIndicator();
  });

  it('should have a Service Indicator dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#service_indicator');
    assert.equal(true, control.isVisible());
    IndPage.saveNewIndicator();
  });

  it('should have a Country dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#country');
    assert.equal(true, control.isVisible());
    IndPage.saveNewIndicator();
  });

  it('should have a Program dropdown', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    let control = $('select#program');
    assert.equal(true, control.isVisible());
    IndPage.saveNewIndicator();
  });

  it('should have a save button', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    //let control = $('form').$('input[value="save"]');
    let control = $('form[name="most"]').$('input[value="save"]');
    assert.equal(true, control.isVisible(), 'Save button is not visible');
    control.click();
  });

  it('should confirm indicator created', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    IndPage.saveNewIndicator();
    let message = IndPage.getAlertMsg();
    expect(message.includes('Success, Basic Indicator Created!'),
      'Unexpected message during indicator creation');
  });

  it('should open Indicator detail form after clicking Save button', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    IndPage.saveNewIndicator();
    browser.waitForVisible('h4');
    let title = browser.$('h4').getText().trim();
    expect(title.includes('Goal indicator: Temporary'),
      'Unexpected title text on the indicator detail screen');
  });

  it('should have a Reset button to reset form', function() {
    IndPage.clickIndicatorsLink();
    IndPage.clickNewIndicatorButton();
    IndPage.saveNewIndicator();
    let control = $('form#indicator_update_form').$('input[value="Reset"]');
    assert.equal(true, control.isVisible(), 'Reset button is not visible');
    control.click();
  });
});
