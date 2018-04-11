var assert = require('chai').assert;
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Semi-annual" target frequency', function() {
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

  it('should require entering the date that first period begins', function() {
    NavBar.Indicators.click();
    assert.equal('Program Indicators', IndPage.getPageName(),
        'Unexpected page name mismatch');
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
    assert.equal(2, TargetsTab.getNumTargetPeriods(),
      'Did not find expected number of target periods');
  });
});
