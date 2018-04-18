import LoginPage from '../pages/login.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import NavBar from '../pages/navbar.page';
import Util from '../lib/testutil';
import { expect } from 'chai';
'use strict';

/**
 * Validate the behavior or percentage indiators
 */
describe('Percentage indicator configuration and display', function () {
    before(function() {
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

    it('should append a % sign to numeric values types in numeric fields', function() {
        NavBar.Indicators.click()
        IndPage.createBasicIndicator();
        TargetsTab.setUnitOfMeasure('Mints per moment');
        TargetsTab.setLoPTarget(100);
        TargetsTab.setBaseline(32);
        TargetsTab.setTargetFrequency('Midline and endline');
        TargetsTab.clickPercentType();
        TargetsTab.saveIndicatorChanges();
        // Verify that targets table has % sign in appropriate fields
        expect(TargetsTab.getLoPTarget() == 100);
        expect(TargetsTab.getBaseline() == 32);
    });

/*
    it('should not permit non-numeric values to be typed in numeric fields', function() {
    });

    it('should allow to specify percentage indicators as cumulative or non-cumulative', function() {
    // set cumulative and save
    // set non-cumulative and save
    });

    it('should make percentage indicators default to cumulative', function() {
    // Make percentage indicator
    // Verify that the cumulative radio button is checked
    });

    it('should remove the “Sum of targets” row from the table for a cumulative percentage indicator', function() {
    // Make percentage indicator
    });

    it('should add an “Average of targets” row to the table for a non-cumulative percentage indicator', function() {
    // Verify that non-cum pct indicator adds the average row
    });

    it('“Average of targets” value is the calculated average of the target period values in the table', function() {
    });
*/
})
