import { assert } from  'chai';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from  '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
const msec = 1000;

describe('Grid/Print Report page', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
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

    it('should have a Grid/Print Report button for each program', function() {
        NavBar.Indicators.click();
        assert.equal('Program Indicators', IndPage.getPageName());
        let progList = IndPage.getProgramsDropdownList();
        let prog = progList[1];
        IndPage.selectProgram(prog);
        assert(browser.isVisible('=Grid/Print Report'));
    });

    it('should open when the Grid/Print Report button is clicked', function() {
        NavBar.Indicators.click();
        let progList = IndPage.getProgramsDropdownList();
        let prog = progList[1];
        IndPage.selectProgram(prog);
        browser.$('=Grid/Print Report').click();
        let pageTitle = IndPage.getPageName();
        assert(pageTitle.includes('Indicator Print/Grid Report'), 
            'Did not receive expected report page title');
    });

    it('should have an Export All button', function() {
        NavBar.Indicators.click();
        let progList = IndPage.getProgramsDropdownList();
        let prog = progList[1];
        IndPage.selectProgram(prog);
        browser.$('=Grid/Print Report').click();

        // Scroll to the bottom of the page
        browser.scroll('button[type="submit"]');
        let button = browser.$('button[type="submit"]');
        let text = button.getText();
        assert(text.includes('Export All'), 'Did not find expected button text');
    });

    it('should export all report entries when Export All button is clicked', function() {
        NavBar.Indicators.click();
        let progList = IndPage.getProgramsDropdownList();
        let prog = progList[1];
        IndPage.selectProgram(prog);
        browser.$('=Grid/Print Report').click();

        // Scroll to the bottom of the page
        let button = browser.$('button[type="submit"]');
        browser.scroll('button[type="submit"]');
        button.click();
        //IndPage.clickExportAllButton('myexportfile.csv');
    });
    it('should be able to save reports as CSV');
    it('should be able to save reports as PDF');
});
