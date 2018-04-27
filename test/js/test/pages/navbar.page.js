/**
 * "Page" model and methods for dealing with the MercyCorps
 * TolaActivity navigation bar/page header
 * @module NavBar
 */
'use strict';

class NavBar {
    get TolaActivity() { return browser.$('a.navbar-brand'); }
    get Workflow() { return browser.$('=Workflow'); }
    get Indicators() {
        if (! browser.isVisible('nav.navbar')) {
            browser.waitForVisible('nav.navbar');
        }
        return browser.$('ul.navbar-nav').$('=Indicators');
    }
    get Reports() { return browser.$('=Reports'); }
    get UserProfile() { return browser.$('ul>li.dropdown>a'); }
}
export default new NavBar();
