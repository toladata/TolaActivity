var LoginPage = require('./test/pages/login.page.js');
var IndPage = require('./test/pages/indicators.page.js');
var TargetsTab = require('./test/pages/targets.page.js');
var util = require('./test/lib/testutil.js');
const msec = 1000;

describe('Deleting a lot of indicators', function() {
  // Disable timeouts
  this.timeout(0);
  browser.windowHandleMaximize();

  it('should delete a PI by clicking its Delete button', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();

    IndPage.clickIndicatorsLink();
    browser.waitForVisible('h2=Program Indicators', 10*msec);
    if (browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', true, 10*msec);
    }
    IndPage.selectProgram('Tola Rollout');
    let indButtons = TargetsTab.getProgramIndicatorButtons();
    IndPage.clickProgramsDropdown();
    indButtons[0].click();

    let indicatorList, indicator, confirmBtn
    let deleteCnt = 0;
    let indicatorCount = TargetsTab.getProgramIndicatorsTableCount();
    let buttons = new Array();
    while (indicatorCount > 8) {
      indicatorList = TargetsTab.getProgramIndicatorsTable();
      indicator = indicatorList.shift();
      indicator.click();
      confirmBtn = $('input[value="Confirm"]');
      confirmBtn.click();
      browser.waitForVisible('h2=Program Indicators', 10*msec);
      buttons = TargetsTab.getProgramIndicatorButtons();
      buttons[0].click();
      indicatorCount = TargetsTab.getProgramIndicatorsTableCount();
      console.log('Indicators deleted: ' + deleteCnt++);
    }
  });
});

