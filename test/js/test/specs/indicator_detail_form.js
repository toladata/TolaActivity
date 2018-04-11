import { assert, expect } from 'chai';
import LoginPage from '../pages/login.page';
import IndPage from '../pages/indicators.page';
import TargetsTab from '../pages/targets.page';
import NavBar from '../pages/navbar.page';
import Util from '../lib/testutil';
const msec = 1000;

describe('Indicator creation detail form', function() {
    before(function() {
        // Disable timeouts
        this.timeout(0);
        //browser.windowHandleMaximize();
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

  it('should exist', function() {
    NavBar.Indicators.click();
    assert.equal('Program Indicators', IndPage.getPageName());
    IndPage.createBasicIndicator();
    browser.waitForVisible('h4');
    let title = browser.$('h4').getText().trim();
    expect(title.includes('Goal indicator: Temporary'),
      'Unexpected title text on the indicator detail screen');
  });

  describe('Summary tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Summary')); 
    });
  }); // end summary tab tests

  describe('Performance tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Performance')); 
    });
  }); // end performance tab tests

  describe('Targets tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Targets')); 
    });
  }); // end targets tab tests

  describe('Data Acquisition tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Data Acquisition')); 
    });
  }); // end data acquistion tab tests

  describe('Analysis and Reporting tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Analysis and Reporting')); 
    });
  }); // end analysis tab tests

  describe('Approval tab', function() {
    it('should exist', function() {
      expect(browser.isVisible('=Approval')); 
    });
  }); // end approval tab tests

  it('should have a Help link', function() {
    expect(browser.isVisible('=Help'));
  });

  it('should have a Save Changes button', function() {
    expect(browser.isVisible('=Save changes'));
  });

  it('should have a Reset button', function() {
    expect(browser.isVisible('=Reset'));
  });

  it('should restore form to pre-edit state when Reset button is clicked', function() {
    let select = browser.$('select#id_sector');
    let options = select.$$('option');
    let option = options[1];
    let origVal = option.getValue();

    // 2 - Basic Needs
    select.selectByValue(2);
    let newVal =  select.getValue();
    assert.equal(2, newVal, 'Unexpected selection mismatch');
    IndPage.clickResetButton();
    let resetVal = options[1].getValue();
    assert.equal(origVal, resetVal, 'Unexpected selection mismatch after Reset');
  });
}); // end create indicator detail page tests
