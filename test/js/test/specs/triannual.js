var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Tri-annual" target frequency', function() {
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

  it('should require date that first target period begins', function() {
    IndPage.clickIndicatorsLink();
    TargetsTab.clickNewIndicatorButton();
    TargetsTab.saveNewIndicator();

    // This should succeed
    TargetsTab.setIndicatorName('Tri-annual target first period required testing');
    TargetsTab.setUnitOfMeasure('Hawks per hectare');
    TargetsTab.setLoPTarget(379);
    TargetsTab.setBaseline(380);
    TargetsTab.setTargetFrequency('Tri-annual');

    // Trying to save without setting the start date should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
    assert(errorMessage.includes('Please complete this field.'));
  });

  it('should default number of periods to 1', function() {
    assert.equal(1, TargetsTab.getNumTargetPeriods());
  });

  it('should create target periods for each period requested', function() {
    IndPage.clickIndicatorsLink();
    TargetsTab.clickNewIndicatorButton();
    TargetsTab.saveNewIndicator();

    // This should succeed
    TargetsTab.setIndicatorName('Tri-annual target first period required testing');
    TargetsTab.setUnitOfMeasure('Hawks per hectare');
    TargetsTab.setLoPTarget(382);
    TargetsTab.setBaseline(383);
    TargetsTab.setTargetFrequency('Tri-annual');
    TargetsTab.setNumTargetPeriods(3);
    TargetsTab.saveIndicatorChanges();
    assert.equal(3, TargetsTab.getNumTargetPeriods());
  });

  it('should require entering targets for each target period');
});
