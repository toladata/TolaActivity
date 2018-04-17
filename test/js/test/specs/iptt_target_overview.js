import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
'use strict';

/**
 * IPTT report: Program target overview
 * Tests from mc/issues/119
 */
describe('IPTT report: Program indicator overview', function() {
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
    it('should have a Program dropdown');
    it('should have a Target Frequency dropdown');
    it('should have a Time Span dropdown');
    it('should have a Start month field');
    it('should have an End month field');
    it('should have a View report button');
    it('should require choosing a program');
    it('should require choosing a target frequency');
    it('should require setting reporting period');
    it('should allow choosing a time span');
    it('should allow choosing a Start month');
    it('should allow choosing an End month');
    it('should require the start date to be older than the end date');
    it('should only display combinations of indicators with compatible target frequencies');
    it('should not display combinations of indicators with incompatible target frequencies');
    it('should display indicators with compatible target frequencies and incompatible start months in separate tables');
    it('should open report with filter panel(s) open');
}); 
