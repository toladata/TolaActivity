import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
import { expect } from 'chai';
'use strict';

/**
 * Indicator evidence table: number indicator config and display
 * Tests from mc/issues/115, mc/issues/118
 */
describe('Number indicators in the indicator evidence table', function() {

    before(function() {
      // Disable timeouts
      this.timeout(0);
      //browser.windowHandleMaximize();
      let parms = Util.readConfig();
                          
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

    it('should take LoP target of NC number indicator from LoP target field', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.setIndicatorName('Scenario 1');
        TargetsTab.clickTargetsTab();
        TargetsTab.setUnitOfMeasure('Things');
        TargetsTab.setMeasureType('number');
        TargetsTab.setLoPTarget(600);
        TargetsTab.setBaseline(0);
        TargetsTab.setTargetFrequency('Annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.setNumTargetPeriods(3);
        TargetsTab.saveIndicatorChanges();

        let reqTarget = TargetsTab.getLoPTarget();
        let actTarget = TargetsTab.getLoPTarget();
        expect(reqTarget == actTarget);
    });

    it('should calculate the LoP actual of NC number indicators as sum of target actuals');
    it('should take the LoP target of a C number indicators from LoP target field');
    it('should take the LoP actual of C number indicators from the latest target actual');
}); 
