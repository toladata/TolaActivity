import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
'use strict';

/**
 * IPTT report: Program indicator overview
 * Tests from mc/issues/119
 */
describe('Indicator evidence percent indicators', function() {
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

    it('should exist');
    it('should have Program dropdown');
    it('should have a Time Span dropdown');
    it('should have a Start month picker field');
    it('should have an End month picker field');
    it('should have a View Report button');
    it('should require choosing a program');
    it('should allow choosing a relative time span');
    it('should set Start and End date fields based on time period selected');
    it('should allow selecting start and end months');
    it('should allow choosing a relative time span and then modifying the month');
    it('should default time span to Show all');
    it('should open report with filter panel(s) open');
    it('should display Targets and % Met fields for LoP target and actual');
    it('should require the start month to be older than the end date');
    it('should only display LoP targets, not intermediate targets');
    it('should only display % Met for LoP targets, not intermediate targets');
}); 
