// TODO: Refactor me to get rid of all the repetitive code
// TODO: Think about how to test all of the help screens
// TODO: Many of these are more fluidly, natually expressed using
// expect(...)
// TODO: Write tests for the new indicator evidence form
// TODO: What happens when we feed the textareas // the BLNS?
// TODO: Focus testing on the platform(s) most used in the field were
// Tola is deployed. What browsers and what are their priorities?
// TODO: Selecting elements by linkText is fragile.
// TODO: Didn't find suitable unique name or id selectors on // key
// elements;
// TODO: Most of these assertions are bogus
// TODO: set of tests for the edit dialog
// TODO: Much more work to do on the Indicator creation detail //
// screen
// TODO: is clicking an indicator name functionally equivalent to
// clicking its Edit button?
// TODO: Focus testing on the platform(s) most used by Tola users.
// What browsers and what are their priorities?

var webdriver = require('selenium-webdriver');
var test = require('selenium-webdriver/testing');
var assert = require('chai').assert;
var expect = require('chai').should;
var fs = require('fs');
let el;

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};
var parms = readConfig();

var driver = new webdriver.Builder()
  .forBrowser(parms.browser)
  .build();

test.describe('TolaActivity', function() {
  test.before(function() {
    driver.get(parms.baseurl);
  });

  test.after(function() {
    driver.quit();
  });

  test.describe('Login Screen', function() {
    test.it('should require user to authenticate', function() {
      el = driver.getTitle().then(function(el) {
        assert.equal(el, 'Mercy Corps Sign-On', el);
      });
    });

    test.it('should have a login field', function() {
      el = driver.findElement({name: 'login'})
        .then(function(el) {
          el.sendKeys(parms.username);
        });
    });

    test.it('should have a password field', function() {
      el = driver.findElement({name: 'password'})
        .then(function(el) {
          el.sendKeys(parms.password);
        });
    });

    test.it('should have a Log In button', function() {
      el = driver.findElement({className: 'inputsub'})
        .then(function(el) {
          el.click();
        });
    });

    test.it('should not permit access if username is invalid');
    test.it('should not permit access if password is invalid');

  }); // end login screen tests

  test.describe('TolaActivity Dashboard', function() {
    test.it('should have a page title', function() {
      el = driver.getTitle().then(function(el) {
        assert.equal(el, 'TolaActivity', el);
      });
    });

    test.it('should have a TolaActivity link', function() {
      let xp = '/html/body/nav/div/div[1]/a/img';
      el = driver.findElement({xpath: xp}).then(function(el) {
        assert(el.click());
      });
    });
    
    // TODO: file enhancement request about the id dropdownMenu1
    test.it('should have a Country Dashboard dropdown', function() {
      let xp = '/html/body/div[1]/div[3]/div/div/div[2]/div/div[1]';
      el = driver.findElement({xpath: xp})
        .then(function(el) {
          assert(el.click());
        });
    });

    // TODO: file enhancement request about the id dropdownMenu3
    test.it('should have a Filter by Program link', function() {
      let xp = '/html/body/div[1]/div[3]/div/div/div[2]/div/div[2]';
      el = driver.findElement({xpath: xp})
        .then(function(el) {
          assert(el.click());
        });
    });

    test.it('should have a Workflow dropdown', function() {
      let xp = '/html/body/nav/div/div[2]/ul[1]/li[1]/a';
      el = driver.findElement({xpath: xp}).then(function(el) {
        assert(el.click());
      });
    });

    test.it('should have a Form Library dropdown', function() {
      el = driver.findElement({linkText: 'Form Library'})
        .then(function(el) {
          assert(el.click());
        });
    });
    
    test.it('should have a Reports link', function() {
      el = driver.findElement({linkText: 'Reports'})
        .then(function(el) {
          assert(el.click());
        });
    });

    test.it.skip('should have a Profile link', function() {
      let xp = '/html/body/nav/div/div[2]/ul[2]/li[1]/a';
      el = driver.findElement({xpath: xp})
        .then(function(el) {
          assert(el.click());
        });
    });

    test.it('should have a Bookmarks link', function() {
      let xp = '/html/body/nav/div/div[2]/ul[2]/li[2]/a';
      el = driver.findElement({xpath: xp})
        .then(function(el) {
          assert(el.click());
        });
    });

    test.describe('Indicator Evidence panel', function() {
      test.it('should exist');
    }); // end indicator evidence panel tests

    test.describe('Strategic Objectives panel', function() {
      test.it('should exist');
    }); // end strategic objectives panel tests

    test.describe('Sites panel', function() {
      test.it('should exist');
      test.it('should show map of country selected in Country Dashboard dropdown');
      test.it('should be able to zoom in on the map');
      test.it('should be able to zoom out on the map');
      test.it('should display data points on the Sites map');
    }); // end sites panel tests

    test.describe('Program Projects by Status panel', function() {
      test.it('should exist');
      test.it('should have a project status chart');
    }); // end program projects by status tests

    test.describe('Indicators performance panel', function() {
      test.it('should exist');
      test.it('should have a KPI status chart');
    }); // end indicators performance panel tests
  }); // end TolaActivity dashboard tests

  test.describe('Program Indicators (PI) page', function() {
    test.it('should exist');
    test.it('should have an Indicators link', function() {
      // First let's find the link
      let xp = '/html/body/nav/div/div[2]/ul[1]/li[2]';
      el = driver.findElement({xpath: xp})
        .then(function(el) {
          assert(el.click());
        });
    });

    // Using setTimeout() suggested by https://goo.gl/GP2hLF. Test
    // was executing before the page was loaded and failed because
    // the element wasn't visible or the DOM wasn't fully populated.
    test.it('should open PI page after clicking link', function() {
      setTimeout(function() {
        el = driver.findElement({css: 'h2'})
          .then(function(el) {
            assert.equal(el.getText(), 'Program Indicators');
          });
      }, 5000);
    });
    
    // These are enhancements
    test.it('should highlight PIs with no evidence');
    test.it('should disable Indicators button if program has no indicators');
    test.it('should be able to sort table by clicking a column header');

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
    
    test.describe('Programs dropdown', function() {
      test.it('should exist');
      test.it('should have at least one entry');
      test.it('should default to showing all programs');
      test.it('should be able to filter PIs by Program');
      test.it('should be able to filter Programs by PI');
      test.it('should have same item count as Programs table');
      test.it('should have same items as Programs table');
    }); // end programs dropdown tests
    
    test.describe('Indicators dropdown', function() {
      test.it('should exist');
      test.it('should default to showing all PIs for a program');
      test.it('should be able to filter resultset by PI');
    }); // end indicators dropdown tests
    
    test.describe('Indicator Type dropdown', function() {
      test.it('should exist');
      test.it('should default to showing all Indicator Types for a program');
      test.it('should be able to filter the resultset by Indicator Type');
    }); // end indicator type dropdown tests
    
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
        // TODO: Save changes button complains required fields on the Targets
        // tab aren't filled out when they in fact are
        test.it('should have a Save Changes button');
        // TODO: Reset button does not clear Summary > Country Strategic Objective field
        // if it has been changed
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
  }); // end indicators page tests
});
