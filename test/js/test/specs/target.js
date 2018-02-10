var assert = require('chai').assert;
var expect = require('chai').expect;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
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
      TargetsTab.clickNewIndicatorButton();
      assert.equal('Create an Indicator', TargetsTab.pageName());
    });

    it('should save the new indicator when the button is clicked', function() {
      TargetsTab.saveNewIndicator();
    });

    it('should have a "Reset" button', function() {
      TargetsTab.clickResetButton();
    });

    it('should clear form when "Reset" button clicked', function() {
      TargetsTab.setIndicatorName('Testing the reset button');
      TargetsTab.setUnitOfMeasure('Clicks');
      TargetsTab.setLoPTarget(38);
      TargetsTab.setBaseline(39);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.clickResetButton();
      assert.equal('Temporary', TargetsTab.getIndicatorName());
      assert.equal('', TargetsTab.getUnitOfMeasure());
      assert.equal('', TargetsTab.getLoPTarget());
      assert.equal('', TargetsTab.getBaseline());
      assert.equal('', TargetsTab.getTargetFrequency());
    });

    it('should save data when "Save changes" button clicked', function() {
      TargetsTab.setIndicatorName('Testing the save changes button');
      TargetsTab.setUnitOfMeasure('Dashes');
      TargetsTab.setLoPTarget(52);
      TargetsTab.setBaseline(53);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
    });
  }); // end new indicator dialog

  // Test cases from issues #21, #24, #25, #30, #33, #35, #37, #42, #43
  describe('Targets tab', function() {
    this.timeout(0);
    it('should require "Unit of measure"', function() {
      // Set everything but the unit of measure then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setIndicatorName('Unit of measure test');
      TargetsTab.setLoPTarget(68);
      TargetsTab.setBaseline(69);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require "Life of Program (LoP) target" value', function() {
      // Set everything but the LoP target then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setUnitOfMeasure('LoP target test');
      TargetsTab.setBaseline(84);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should require target Baseline if "Not applicable" not checked', function() {
      // Set everything but the baseline value then try to save
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setUnitOfMeasure('Baseline value test');
      TargetsTab.setLoPTarget(99);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should *not* require target Baseline if "Not applicable" *is* checked', function() {
      // Set everything but the baseline value
      IndPage.clickIndicatorsLink();
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setUnitOfMeasure('Baseline value not applicable test');
      TargetsTab.setLoPTarget(114);
      TargetsTab.setTargetFrequency('Life of Program (LoP) only');
      // check "Not applicable" then try to save
      TargetsTab.setBaselineNA();
      TargetsTab.saveIndicatorChanges();
      // Should get this success message
      // FIXME: This test fails because the success message is too fast;
      //        I don't know how to catch it with WebDriver
      assert.equal('Success, form data saved.',
                   TargetsTab.getAlertMsg(),
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
      TargetsTab.clickNewIndicatorButton();
      TargetsTab.saveNewIndicator();
      TargetsTab.setUnitOfMeasure('Target frequency test');
      TargetsTab.setLoPTarget(139);
      TargetsTab.setBaseline(140);
      TargetsTab.saveIndicatorChanges();
      // Should get this error message
      assert.equal('Please complete all required fields in the Targets tab.',
                   TargetsTab.getAlertMsg(),
                   'Did not receive expected failure message');
    });

    it('should have 8 options on Target frequency selection menu');

    describe('"Life of Program (LoP) only" target frequency', function() {
      it('should permit only numeric values for LoP target', function() {
        IndPage.clickIndicatorsLink();
        TargetsTab.clickNewIndicatorButton();
        TargetsTab.saveNewIndicator();

        TargetsTab.setIndicatorName('LoP only target testing');
        TargetsTab.setUnitOfMeasure('Furlongs per fortnight');
        TargetsTab.setLoPTarget(158);
        TargetsTab.setBaseline(156);
        TargetsTab.setTargetFrequency('Life of Program (LoP) only');
        // This should succeed
        TargetsTab.saveIndicatorChanges();
      });

      it('should reject non-numeric values for LoP target', function() {
        TargetsTab.setLoPTarget('"166"');
        // This should fail
        TargetsTab.saveIndicatorChanges();
        let errorHint = TargetsTab.getLoPErrorHint();
        assert(errorHint.includes('Please enter a number larger than zero'),
               'Did not receive expected failure message');
        // Make it numeric; this should succeed
        TargetsTab.setLoPTarget(173);
        TargetsTab.saveIndicatorChanges();
        assert.equal(173,
                     TargetsTab.getLoPTarget(),
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
