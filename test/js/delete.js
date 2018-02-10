var LoginPage = require('./test/pages/login.page.js');
var IndPage = require('./test/pages/indicators.page.js');
var util = require('./test/lib/testutil.js');
const msec = 1000;

describe('Deleting a lot of indicators', function() {
  // Disable timeouts
  this.timeout(0);

  it('should delete a PI by clicking its Delete button', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();

     IndPage.clickIndicatorsLink();
     browser.waitForVisible('h2=Program Indicators', 10*msec);
    if (browser.isVisible('div#ajaxloading')) {
      browser.waitForVisible('div#ajaxloading', true);
    }


    IndPage.selectProgram('Tola Rollout');
    let indicatorList, indicator, confirm;
    let indicatorCount = IndPage.getProgramIndicatorsTableCount();
    while (indicatorCount > 6) {
      indicatorList = IndPage.getProgramIndicatorsTable('Tola Rollout');
      indicator = indicatorList.shift();
      indicator.click();
      confirm=$('input[value="Confirm"]');
      confirm.click();
      browser.waitForVisible('h2=Program Indicators', 10*msec);
      indicatorCount = IndPage.getProgramIndicatorsTableCount();
    }
  });
});

