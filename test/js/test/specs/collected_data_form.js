var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;

describe('Collected data record: Actual value field for percentage indicator', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
        // Full screen
        browser.windowHandleMaximize();
        // Get login data and login
        let parms = util.readConfig();
        LoginPage.open(parms.baseurl);
        LoginPage.setUserName(parms.username);
        LoginPage.setPassword(parms.password);
        LoginPage.clickLoginButton();
    });

    it('should append a % sign to numbers types in the field');
    it('should not permit non-numeric values to typed in the field');
});
