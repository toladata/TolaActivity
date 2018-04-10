import { expect } from 'chai';
import util from '../lib/testutil';
import LoginPage from '../pages/login.page';
import reporter from 'wdio-allure-reporter';

describe('TolaActivity Login screen', function() {
    before(function() {
        this.timeout(0);
        //browser.windowHandleMaximize();
    });

    it('should deny access if username is invalid', function() {
        let parms = util.readConfig();
        // inject bogus username
        parms.username = 'HorseWithNoName';

        LoginPage.open(parms.baseurl); 
        if (parms.baseurl.includes('mercycorps.org')) {
            LoginPage.username = parms.username;
            LoginPage.password = parms.password;
            LoginPage.login.click();
            expect(LoginPage.error).to.include('Login failed:');
        } else if (parms.baseurl.includes('localhost')) {
            LoginPage.googleplus.click();
            if ('TolaActivity' != LoginPage.title) {
                LoginPage.gUsername = parms.username + '@mercycorps.org';
            }
            expect(LoginPage.gError).includes("Couldn't find your Google Account");
        }
    });

    it('should deny access if password is invalid', function() {
        let parms = util.readConfig();
        // Inject bogus password
        parms.password = 'ThisBetterFail';

        LoginPage.open(parms.baseurl);
        if (parms.baseurl.includes('mercycorps.org')) {
            LoginPage.username = parms.username;
            LoginPage.password = parms.password;
            LoginPage.login.click();
            expect(LoginPage.error).includes('Login failed:');
        } else if (parms.baseurl.includes('localhost')) {
            LoginPage.googleplus.click();
            if ('TolaActivity' != LoginPage.title) {
                LoginPage.gUsername = parms.username + '@mercycorps.org';
                LoginPage.gPassword = parms.password;
            }
            expect(LoginPage.gError).includes('Wrong password.');
        }
    });

    it('should require unauthenticated user to authenticate', function() {
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
        expect(LoginPage.title).to.equal('TolaActivity');
    });
});
