var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var util = require('../lib/testutil.js');

describe('Indicator Targets', function() {
  // Disable timeouts
  this.timeout(0);

  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    assert.equal('Program Indicators', IndPage.pageName());
  });

  describe('Create new indicator dialog', function() {
    this.timeout(0);
    it('should open new indicator form when button is clicked', function() {
      IndPage.clickNewIndicatorButton();
      assert.equal('Create an Indicator', IndPage.pageName());
    });

    it('should save the new indicator when the button is clicked', function() {
      IndPage.saveNewIndicator();
    });

    it('should have a "Reset" button', function() {
      IndPage.clickResetButton();
    });

    it('should clear form when "Reset" button clicked', function() {
      IndPage.setIndicatorName('Testing the reset button');
      IndPage.setUnitOfMeasure('Clicks');
      IndPage.setLoPTarget(38);
      IndPage.setBaseline(39);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      IndPage.clickResetButton();
      assert.equal('Temporary', IndPage.getIndicatorName());
      assert.equal('', IndPage.getUnitOfMeasure());
      assert.equal('', IndPage.getLoPTarget());
      assert.equal('', IndPage.getBaseline());
      assert.equal('', IndPage.getTargetFrequency());
    });

    it('should save data when "Save changes" button clicked', function() {
      IndPage.setIndicatorName('Testing the save changes button');
      IndPage.setUnitOfMeasure('Dashes');
      IndPage.setLoPTarget(52);
      IndPage.setBaseline(53);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      IndPage.saveIndicatorChanges();
    });
  }); // end new indicator dialog

  // Test cases from issues #21, #24, #25, #30, #33, #35, #37, #42, #43
  describe('Targets tab', function() {
    this.timeout(0);
    it('should require "Unit of measure"', function() {
      // Set everything but the unit of measure then try to save
      IndPage.clickIndicatorsLink();
      IndPage.clickNewIndicatorButton();
      IndPage.saveNewIndicator();
      IndPage.setIndicatorName('Unit of measure test');
      IndPage.setLoPTarget(68);
      IndPage.setBaseline(69);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      IndPage.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   IndPage.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require "Life of Program (LoP) target" value', function() {
      // Set everything but the LoP target then try to save
      IndPage.clickIndicatorsLink();
      IndPage.clickNewIndicatorButton();
      IndPage.saveNewIndicator();
      IndPage.setUnitOfMeasure('LoP target test');
      IndPage.setBaseline(84);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      IndPage.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   IndPage.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require target Baseline if "Not applicable" not checked', function() {
      // Set everything but the baseline value then try to save
      IndPage.clickIndicatorsLink();
      IndPage.clickNewIndicatorButton();
      IndPage.saveNewIndicator();
      IndPage.setUnitOfMeasure('Baseline value test');
      IndPage.setLoPTarget(99);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      IndPage.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   IndPage.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should *not* require target Baseline if "Not applicable" *is* checked', function() {
      // Set everything but the baseline value
      IndPage.clickIndicatorsLink();
      IndPage.clickNewIndicatorButton();
      IndPage.saveNewIndicator();
      IndPage.setUnitOfMeasure('Baseline value not applicable test');
      IndPage.setLoPTarget(114);
      IndPage.setTargetFrequency('Life of Program (LoP) only');
      // check "Not applicable" then try to save
      IndPage.setBaselineNA();
      IndPage.saveIndicatorChanges();
      // Should get this success message
      // FIXME: This test fails because the success message is too fast;
      //        I don't know how to catch it with WebDriver
      assert.equal('Success, form data saved.',
                   IndPage.getAlertMsg(),
                   'Did not receive expected success message');
      // Should not get this message
      // FIXME: I'd rather not use the negative logic; much prefer the
      //        positive form above if it can be made to work
      assert.notEqual('Please complete all required fields in the Targets tab.',
                       IndPage.getAlertMsg(),
                       'Received unexpected error message');
    });

    it('should require Target frequency', function() {
      // Set everything but the target frequency then try to save
      IndPage.clickIndicatorsLink();
      IndPage.clickNewIndicatorButton();
      IndPage.saveNewIndicator();
      IndPage.setUnitOfMeasure('Target frequency test');
      IndPage.setLoPTarget(139);
      IndPage.setBaseline(140);
      IndPage.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   IndPage.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should have 8 options on Target frequency selection menu');

    describe('"Life of Program (LoP) only" target frequency', function() {
      it('should permit only numeric values for LoP target', function() {
        IndPage.clickIndicatorsLink();
        IndPage.clickNewIndicatorButton();
        IndPage.saveNewIndicator();

        IndPage.setIndicatorName('LoP only target testing');
        IndPage.setUnitOfMeasure('Furlongs per fortnight');
        IndPage.setLoPTarget(158);
        IndPage.setBaseline(156);
        IndPage.setTargetFrequency('Life of Program (LoP) only');
        // This should succeed
        IndPage.saveIndicatorChanges();
      });

      it('should reject non-numeric values for LoP target', function() {
        IndPage.setLoPTarget('"166"');
        // This should fail
        IndPage.saveIndicatorChanges();
        let errorHint = IndPage.getLoPErrorHint();
        assert(errorHint.includes('Please enter a number larger than zero'),
               'Did not receive expected failure message');
        // Make it numeric; this should succeed
        IndPage.setLoPTarget(173);
        IndPage.saveIndicatorChanges();
        assert.equal(173,
                     IndPage.getLoPTarget(),
                     'Did not receive expected value from getLoPTarget()');
      });

      // FIXME: Are these 2 test cases still important?
      it('should permit non-numeric values only in legacy data for LoP target');
      it('should require numeric value for LoP target if non-numeric legacy data is modified');
    });

    describe('"Midline and endline" target frequency', function() {
      it('should require value in Midline target field');
      it('should require value in Endline target field');
    });

    describe('"Annual" target frequency', function() {
      it('should require date that first target period begins');
      it('should require the number of target periods to create');
      it('should require entering targets for each target period')
    });

    describe('"Semi-annual" target frequency', function() {
      it('should require date that first target period begins');
      it('should require the number of target periods to create');
      it('should require entering targets for each target period');
    });

    describe('"Tri-annual" target frequency', function() {
      it('should require date that first target period begins');
      it('should require the number of target periods to create');
      it('should require entering targets for each target period');
    });

    describe('"Quarterly" target frequency', function() {
      it('should require date that first target period begins');
      it('should require the number of target periods to create');
      it('should require entering targets for each target period');
    });

    describe('"Monthly" target frequency', function() {
      it('should require date that first target period begins');
      it('should require the number of target periods to create');
      it('should require entering targets for each target period');
    });

    describe('"Event" target frequency', function() {
      it('should require "First event name"');
      it('should require "Number of events"');
      it('should allow only numeric values in "Number of events"');
      it('should default "Number of events" to 1');
      it('should limit "Number of events" between 1 and 12 inclusive');
      // FIXME: The next test fails; I can enter 0 events and save
      it('should require at least one event');
      it('should inform user that only 12 events can be created at once');
    });
  }); // end test cases from GitHub issues
});
