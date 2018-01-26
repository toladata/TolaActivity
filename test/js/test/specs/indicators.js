var assert = require('assert');
var fs = require('fs');

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};
var parms = readConfig();

describe('TolaActivity Program Indicators page', function() {
  it('should require user to authenticate', function() {
    browser.url(parms.baseurl);
    var title = browser.getTitle();
    assert.equal(title, 'Mercy Corps Sign-On');
  });

  it('should have a login field', function() {
    var login = $('#login');
    login.setValue(parms.username);
  });

  it('should have a password field', function() {
    var password = $('#password');
    password.setValue(parms.password);
  });

  it('should have a Log In button', function() {
    button = $('.inputsub');
    button.click();
  });

  // after all of that, should wind up at the Indicators page
  it('should exist', function() {
    browser.url('https://tola-activity-demo.mercycorps.org/indicators/home/0/0/0/');
    var h2 = $('h2');
    assert.equal(h2.getText(), 'Program Indicators');
  });

  describe('Programs dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownProgram');
      assert(button.getText() == 'Programs');
      button.click();
    });

    it('should have same item count as Programs table', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var programs = buttons[0];
      // have to click to make the menu visible
      programs.click();
      var menu = programs.$('ul.dropdown-menu');
      var progList = menu.$$('li');
      programs.click();
      
      var table = $('div#toplevel_div')
      var rows = table.$$('div.panel.panel-default')
      assert(progList.length == rows.length);
    });

    it('should have same items as Programs table', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var programs = buttons[0];
      // have to click to make the menu visible
      programs.click();
      var menu = programs.$('ul.dropdown-menu');
      var progList = menu.$$('li');
      var table = $('div#toplevel_div')
      var rows = table.$('div.panel.panel-default').$$('h4');
      for (let i = 0; i < progList.length; ++i) {
        assert.equal(rows[i].getText() == progList[i].$('a').getText());
      }
    });
  }); // end programs dropdown tests

  // TODO: Having difficulty working with this element; the non-standard
  // dropdown construction complicates it.
  describe('Indicators dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownIndicator');
      assert(button.getText() == 'Indicators');
      button.click();
    });
    it('should have at least one entry');
    it('should default to showing all PIs for a program');
    it('should be able to select any/all list items');
  }); // end indicators dropdown tests
     
  // TODO: Having difficulty working with this element; the non-standard
  // dropdown construction complicates it.
  describe('Indicator Type dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownIndicatorType');
      assert(button.getText() == 'Indicator Type');
      button.click();
    });
    it('should have at least one entry');
    it('should default to showing all Indicator Types for a program');
    it('should be able to filter the resultset by Indicator Type');
  }); // end indicator type dropdown tests

/*
  it('should toggle PIs table by clicking PI Indicators button');
  it('should increase PI count after adding new indicator');
  it('should decrease PI count after deleting indicator');
  it('should view a PI by clicking its name in Indicator Name column');
  it('should be able to edit a PI by clicking its Edit button');
  it('should be able to view PI evidence table by clicking its Data button');
  it('should have matching counts between Data button and evidence table');
  it('should increase evidence count when PI evidence added');
  it('should decrease evidence count when PI evidence deleted');
  it('should be able to delete a PI by clicking its Delete button');
  
  describe('Program Indicators table', function() {
    it('should open the Create an Indicator form when New Indicator button is clicked');
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
      it('should have a Save button');
      it('should validate input data after Save button clicked');
      it('should validate input data before committing');
      it('should not save invalid input data');
      it('should highlight invalid input data');
      it('should have a Reset button');
      it('should clear the form by clicking the Reset button');
      it('should restore the form defaults by clicking the Reset button');
      it('should pull data from Tola Tables by clicking the Import Evidence From Tola Tables link');
      it('should open the Indicator edit form by clicking the Add a Disaggregation link');
      it('should only accept numerica values in the disaggregations Actuals fields');
      it('should have a cancel button');
      it('should be able to close the firm by clicking the Cancel button');
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
*/
});
