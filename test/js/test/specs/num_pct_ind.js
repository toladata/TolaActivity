import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
import { expect } from 'chai';
'use strict';

/**
 * General number and percentage indicator tests
 * Tests from mc/issues/114, mc/issues/117, ms/issues/144
 */
describe('Number indicators config and display', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
        browser.windowHandleMaximize();
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

    it('should allow to set percentage indicators', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.setMeasureType('percent');
        let indType = TargetsTab.getMeasureType();
        expect(indType == 1);
    });

    it('should default to number indicators', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        let indType = TargetsTab.getMeasureType();
        expect(indType == 0);
    });

    it('should default number indicators to non-cumulative indicators', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setMeasureType('number');
        let indType = TargetsTab.getMeasureType();
        expect(indType == 1);
        TargetsTab.setUnitOfMeasure('castles');
        TargetsTab.setLoPTarget(60);
        TargetsTab.setBaseline(61);
        TargetsTab.setTargetFrequency('annual');
        TargetsTab.setFirstTargetPeriod();
        TargetsTab.saveChanges();
        expect(false == TargetsTab.getMeasureIsCumulative());
    });

    it('should default percentage indicators to cumulative indicators', function() {
        NavBar.Indicators.click();
        IndPage.createBasicIndicator();
        TargetsTab.clickTargetsTab();
        TargetsTab.setMeasureType('percent');
        let indType = TargetsTab.getMeasureType();
        expect(indType == 2);
        expect(true == TargetsTab.getMeasureIsCumulative());

    });

    it('should add “%” to LoP target and Baseline text boxes');

    it('should have direction of change option', function() {
        expect(TargetsTab.getDirectionOfChange() != undefined);
        expect(TargetsTab.getDirectionOfChange() != null);
    });

    it('should default to no direction of change', function() {
        expect(TargetsTab.getDirectionOfChange() == 'none');
    });
});
