import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
import { assert, expect } from 'chai';
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

    it('should default to number indicators');
    it('should default number indicators to non-cumulative indicators');
    it('should default percentage indicators to cumulative indicators');
    it('should add “%” to LoP target and Baseline text boxes');

    it('should have direction of change option', function() {
        TargetsTab.setDirectionOfChange('none');
        expect(TargetsTab.getDirectionOfChange() == 'none');
        TargetsTab.setDirectionOfChange('pos');
        expect(TargetsTab.setDirectionOfChange() == 'pos');
        TargetsTab.setDirectionOfChange('net');
        expect(TargetsTab.setDirectionOfChange() == 'neg');
    });
    it('should default to no direction of change');
}); 
