var assert = require('chai').assert;
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

  describe('Collected Data form', function() {
    it('should exist');
    it('should require required fields');
    it('should not require optional fields');
    it('should validate input data before saving it');
    it('should not save invalid input data');
    it('should have a Reset button');
    it('should clear the form by clicking the Reset button');
    it('should restore the form defaults by clicking the Reset button');
    it('should open the Indicator edit form by clicking the Add a Disaggregation link');
    it('should only accept numeric values in the disaggregations Actuals fields');
    it('should have a cancel button');
    it('should be able to close the form by clicking the Cancel button');
  });
});
