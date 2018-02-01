var assert = require('chai').assert;
var fs = require('fs');

function readConfig() {
  let data = fs.readFileSync('config.json');
  return JSON.parse(data);
};

describe('TolaActivity Program Indicators page', function() {
  // Disable timeouts
  this.timeout(0);
  var parms = readConfig();

  // TODO: add test
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

  it('should exist', function() {
    browser.url(parms.baseurl + '/indicators/home/0/0/0/');
    browser.waitForText('h2');
    var h2 = $('h2');
    assert.equal(h2.getText(), 'Program Indicators');
  });

  describe('Programs dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownProgram');
      assert(button.getText() == 'Programs');
    });

    it('should have same count on button as in Programs table', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var programs = buttons[0];
      // have to click to make the menu visible
      programs.click();
      var menu = programs.$('ul.dropdown-menu');
      var progList = menu.$$('li');
      programs.click();

      var table = $('div#toplevel_div')
      var tableRows = table.$$('div.panel-heading');
      assert(progList.length === tableRows.length);
    });

    it('should have same items as Programs table', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var dropdown = buttons[0];
      // have to click to make the menu visible
      dropdown.click();
      var dropdownList = dropdown.$('ul.dropdown-menu').$$('li');
      var progList = Array();
      for (let item of dropdownList) {
        var listitem = item.$('a').getText();
        progList.push(listitem.split('-')[1].trim());
      }
      dropdown.click();

      var table = $('div#toplevel_div')
      var tableRows = table.$$('div.panel-heading');
      for (let i = 0; i < tableRows.length; i++) {
        let s = tableRows[i].$('h4').getText().split("\n")[0].trim();
        assert.equal(s, progList[i]);
      };
    });

    it('should filter programs table by selected program name', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var dropdown = buttons[0];
      // have to click to make the menu visible
      dropdown.click();
      var dropdownList = dropdown.$('ul.dropdown-menu').$$('li');
      var item = dropdownList[0];
      var listitem = item.$('a');
      var progName = listitem.getText().split('-')[1].trim();
      item.click();

      // should have a single row in the table
      browser.waitForText('h4');
      var table = $('div#toplevel_div')
      var tableRows = table.$$('div.panel-heading');
      assert.equal(1, tableRows.length);

      // row should be the one selected from the dropdown
      s = tableRows[0].$('h4').getText().split("\n")[0].trim();
      assert.equal(s, progName);
    });
  }); // end programs dropdown tests

  describe('Indicators dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownIndicator');
      assert(button.getText() == 'Indicators');
    });

    it('should have at least one entry', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var indicators = buttons[1];

      // have to click to make the menu visible
      indicators.click();
      var dropdownList = indicators.$('ul.dropdown-menu').$$('li');
      indicators.click();
      assert(dropdownList.length > 0);
    });

    it('should be able to select any/all list items');
  }); // end indicators dropdown tests

  describe('Indicator Type dropdown', function() {
    it('should be present on page', function() {
      var button = $('#dropdownIndicatorType');
      assert(button.getText() == 'Indicator Type');
      button.click();
    });

    it('should have at least one entry', function() {
      var buttons = $('div.panel').$$('div.btn-group');
      var indicatorType = buttons[2];

      // have to click to make the menu visible
      // TODO: Validate the indicator type list as static
      indicatorType.click();
      var dropdownList = indicatorType.$('ul.dropdown-menu').$$('li');
      indicatorType.click();
      assert(dropdownList.length > 0);
    });

    it('should default to showing all Indicator Types for a program');
    it('should be able to filter the resultset by Indicator Type');
  }); // end indicator type dropdown tests

  it('should toggle PIs table by clicking PI Indicators button', function() {
    progIndTable = $('#toplevel_div');
    buttons = progIndTable.$$('div.panel-body');
    for (let button of buttons) {
      // starts out collapsed
      var link = button.$('a');
      var target = link.getAttribute('data-target');
      var state = browser.isVisible('div' + target);
      assert(!state);

      // open it and verify
      button.click();
      state = browser.isVisible('div' + target);
      assert(!state);

      // close it and verify again
      button.click();
      state = browser.isVisible('div' + target);
      assert(!state);
    }
  });

  it('should have matching indicator counts on data button and in table', function() {
    // FIXME: The hard pauses are a poor WAR for the button we want to click sometimes
    // being occluded by another element.
    progIndTable = $('#toplevel_div');
    buttons = progIndTable.$$('div.panel-body');
    for (let button of buttons) {
      var buttonCnt = parseInt(button.$('a').getText());
      var link = button.$('a');
      // expand the table
      link.click();
      browser.pause(500);

      // indicator count from table
      var targetDiv = link.getAttribute('data-target');
      var table = $('div' + targetDiv).$('table');
      var tableRows = table.$$('tbody>tr>td>a');
      // divide by 2 because each <tr> has a blank <tr> spacer row
      // beneath it
      assert.equal(buttonCnt, (tableRows.length / 2), 'evidence count mismatch');

      // collapse the table
      link.click();
      browser.pause(500);
    }
  }, 3); // retry this flaky test 2 more times before failing

  describe('Program Indicators table', function() {
    it('should view PI by clicking its name in Indicator Name column', function() {
      let buttons = $('#toplevel_div').$$('div.panel-body');
      let button = buttons[0];
      let link = button.$('a');
      let target = link.getAttribute('data-target');
      let targetDiv = $('div' + target);
      link.click();
      browser.pause(500);

      let table = targetDiv.$('table');
      let tableRows = table.$$('tbody>tr>td>a.indicator-link');
      let tableRow = tableRows[0];
      let rowText = tableRow.getText();
      // FIXME: This is a horrible hack to accomodate a race.
      // <div id="ajaxloading" class="modal ajax_loading" style="display: block;"></div>
      // obscures the button we want to click, but how long varies because Internet.,
      // so hide the div. :-\
      browser.execute("document.getElementById('ajaxloading').style.visibility = 'hidden';");
      tableRow.click();
      browser.waitForVisible('div#indicator_modal_header>h3');
      let dialogText = $('div#indicator_modal_header>h3').getText().split(':')[1].trim();
      assert.equal(rowText, dialogText, 'indicator name mismatch');
      let close = $('div#indicator_modal_div').$('button.close');
      close.click();
    });

    it('should be able to create PI by clicking the New Indicator button', function() {
      browser.pause(500);
      let newButtons = $('div#toplevel_div').$('div.panel-heading').$$('h4>span>a');
      let newButton = newButtons[0];
      newButton.click();
      assert.equal('Create an Indicator', $('h2').getText());

      // Go with the defaults
      let form = $('form');
      let saveNew = form.$('input.btn.btn-success');
      saveNew.click();
      assert.equal('Success, Basic Indicator Created!',
                   $('div.alert.alert-success').getText());

      // Find the Performance tab
      let tabs = $$('li.tab-pane>a');
      let perfTab = tabs[1];
      let indName = $('input#id_name');
      assert.equal('Performance', perfTab.getText());
      perfTab.click();
      // A name unlikely to clash with real data
      indName.setValue('===> Delete Me! <===');

      // Find the Targets tab
      let targetsTab = tabs[2];
      assert.equal('Targets', targetsTab.getText());
      targetsTab.click();

      // Add some values
      let bucket = $('input#id_unit_of_measure');
      bucket.setValue('Buckets');
      let lopTarget = $('input#id_lop_target');
      lopTarget.setValue('10');
      let baseline = $('input#id_baseline');
      baseline.setValue('0');
      let targetFreq = $('select#id_target_frequency');
      targetFreq.selectByValue(1);

      // Save
      let saveChanges = $('input.btn.btn-primary');
      assert.equal('Save changes', saveChanges.getValue());
      saveChanges.click();
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
});
