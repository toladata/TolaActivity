/**
 * Page model and methods for dealing with the MercyCorps
 * SSO login page
 * @module LoginPage
 */
'use strict';
import Page from './page';
const msecs = 1000;

class LoginPage extends Page {
    // These are for authentication using MC's SSO
    get username() { return $('#login'); }
    get password() { return $('#password'); }
    get login() { return $('.inputsub'); }
    get error() { return browser.getText('#error'); }

    set username(val) { return $('#login').setValue(val); }
    set password(val) { return $('#password').setValue(val); }

    // These are for authenticating using GoogleAuth on a local instance
    get gUsername() { return $('form').$('input#identifierId'); }
    get gPassword() { return $('form').$('input.whsOnd.zHQkBf'); }
    get googleplus() { return $('=Google+'); }
    get gError() { return $('div.dEOOab.RxsGPe').getText(); }

    set gUsername(val) {
        browser.pause(msecs);
        browser.$('form').$('input#identifierId').setValue(val);
        browser.$('form').$('input#identifierId').keys('Enter');
    }
    set gPassword(val) {
        browser.pause(msecs);
        browser.$('form').$('input.whsOnd.zHQkBf').setValue(val);
        browser.$('form').$('input.whsOnd.zHQkBf').keys('Enter');
    }

    // Works everywhere (or at least it better)
    get title() { return browser.getTitle(); }

    open(url) { super.open(url); }
}
export default new LoginPage();
