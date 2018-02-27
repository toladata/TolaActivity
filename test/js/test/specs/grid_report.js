var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

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
    // FIXME: pageName should be a property
    IndPage.open();
    assert.equal('Program Indicators', IndPage.pageName());
  });

  it('should have a Grid/Print Report button');
  it('should open when the Grid/Print Report button is clicked');
  it('should have an Export All button');
  it('should export all report entries when Export All button is clicked');
});
