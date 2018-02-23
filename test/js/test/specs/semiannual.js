var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Semi-annual" target frequency', function() {
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

  it('should require entering the date that first period begins', function() {
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Semi-annual target, first period start date required');
    TargetsTab.setUnitOfMeasure('Klingons per kiloton');
    TargetsTab.setLoPTarget(30);
    TargetsTab.setBaseline(31);
    TargetsTab.setTargetFrequency('Semi-annual');

    // Trying to save without setting the start date should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
    assert(errorMessage.includes('Please complete this field.'));
  });

  it('should default number of periods to 1', function() {
    assert.equal(1, TargetsTab.getNumTargetPeriods(),
      'Did not receive expected default value');
  });

  it('should create target periods for each period requested', function() {
    IndPage.createBasicIndicator();

    // This should succeed
    TargetsTab.setIndicatorName('Semi-annual target create target periods testing');
    TargetsTab.setUnitOfMeasure('Llamas per lane');
    TargetsTab.setLoPTarget(358);
    TargetsTab.setBaseline(359);
    TargetsTab.setTargetFrequency('Semi-annual');
    TargetsTab.setNumTargetPeriods(2);

    TargetsTab.saveIndicatorChanges();
    assert.equal(2, TargetsTab.getNumTargetPeriods());
  });
});
