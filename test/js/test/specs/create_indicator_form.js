var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

describe('Program Indicators page', function() {
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
    // FIXME: pageName should be a property
    assert.equal('Program Indicators', IndPage.pageName());
  });

  describe('Create an Indicator form', function() {
    it('should show context-sensitve help by clicking Form Help/Guidance button');
    it('should have an Indicator Service Templates dropdown');
    it('should have a Custom entry in the Indicator Service Templates dropdown');
    it('should have a Service Indicator dropdown');
    it('should have a Country dropdown');
    it('should have a Program dropdown');
    it('should have a Save button');
    it('should confirm indicator created')
    it('should open Indicator detail form after clicking Save button');
    it('should have a Cancel button');
    it('should reset and close form when Cancel button clicked');
    it('should return to previous screen when Cancel button clicked');
    it('should have a Reset button to reset form');
    it('should have a Help link');
    it('should have a Save Changes button');
    it('should have a Reset button');
    it('should have a Cancel button');
    it('should trigger cancel action by pressing Escape key');
    it('should validate input data after clicking Save Changes button');
    it('should validate input data before committing it');
    it('should restore form to pre-edit state when Reset button is clicked');
  }); // end create new indicator form tests
});
