var assert = require('chai').assert;
var expect = require('chai').expect;
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('Monthly target frequency', function() {
  before(function() {
      // Disable timeouts
      this.timeout(0);
      //browser.windowHandleMaximize();
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

  it('should require date that first target period begins', function() {
    IndPage.open();
    assert.equal('Program Indicators', IndPage.getPageName(),
      'Unexpected page name mismatch');
    IndPage.createBasicIndicator();

    // This should succeed
    TargetsTab.setIndicatorName('Annual target first period required testing');
    TargetsTab.setUnitOfMeasure('Hawks per hectare');
    TargetsTab.setLoPTarget(29);
    TargetsTab.setBaseline(30);
    TargetsTab.setTargetFrequency('Annual');

    // Trying to save without setting the start date should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetFirstPeriodErrorHint();
    expect(errorMessage.includes('Please complete this field.'));
  });

  it('should default number of periods to 1', function() {
    assert.equal(1, TargetsTab.getNumTargetPeriods(), 
      'Mismatched target period values');
  });

  it('should create target periods for each period requested', function() {
    TargetsTab.setNumTargetPeriods(12);
    TargetsTab.saveIndicatorChanges();
    assert.equal(12, TargetsTab.getNumTargetPeriods(),
      'Mismatched target period values');
  });

  it('should require entering targets for each target period', function() {
    IndPage.clickIndicatorsLink();
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Monthly target, target period value(s) required');
    TargetsTab.setUnitOfMeasure('Zebras per zoo');
    TargetsTab.setLoPTarget(57);
    TargetsTab.setBaseline(58);
    TargetsTab.setTargetFrequency('Monthly');
    TargetsTab.setNumTargetPeriods(5);
    TargetsTab.setFirstTargetPeriod();
    TargetsTab.saveIndicatorChanges();

    // Find the input boxes
    let inputBoxes = TargetsTab.getTargetInputBoxes();
    let targetCount = inputBoxes.length;
    // Place values in each box one at a time and attempt to save.
    // This should *fail* until all the fields are filled.
    let errorCount = 0;
    for(let inputBox of inputBoxes) {
      inputBox.setValue(71);
      TargetsTab.saveIndicatorChanges();
      // Did we fail successfully?
      let errMsg = TargetsTab.getTargetValueErrorHint();
      expect(errMsg.includes('Please enter a target value. Your target value can be zero.'));
      errorCount++;
    }
    assert.equal(targetCount, errorCount, 'Received unexpected error count mismatch');
    TargetsTab.saveIndicatorChanges();
  });
}); // end monthly target frequency tests

