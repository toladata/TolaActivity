var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Midline and endline" target frequency', function() {
  // Disable timeouts
  this.timeout(0);
  browser.windowHandleMaximize();

  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    assert.equal('Program Indicators', IndPage.pageName(),
      'Unexpected page name mismatch');
  });

  it('should require value in Midline target field', function() {
    IndPage.createBasicIndicator();
 
    // This shold succeed
    TargetsTab.setIndicatorName('Midline target required testing');
    TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
    TargetsTab.setLoPTarget(228);
    TargetsTab.setBaseline(229);
    TargetsTab.setTargetFrequency('Midline and endline');
    TargetsTab.saveIndicatorChanges();
 
    // This should fail without midline target
    TargetsTab.setEndlineTarget(234);
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetValueErrorHint();
    assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
 
  });
 
  it('should require value in Endline target field', function() {
    IndPage.createBasicIndicator();
 
    // This should succeed
    TargetsTab.setIndicatorName('Endline target required testing');
    TargetsTab.setUnitOfMeasure('Gargoyles per parapet');
    TargetsTab.setLoPTarget(249);
    TargetsTab.setBaseline(250);
    TargetsTab.setTargetFrequency('Midline and endline');
    TargetsTab.saveIndicatorChanges();
 
    // This should fail without endline target
    TargetsTab.setMidlineTarget(255);
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetValueErrorHint();
    assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
  });
});
