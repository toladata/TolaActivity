var assert = require('chai').assert;
import LoginPage from '../pages/login.page';
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;

describe('Collected data record: Actual value field for percentage indicator', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
        //browser.windowHandleMaximize(); 

        // Get login data and login
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

    it('should append a % sign to numbers types in the field');
    it('should not permit non-numeric values to typed in the field');
});
