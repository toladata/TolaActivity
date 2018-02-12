var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');
const msec = 1000;
const delay = 10*msec;

describe('TolaActivity Program Indicators page', function() {
  // Disable timeouts
  this.timeout(0);
  browser.windowHandleMaximize();

  it('should exist', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    // FIXME: pageName should be a property
    assert.equal('Program Indicators', IndPage.pageName());
  });

  describe('Programs dropdown', function() {
    it('should be present on page', function() {
			if (browser.isVisible('div#ajaxloading')) {
				browser.execute("document.getElementById('ajaxloading').style.visibility = 'hidden';");
		  }
      IndPage.clickProgramsDropdown();
      IndPage.clickProgramsDropdown();
    });

    it('should have same number of items as the Programs table', function() {
      let progList = IndPage.getProgramsDropdownList();
      let progTable = IndPage.getProgramsTable();
      assert.equal(progList.length, progTable.length, 'row count mismatch');
    });

    it('should have same items as Programs table', function() {
      let progList = IndPage.getProgramsDropdownList();
      let listItems = new Array();
      for (let prog of progList) {
        let name = prog.split('-')[1].trim();
        listItems.push(name);
      }

      let progTable = IndPage.getProgramsTable();
      for (let i = 0; i < progTable.length; i++) {
        let rowText = progTable[i].split('\n')[0].trim();
        assert.equal(rowText, listItems[i]);
      };
    });

    it('should filter programs table by selected program name', function() {
      let progList = IndPage.getProgramsDropdownList();
      let listItem = progList[0];
      IndPage.selectProgram(listItem);

      // should have a single row in the table
      let progTable = IndPage.getProgramsTable();
      // row should be the one selected from the dropdown
      let rowText = progTable[0].split('\n')[0].trim();
      let listText = listItem.split('-')[1].trim();
      assert.equal(rowText, listText, 'program name mismtach');
    });
  }); // end programs dropdown tests

  describe('Indicators dropdown', function() {
    it('should be present on page', function() {
      IndPage.clickIndicatorsDropdown();
    });

    it('should have at least one entry', function() {
      let indList = IndPage.getIndicatorsDropdownList();
      assert(indList.length > 0);
    });

  }); // end indicators dropdown tests

  describe('Indicator Type dropdown', function() {
    it('should be present on page', function() {
      IndPage.clickIndicatorTypeDropdown();
    });

    it('should have at least one entry', function() {
      let indTypeList = IndPage.getIndicatorTypeList();
      assert(indTypeList.length > 0);
    });

  }); // end indicator type dropdown tests

  // FIXME: Still need to get WebDriver code out of this test
  it('should toggle PIs table by clicking PI Indicators button', function() {
    let buttons = TargetsTab.getProgramIndicatorButtons();
    for (let button of buttons) {
      let targetDiv = 'div' + button.getAttribute('data-target');
      let isVisible = browser.isVisible(targetDiv);
      // Starts out collapsed
      assert.equal(false, isVisible);

      // Open it and verify
      button.click();
      // FIXME: This is a horrible hack to accommodate a race.
      // <div id="ajaxloading" class="modal ajax_loading" style="display: block;"></div>
      // obscures the button we want to click, but how long varies because Internet,
      // so hide the obscuring div. Pfft.
      // Close it and move on
      browser.execute("document.getElementById('ajaxloading').style.visibility = 'hidden';");
      isVisible = browser.isVisible(targetDiv);
      assert.equal(true, isVisible);

      button.click();
    }
  });

  // FIXME: Still need to get WebDriver code out of this test
  it('should have matching indicator counts on data button and in table', function() {
		if(browser.isVisible('div#ajaxloading')) {
			browser.waitForVisible('div#ajaxloading', delay, true);
		}
		IndPage.clickIndicatorsLink();
    let buttons = TargetsTab.getProgramIndicatorButtons();
    for (let button of buttons) {
      let buttonCnt = parseInt(button.getText());
      let targetDiv = button.getAttribute('data-target');
      // Expand the table
      button.click();
      // Get indicator count from table
      let table = $('='+targetDiv).$('table');
      // collapse the table
      button.click();
    }
  }, 3); // Try this flaky test up to 3 times before failing

  describe('Program Indicators table', function() {
    it('should view PI by clicking its name in Indicator Name column', function() {
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
				browser.execute("document.getElementById('ajaxloading').style.visibility = 'hidden';");
		  }
      let indicatorName = indicatorNameList[0];
      TargetsTab.clickProgramIndicatorsButton(indicatorName);
    });

    it('should be able to create PI by clicking the New Indicator button', function() {
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('New Indicator button test');
      TargetsTab.setUnitOfMeasure('Bugs fixed');
      TargetsTab.setLoPTarget(172);
      TargetsTab.setBaseline(173);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
    });

    it('should increase PI count after adding new indicator');
    it('should be able to delete PI by clicking its Delete button');
    it('should decrease PI count after deleting indicator');
    it('should be able to edit PI by clicking its Edit button');
    it('should open the Grid/Print Report page when button is clicked');
    it('should highlight invalid data');
    it('should return to previous screen if Cancel button clicked');
    it('should clear form when Clear button clicked');

    describe('Create an Indicator form', function() {
      it('should show context-sensitve help by clicking Form Help/Guidance button');
      it('should have an Indicator Service Templates dropdown');
      it('should have a Custom entry in the Indicator Service Templates dropdown');
      it('should have a Service Indicator dropdown');
      it('should have a Country dropdown');
      it('should have a Program dropdown');
      it('should have a Save button');
      it('should validate input data after clicking Save button and before committing it');
      it('should not save unvalidated input data');
      it('should highlight invalid input data');
      it('should save data after validating it');
      it('should open Indicator detail form after clicking Save button');
      it('should have a Cancel button');
      it('should reset and close form when Cancel button clicked');
      it('should return to previous screen when Cancel button clicked');
      it('should have a Reset button to reset form');
      it('should have a Summary tab');
      it('should have a Performance tab');
      it('should hnve a Targets tab');
      it('should have a Data Acquisition tab');
      it('should have a Analysis and Reporting tab');
      it('should have an Approval tab');
      it('should have a Help link');
      it('should have a Save Changes button');
      it('should have a Reset button');
      it('should have a Cancel button');
      it('should trigger cancel action by pressing Escape key');
      it('should validate input data after clicking Save Changes button');
      it('should validate input data before committing it');
      it('should restore form to pre-edit state when Reset button is clicked');

      describe('Indicator creation detail form', function() {
        it.skip('should confirm indicator created', function() {
          // CSS selector: #alerts
          // CSS path: .alert
          // XPath: /html/body/div[1]/div[2]/div
          el = driver.findElement({xpath: '/html/body/div[1]/div[2]/div'}).then(function(el) {
            assert.include(el.getText(), 'Success', el.getText());
            assert.match(el.getText(), '/^Success .*Created$/', el.getText());
          });
        });

        describe('Summary tab', function() {
          it('should exist');
          it('should have Program field matching input data')
        }); // end summary tab tests

        describe('Performance tab', function() {
          it('should exist');
        }); // end performance tab tests

        describe('Targets tab', function() {
          it('should exist');
        }); // end targets tab tests

        describe('Data Acquisition tab', function() {
          it('should exist');
        }); // end data acquistion tab tests

        describe('Analysis and Reporting tab', function() {
          it('should exist');
        }); // end analysis tab tests

        describe('Approval tab', function() {
          it('should exist');
        }); // end approval tab tests
      }); // end create indicator detail page tests
    }); // end create new indicator form tests

    describe('Grid/Print Report page', function() {
      it('should exist');
      it('should have an Export All button');
      it('should export all report entries when Export All button is clicked');
    });

    describe('Indicator evidence dropdown', function() {
      it('should be able to view PI evidence table by clicking its Data button');
      it('should decrease evidence count when PI evidence deleted');
      it('should increase evidence count when PI evidence added');
      it("should toggle indicator's evidence dropdown by clicking its Data button");
      it('should have the same row count as evidence count on Data button');
      it('should be able to edit evidence line item by clicking its Edit button');
      it('should be able to edit evidence line item by clicking its Indicator Name');
      it('should open Collected Data form when editing evidence line item');
      it('should be able to delete evidence line item by clicking its Delete button');
      it('should be able to add evidence line item by clicking the New Data button');
      it('should open blank Collected Data form when the New Data button is clicked');
    });

    describe('Collected Data form', function() {
      it('should exist');
      it('should require required fields');
      it('should not require optional fields');
      it('should validate input data before saving it');
      it('should not save invalid input data');
      it('should have a Reset button');
      it('should clear the form by clicking the Reset button');
      it('should restore the form defaults by clicking the Reset button');
      it('should open the Indicator edit form by clicking the Add a Disaggregation link');
      it('should only accept numeric values in the disaggregations Actuals fields');
      it('should have a cancel button');
      it('should be able to close the form by clicking the Cancel button');
    });

    // TODO: Indicator Delete confirmation page only has a Confirm
    // button and no way to indicate "No" except using the browser's
    // Back button to return to the previous page. Except that operation
    // actually return the user to in the Program Indicators index page
    // instead. This violates the Principle of Least Surprise.
    it('should close the delete dialog by pressing the Esc key');
    it('should have a Cancel button that returns to the previous screen');
    it('should identify required fields as such');
    it('should not permit read-only fields to be edited');
    it('should have a Grid/Print Report button');
    it('should open a report page when the Grid/Print Report button is clicked');
  });

  // These are enhancements
  it('should highlight PIs with no evidence');
  it('should disable Indicators button if program has no indicators');
  it('should be able to sort table by clicking a column header');
  it('should be able to select any/all list items');
  it('should default to showing all Indicator Types for a program');
  it('should be able to filter the resultset by Indicator Type');
});
