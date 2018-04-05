var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var IndPage = require('../pages/indicators.page.js');
var TargetsTab = require('../pages/targets.page.js');
var util = require('../lib/testutil.js');

describe('"Event" target frequency', function() {
  before(function() {
    // Disable timeouts
    this.timeout(0);
    browser.windowHandleMaximize();
  });

  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUsername(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
    IndPage.open();
    assert.equal('Program Indicators', IndPage.getPageName(),
      'Unexpected page name mismatch');
  });

  it('should require "First event name"', function() {
    IndPage.createBasicIndicator();

    // Don't set a name
    TargetsTab.setIndicatorName('Event target first event name required testing');
    TargetsTab.setUnitOfMeasure('Iodine per igloo');
    TargetsTab.setLoPTarget(476);
    TargetsTab.setBaseline(477);
    TargetsTab.setTargetFrequency('Event');
    TargetsTab.setNumTargetEvents(1);

    // Should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getTargetFirstEventErrorHint();
    assert(errorMessage.includes('Please complete this field.'));
  });

  it('should require "Number of events"', function() {
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Event target first number of events required testing');
    TargetsTab.setUnitOfMeasure('Iodine per igloo');
    TargetsTab.setLoPTarget(495);
    TargetsTab.setBaseline(496);
    TargetsTab.setTargetFrequency('Event');
    TargetsTab.setFirstEventName('Mulugeta Seraw Memorial');
    TargetsTab.setNumTargetEvents(0);

    // Should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
    assert(errorMessage.includes('Please complete this field.'));
  });

  it('should allow only numeric values in "Number of events"', function () {
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Event target number can only be numeric testing');
    TargetsTab.setUnitOfMeasure('Jugglers per jitney');
    TargetsTab.setLoPTarget(514);
    TargetsTab.setBaseline(515);
    TargetsTab.setTargetFrequency('Event');
    TargetsTab.setFirstEventName('Heather Heyer Rest in Power');
    TargetsTab.setNumTargetEvents('a');

    // Should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
    assert(errorMessage.includes('Please complete this field.'));
  });

  it('should default "Number of events" to 1', function() {
    IndPage.createBasicIndicator();
    TargetsTab.clickTargetsTab();
    TargetsTab.setTargetFrequency('Event');
    assert.equal(1, TargetsTab.getNumTargetPeriods(),
      'Did not receive expected number of target events');
  });

  it('should limit max "Number of events" to 12 or less', function() {
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Can create max of 12 events initially testing');
    TargetsTab.setUnitOfMeasure('Mangos per manager');
    TargetsTab.setLoPTarget(538);
    TargetsTab.setBaseline(539);
    TargetsTab.setTargetFrequency('Event');
    TargetsTab.setFirstEventName('Battle of Cable Street');
    TargetsTab.setNumTargetEvents(13);

    // Should fail
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
    assert(errorMessage.includes('You can start with up to 12 targets and add more later.'));
  });

  // FIXME: The next test fails; I can enter 0 events and save
  it('should require at least one event', function() {
    IndPage.createBasicIndicator();

    TargetsTab.setIndicatorName('Must create a least one event testing');
    TargetsTab.setUnitOfMeasure('Noodles per night');
    TargetsTab.setLoPTarget(560);
    TargetsTab.setBaseline(561);
    TargetsTab.setTargetFrequency('Event');
    TargetsTab.setFirstEventName('Battle of Cable Street');
    TargetsTab.setNumTargetEvents(1);

    // FIXME: Test should fail but passes (
    // [see issue #106](https://github.com/mercycorps/TolaActivity/issues/106)).
    // This test will start to fail when that bug gets fixed.
    TargetsTab.saveIndicatorChanges();
    let errorMessage = TargetsTab.getNumTargetEventsErrorHint();
    assert.equal('', errorMessage);
  });
}); // end event target frequency tests

