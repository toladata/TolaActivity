import { assert, expect } from 'chai';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('Midline and endline target frequency', function() {
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

  it('should require value in Midline target field', function() {
    NavBar.Indicators.click();
    expect('Program Indicators' == IndPage.getPageName());
    IndPage.createBasicIndicator();
 
    // This should succeed
    TargetsTab.setIndicatorName('Midline target required testing');
    TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
    TargetsTab.setLoPTarget(38);
    TargetsTab.setBaseline(39);
    TargetsTab.setTargetFrequency('Midline and endline');
    TargetsTab.saveIndicatorChanges();
 
    // This should fail without midline target
    TargetsTab.setEndlineTarget(44);
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetValueErrorHint();
    assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
 
  });
 
  it('should require value in Endline target field', function() {
    NavBar.Indicators.click();
    IndPage.createBasicIndicator();
 
    // This should succeed
    TargetsTab.setIndicatorName('Endline target required testing');
    TargetsTab.setUnitOfMeasure('Gargoyles per gable');
    TargetsTab.setLoPTarget(57);
    TargetsTab.setBaseline(58);
    TargetsTab.setTargetFrequency('Midline and endline');
    TargetsTab.saveIndicatorChanges();
 
    // This should fail without endline target
    TargetsTab.setMidlineTarget(63);
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetValueErrorHint();
    assert(errorMessage.includes('Please enter a target value. Your target value can be zero.'));
  });
});
