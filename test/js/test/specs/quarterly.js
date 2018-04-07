var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('Quarterly target frequency', function() {
  before(function() {
    // Disable timeouts
    this.timeout(0);
    browser.windowHandleMaximize();
  });

  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUsername(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    assert.equal('Program Indicators', IndPage.getPageName(),
     'Unexpected page name mismatch');
  });

  it('should require date that first target period begins', function() {
    IndPage.createBasicIndicator();
    TargetsTab.setIndicatorName('Quarterly target first period required testing');
    TargetsTab.setUnitOfMeasure('Hawks per hectare');
    TargetsTab.setLoPTarget(31);
    TargetsTab.setBaseline(32);
    TargetsTab.setTargetFrequency('Quarterly');

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
    IndPage.createBasicIndicator();

    // This should succeed
    TargetsTab.setIndicatorName('Quarterly target create target periods testing');
    TargetsTab.setUnitOfMeasure('Irritants per island');
    TargetsTab.setLoPTarget(49);
    TargetsTab.setBaseline(50);
    TargetsTab.setTargetFrequency('Quarterly');

    TargetsTab.setNumTargetPeriods(4);
    TargetsTab.saveIndicatorChanges();
    assert.equal(4, TargetsTab.getNumTargetPeriods());
  });

  it('should require entering targets for each target period', function() {
    IndPage.clickIndicatorsLink();
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Quarterly target, target period value(s) required');
    TargetsTab.setUnitOfMeasure('Weekends per worker');
    TargetsTab.setLoPTarget(65);
    TargetsTab.setBaseline(66);
    TargetsTab.setTargetFrequency('Quarterly');
    TargetsTab.setNumTargetPeriods(4);
    TargetsTab.setFirstTargetPeriod();
    TargetsTab.saveIndicatorChanges();

    // Find the input boxes
    let inputBoxes = TargetsTab.getTargetInputBoxes();
    let targetCount = inputBoxes.length;
    // Place values in each box one at a time and attempt to save.
    // This should *fail* until all the fields are filled.
    let errorCount = 0;
    for(let inputBox of inputBoxes) {
      inputBox.setValue(86);
      TargetsTab.saveIndicatorChanges();
      // Did we fail successfully?
      let errMsg = TargetsTab.getTargetValueErrorHint();
      expect(errMsg.includes('Please enter a target value. Your target value can be zero.'));
      errorCount++;
    }
    assert.equal(targetCount, errorCount, 'Received unexpected error count mismatch');
    TargetsTab.saveIndicatorChanges();
  });
}); // end quarterly target tests
