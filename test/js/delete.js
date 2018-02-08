var LoginPage = require('./test/pages/login.page.js');
var IndPage = require('./test/pages/indicators.page.js');
var util = require('./test/lib/testutil.js');
const msec = 1000;

describe('TolaActivity Program Indicators page', function() {
  // Disable timeouts
  this.timeout(0);

  it('should exist', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
  });

  it('should delete a PI by clicking its Delete button', function() {
		for (let i = 1; i <= 5; ++i) {
		  let indButton = $('div#toplevel_div').$('div.panel-body').$('a.btn.btn-sm.btn-success');
			indButton.click();
			browser.pause(msec);
			let indTableRows = $$('div#hidden-452>table>tbody>tr');
			let indTableRow = indTableRows[1];
			let indTableRowDel = indTableRows[1].$('=Delete');
			indTableRowDel.click();
			let confirmBtn = $('input[value="Confirm"]');
			confirmBtn.click();
			browser.pause(msec);
			console.log('deleted #' + i);
		}
  }, 3);
});
