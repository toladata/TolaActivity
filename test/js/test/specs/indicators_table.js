import { assert, expect } from 'chai';
import LoginPage from '../pages/login.page';
import NavBar from '../pages/navbar.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import Util from '../lib/testutil';
const msec = 1000;
const delay = 10*msec;

describe('Program Indicators table', function() {
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

  // FIXME: Still need to get WebDriver code out of this test
    it('should toggle table when a PI button is clicked', function() {
        //NavBar.Indicators.click();
        IndPage.clickIndicatorsLink();
        if(browser.isVisible('div#ajaxloading')) {
            browser.waitForVisible('div#ajaxloading', delay, true);
        }

        let buttons = TargetsTab.getProgramIndicatorButtons();
        for (let button of buttons) {
            let targetDiv = 'div' + button.getAttribute('data-target');
            let isVisible = browser.isVisible(targetDiv);

            // If it's open, close it; start from a known state
            if (isVisible) {
                button.click();
                if (browser.isVisible('div#ajaxloading')) {
                    browser.waitForVisible('div#ajaxloading', delay, true);
                }
            }
            expect(false == browser.isVisible(targetDiv), 'Unable to set initial state');

            // Open it
            button.click();
            if (browser.isVisible('div#ajaxloading')) {
                browser.waitForVisible('div#ajaxloading', delay, true);
            }
            expect(true == browser.isVisible(targetDiv));

            // Close it again
            button.click();
            if (browser.isVisible('div#ajaxloading')) {
                browser.waitForVisible('div#ajaxloading', delay, true);
            }
            expect(false == browser.isVisible(targetDiv));
        }
    });

    it('should show a detail screen when an indicator name is clicked', function() {
        if (browser.isVisible('div#ajaxloading')) {
            browser.waitForVisible('div#ajaxloading', delay, true);
        }
        //NavBar.Indicators.click();
        IndPage.clickIndicatorsLink();
        // Make list of Indicators buttons
        let buttons = TargetsTab.getProgramIndicatorButtons();
        // Click the first one to expand the table
        let button = buttons[0];
        button.click();
        // Make list of indicator names in resulting table
        // FIXME: needs to be from table, not dropdown
        let indicatorNameList = IndPage.getIndicatorsDropdownList();
        // Click the first one
        if (browser.isVisible('div#ajaxloading')) {
            browser.waitForVisible('div#ajaxloading', delay, true);
        }
        let indicatorName = indicatorNameList[0];
        TargetsTab.clickProgramIndicatorsButton(indicatorName);
    });

    it('should be able to create PI by clicking the New Indicator button', function() {
        IndPage.clickIndicatorsLink();
        IndPage.clickNewIndicatorButton();
        IndPage.saveNewIndicator();
        TargetsTab.setIndicatorName('New Indicator button test');
        TargetsTab.setUnitOfMeasure('Bugs fixed');
        TargetsTab.setLoPTarget(81);
        TargetsTab.setBaseline(82);
        TargetsTab.setTargetFrequency('Life of Program (LoP) only');
        TargetsTab.saveIndicatorChanges();
    });

    it('should increase PI count after adding new indicator', function() {
        IndPage.clickIndicatorsLink();
        //NavBar.Indicators.click();
        // Get old count
        let buttons = TargetsTab.getProgramIndicatorButtons();
        let buttonText = buttons[0].getText();
        let oldCount = parseInt(buttonText);
        // Create new indicator
        IndPage.clickNewIndicatorButton();
        IndPage.saveNewIndicator();
        IndPage.clickIndicatorsLink();
        // Get new count
        buttons = TargetsTab.getProgramIndicatorButtons();
        buttonText = buttons[0].getText();
        let newCount = parseInt(buttonText);
        // Assert new count > old count
        expect(newCount == oldCount + 1);
    });

    it('should be able to delete PI by clicking its Delete button', function() {
        IndPage.clickIndicatorsLink();
        //NavBar.Indicators.click();
        IndPage.deleteIndicator();
    });

    it('should decrease PI count after deleting indicator', function() {
        IndPage.clickIndicatorsLink();
        //NavBar.Indicators.click();
        // Get old count
        let buttons = TargetsTab.getProgramIndicatorButtons();
        let buttonText = buttons[0].getText();
        let oldCount = buttonText;

        // Delete an indicator
        IndPage.deleteIndicator();

        // Get new count
        buttons = TargetsTab.getProgramIndicatorButtons();
        buttonText = buttons[0].getText();

        // Assert new count < old count
        let newCount = buttonText;
        expect(newCount == oldCount - 1);
    });

    it('should edit an indicator by clicking its Edit button', function() {
        IndPage.clickIndicatorsLink();
        IndPage.editIndicator();
        expect(browser.isVisible('div#indicator_modal_content'));
    });
});
