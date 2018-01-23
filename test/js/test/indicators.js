'use strict';
var webdriver = require('selenium-webdriver');
var until = require('selenium-webdriver').until;
var logging = require('selenium-webdriver').logging;
var test = require('selenium-webdriver/testing');
var assert = require('chai').assert;
var expect = require('chai').should;
var fs = require('fs');
let el;
var driver;

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};

async function newTolaSession(parms) {
  driver = new webdriver.Builder()
  .forBrowser(parms.browser)
  .build();
  await driver.get(parms.baseurl);
  el = await driver.getTitle();
  assert.equal(el, 'Mercy Corps Sign-On', el);
}

async function newTolaLogin(parms) {
  el = await driver.findElement({name: 'login'});
  await el.sendKeys(parms.username);

  el = await driver.findElement({name: 'password'});
  await el.sendKeys(parms.password);

  el = await driver.findElement({className: 'inputsub'})
  await el.click();
}

test.describe('TolaActivity Indicators Page', function() {
  var parms = readConfig();
  
  test.before(async function() {
    await newTolaSession(parms);
  });

  test.after(async function() {
    await driver.quit();
  });

  test.it('should require login authentiction', async function() {
    await newTolaLogin(parms);
  });

  test.it('should exist', async function() {
    await driver.get('https://tola-activity-demo.mercycorps.org/indicators/home/0/0/0/');
    el = await driver.wait(until.elementLocated({css: 'h2'}));
    assert.equal(await el.getText(), 'Program Indicators');
  });

   // TODO: Having difficulty working with this element; the non-standard
   // dropdown construction complicates it.
  test.describe('Programs dropdown', function() {
    test.it('should be present on page', async function() {
      el = await driver.findElement({id: 'dropdownProgram'});
      assert(el.click());
      assert.equal(await el.getText(), 'Programs');
    });
    test.it('should have at least one entry');
    test.it('should default to showing all programs');
    test.it('should be able to filter PIs by Program');
    test.it('should be able to filter Programs by PI');
    test.it('should have same item count as Programs table');
    test.it('should have same items as Programs table');
   }); // end programs dropdown tests
  
  // TODO: Having difficulty working with this element; the non-standard
  // dropdown construction complicates it.
  test.describe('Indicators dropdown', function() {
    test.it('should be present on page', async function() {
      el = await driver.wait(until.elementLocated({id: 'dropdownIndicator'}));
      assert(el.click());
      assert.equal(await el.getText(), 'Indicators');
    });
    test.it('should have at least one entry');
    test.it('should default to showing all PIs for a program');
    test.it('should be able to select any/all list items');
  }); // end indicators dropdown tests
     
  // TODO: Having difficulty working with this element; the non-standard
  // dropdown construction complicates it.
  test.describe('Indicator Type dropdown', function() {
    test.it('should be present on page', async function() {
      el = await driver.wait(until.elementLocated({id: 'dropdownIndicatorType'}));
      assert(el.click());
      assert.equal(await el.getText(), 'Indicator Type');
    });
    test.it('should have at least one entry');
    test.it('should default to showing all Indicator Types for a program');
    test.it('should be able to filter the resultset by Indicator Type');
  }); // end indicator type dropdown tests
  test.it('should toggle PIs table by clicking PI Indicators button');
  test.it('should increase PI count after adding new indicator');
  test.it('should decrease PI count after deleting indicator');
  test.it('should view a PI by clicking its name in Indicator Name column');
  test.it('should be able to edit a PI by clicking its Edit button');
  test.it('should be able to view PI evidence table by clicking its Data button');
  test.it('should have matching counts between Data button and evidence table');
  test.it('should increase evidence count when PI evidence added');
  test.it('should decrease evidence count when PI evidence deleted');
  test.it('should be able to delete a PI by clicking its Delete button');
  
  test.describe('Program Indicators table', function() {
    test.it('should open the Create an Indicator form when New Indicator button is clicked');
    test.it('should open the Grid/Print Report page when button is clicked');
    test.it('should highlight invalid data');
    test.it('should return to previous screen if Cancel button clicked');
    test.it('should clear form when Clear button clicked');
    
    test.describe('Create an Indicator form', function() {
      test.it('should show context-sensitve help by clicking Form Help/Guidance button');
      test.it('should have an Indicator Service Templates dropdown');
      test.it('should have a Custom entry in the Indicator Service Templates dropdown');
      test.it('should have a Service Indicator dropdown');
      test.it('should have a Country dropdown');
      test.it('should have a Program dropdown');
      test.it('should have a Save button');
      test.it('should validate input data after clicking Save button and before committing it');
      test.it('should not save unvalidated input data');
      test.it('should highlight invalid input data');
      test.it('should save data after validating it');
      test.it('should open Indicator detail form after clicking Save button');
      test.it('should have a Cancel button');
      test.it('should reset and close form when Cancel button clicked');
      test.it('should return to previous screen when Cancel button clicked');
      test.it('should have a Reset button to reset form');
      test.it('should have a Summary tab');
      test.it('should have a Performance tab');
      test.it('should hnve a Targets tab');
      test.it('should have a Data Acquisition tab');
      test.it('should have a Analysis and Reporting tab');
      test.it('should have an Approval tab');
      test.it('should have a Help link');
      test.it('should have a Save Changes button');
      test.it('should have a Reset button');
      test.it('should have a Cancel button');
      test.it('should trigger cancel action by pressing Escape key');
      test.it('should validate input data after clicking Save Changes button');
      test.it('should validate input data before committing it');
      test.it('should restore form to pre-edit state when Reset button is clicked');

      test.describe('Indicator creation detail form', function() {
        test.it.skip('should confirm indicator created', function() {
          // CSS selector: #alerts
          // CSS path: .alert
          // XPath: /html/body/div[1]/div[2]/div
          el = driver.findElement({xpath: '/html/body/div[1]/div[2]/div'}).then(function(el) {
            assert.include(el.getText(), 'Success', el.getText());
            assert.match(el.getText(), '/^Success .*Created$/', el.getText());
          });
        });

        test.describe('Summary tab', function() {
          test.it('should exist');
          test.it('should have Program field matching input data')
        }); // end summary tab tests

        test.describe('Performance tab', function() {
          test.it('should exist');
        }); // end performance tab tests

        test.describe('Targets tab', function() {
          test.it('should exist');
        }); // end targets tab tests

        test.describe('Data Acquisition tab', function() {
          test.it('should exist');
        }); // end data acquistion tab tests

        test.describe('Analysis and Reporting tab', function() {
          test.it('should exist');
        }); // end analysis tab tests

        test.describe('Approval tab', function() {
          test.it('should exist');
        }); // end approval tab tests
      }); // end create indicator detail page tests
    }); // end create new indicator form tests

    test.describe('Grid/Print Report page', function() {
      test.it('should exist');
      test.it('should have an Export All button');
      test.it('should export all report entries when Export All button is clicked');
    });

    test.describe('Indicator evidence dropdown', function() { 
      test.it("should toggle indicator's evidence dropdown by clicking its Data button");
      test.it('should have the same row count as evidence count on Data button');
      test.it('should be able to edit evidence line item by clicking its Edit button');
      test.it('should be able to edit evidence line item by clicking its Indicator Name');
      test.it('should open Collected Data form when editing evidence line item');
      test.it('should be able to delete evidence line item by clicking its Delete button');
      test.it('should be able to add evidence line item by clicking the New Data button');
      test.it('should open blank Collected Data form when the New Data button is clicked');
    });

    test.describe('Collected Data form', function() {
      test.it('should exist');
      test.it('should require required fields');
      test.it('should not require optional fields');
      test.it('should have a Save button');
      test.it('should validate input data after Save button clicked');
      test.it('should validate input data before committing');
      test.it('should not save invalid input data');
      test.it('should highlight invalid input data');
      test.it('should have a Reset button');
      test.it('should clear the form by clicking the Reset button');
      test.it('should restore the form defaults by clicking the Reset button');
      test.it('should pull data from Tola Tables by clicking the Import Evidence From Tola Tables link');
      test.it('should open the Indicator edit form by clicking the Add a Disaggregation link');
      test.it('should only accept numerica values in the disaggregations Actuals fields');
      test.it('should have a cancel button');
      test.it('should be able to close the firm by clicking the Cancel button');
    });

    // TODO: Indicator Delete confirmation page only has a Confirm
    // button and no way to indicate "No" except using the browser's
    // Back button to return to the previous page. Except that operation
    // actually return the user to in the Program Indicators index page
    // instead. This violates the Principle of Least Surprise.
    test.it('should close the delete dialog by pressing the Esc key');
    test.it('should have a Cancel button that returns to the previous screen');
    test.it('should identify required fields as such');
    test.it('should not permit read-only fields to be edited');
    test.it('should have a Grid/Print Report button');
    test.it('should open a report page when the Grid/Print Report button is clicked');
  });

  // These are enhancements
  test.it('should highlight PIs with no evidence');
  test.it('should disable Indicators button if program has no indicators');
  test.it('should be able to sort table by clicking a column header');
});
