import { assert } from 'chai';
import IndPage from '../pages/indicators.page';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';

describe('Report filter panel', function() {
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

    it('should filter per program');
    it('should filter per target frequency for Periodic targets overview');
    it('should filter per time period for Program indicator overview');
    it('should filter per time span (see #119)');
    it('should filter by level');
    it('should filter by type');
    it('should filter by sector');
    it('should filter by site');
    it('should filter by indicator');
    it('should be able to filter by multiple levels');
    it('should be able to filter by multiple types');
    it('should be able to filter by multiple sectors');
    it('should be able to filter by multiple sites');
    it('should be able to filter by multiple indicators');
    it('should be able to include a given indicator that would otherwise be filtered');
    it('should be able to filter a given indicator that would otherwise be included');
    it('should apply filters cumulatively');
    it('should have a Cancel button');
    it('should have a Save changes button');
});
