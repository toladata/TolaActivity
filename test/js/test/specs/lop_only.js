var assert = require('chai').assert;
import LoginPage from '../pages/login.page';
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Life of Program (LoP) only" target frequency', function() {
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

  it('should permit only numeric values for LoP target', function() {
    IndPage.open();
    assert.equal('Program Indicators', IndPage.getPageName(),
      'Unexpected page name mismatch');
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('LoP only target testing');
    TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
    TargetsTab.setLoPTarget(30);
    TargetsTab.setBaseline(31);
    TargetsTab.setTargetFrequency('Life of Program (LoP) only');
    // This should succeed
    TargetsTab.saveIndicatorChanges();
  });

  it('should reject non-numeric values for LoP target', function() {
    TargetsTab.setLoPTarget('"666"');
    // This should fail
    TargetsTab.saveIndicatorChanges();
    let errorHint = TargetsTab.getLoPErrorHint();
    assert(errorHint.includes('Please enter a number larger than zero'),
      'Did not receive expected failure message');
    // Make it numeric; this should succeed
    TargetsTab.setLoPTarget(45);
    TargetsTab.saveIndicatorChanges();
    assert.equal(45,
      TargetsTab.getLoPTarget(),
      'Did not receive expected value from getLoPTarget()');
  });
});
