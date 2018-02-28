/**
 * Page model for testing the Program Indicators screen.
 * @module targets
 */
// Methods are listed in alphabetical order; please help
// keep them that way. Thanks!
var util = require('../lib/testutil.js');
var dp = require('../lib/testutil.js').dp;
var IndPage = require('../pages/indicators.page.js');
const msec = 1000;

var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

/**
 * Click the indicator data button for the specified indicator
 * @param {string} indicatorName The name of the indicator
 * @returns Nothing
 */
function clickIndicatorDataButton(indicatorName) {
}

/**
 * Click the delete button for the specified indicator
 * @param {string} indicatorName The name of the indicator to delete
 * @returns Nothing
 */
function clickIndicatorDeleteButton(indicatorName) {
}

/**
 * Click the indicator data button for the specified indicator
 * @param {string} indicatorName The name of the indicator to edit
 * @returns Nothing
 */
function clickIndicatorEditButton(indicatorName) {
}

// FIXME: Should this be a per-program method?
/**
 * Click the New Indicator button for the current program
 * @param {string} The name of the indicator
 * @returns Nothing
 */
function clickNewIndicatorButton() {
  browser.waitForVisible('=New Indicator');
  browser.$('=New Indicator').click();
}

/**
 * Click the indicator name link for the specified indicator
 * to show its detail/edit screen
 * @param {string} indicatorName - The name of the indicator whose
 * detail screen you want to view
 * @returns Nothing
 */
function clickProgramIndicator(indicatorName) {
  let link = browser.$('=' + indicatorName);
  link.click();
}

/**
 * Click the specified program's indicators button to toggle the corresponding
 * table of indicators
 * @param {string} programName - The program name whose indicators button
 * you want to click
 * @returns Nothing
 */
function clickProgramIndicatorsButton(programName) {
  IndPage.selectProgram(programName);
}

/***
 * Click the Reset button on the current form to clear any changes
 * @returns Nothing
 */
function clickResetButton() {
  browser.$('input[value="Reset"]').click();
}

/**
 * Click the Targets tab of the indicator detail modal or page
 * @returns Nothing
 */
function clickTargetsTab() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
}

/**
 * Get the text of the current alert message, if any, and return it as a string
 * @returns {string} The current alert message as a string. Fails ugly if the
 * element isn't found.
 */
// FIXME: broken -- doesn't find the <p> tag in the alert div; I think this
// is because the success message flashes through faster than I can catch it
function getAlertMsg() {
  let alertDiv = browser.$('div#alerts');
  let msg = alertDiv.getText();
  return msg;
}

/**
 * Get the current value of the target baseline from the indicators detail screen
 * @returns {integer} The current value of the Baseline text field
 */
function getBaseline() {
  clickTargetsTab();
  let val = $('input#id_baseline').getValue();
  return val;
}

/**
 * Get the contents of the error hint for Baseline value conformance
 * errors
 * @returns {string} The contents of the hint as a string
 */
function getBaselineErrorHint() {
  let errorBox = browser.$('span#hint_id_baseline_na.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/**
 * Get the current indicator name (from the Performance tab)
 * @returns {string} The current value of the indicator name from the Performance
 * tab of the indicator detail screen
 */
function getIndicatorName() {
  clickTargetsTab();
  let val = $('input#id_name').getValue();
  return val;
}

/**
 * Get the contents of the error hint for LoP tarbet conformance errors
 * @returns {string} The contents of the hint as a string
 */
function getLoPErrorHint() {
  let errorBox = browser.$('span#hint_id_lop_target.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/**
 * Get the current LoP target from the the target indicators detail page
 * @returns {integer} The current value of the LoP target field
 */
function getLoPTarget() {
  clickTargetsTab;
  let val = $('input#id_lop_target').getValue();
  return val;
}

/**
 * Get the number of events specified for event-based targets
 * @returns {integer} The number of events specified
 */
function getNumTargetEvents() {
  clickTargetsTab;
  let val = $('input#id_target_frequency_num_periods').getValue();
  util.dp('val='+val);
  return val;
}

/**
 * Get the text, if any, from the error box beneath the number of
 * events text bo
 * @returns {string} The error text as a string
 */
function getNumTargetEventsErrorHint() {
  let errorBox = browser.$('span#hint_id_target_frequency_num_periods.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/**
 * Get the current value of the "Number of target periods" field on the
 * target indicators detail page
 * @returns {integer} The value of the field, if any
 */
function getNumTargetPeriods() {
  clickTargetsTab();
  browser.waitForExist('input#id_target_frequency_num_periods');
  let val = browser.$('input#id_target_frequency_num_periods').getValue();
  return val;
}

/**
 * Get a list of the program indicators for the program currently displayed in
 * the program indicators table
 * @returns {Array<clickable>} returns an array of clickable progrom indicators
 * based on the "Delete" button
 */
// FIXME: should probably returns linkage to all the buttons and links?
function getProgramIndicatorsTable() {
  let link = browser.$('div#toplevel_div').$('div.panel-body').$('a');
  let dataTarget = link.getAttribute('data-target');
  if (browser.isVisible('div#ajaxloading')) {
    browser.waitForVisible('div#ajaxloading', 10*msec, true);
  }
  let table = $('div'+dataTarget).$('table');
  let rows = table.$$('=Delete');
  return rows;
}

/**
 * Get the number of program indicators for the program currently
 * displayed in the progams indicats table
 * @returns {integer} The number of program indicators in the table
 * based on the "Delete" key
 */
// FIXME: should probably returns linkage to all the buttons and links?
function getProgramIndicatorsTableCount() {
  let link = browser.$('div#toplevel_div').$('div.panel-body').$('a');
  let dataTarget = link.getAttribute('data-target');
  if (browser.isVisible('div#ajaxloading')) {
    browser.waitForVisible('div#ajaxloading', 10*msec, true);
  }
  let table = $('div'+dataTarget).$('table');
  let rows = table.$$('=Delete');
  return rows.length;
}

/**
 * Get a list of the program names in the main Program table
 * @returns {Array<string>} returns an array of the text strings of the
 * program names in the programs table
 */
function getProgramsTable() {
  let rows = browser.$('div#toplevel_div').$$('div.panel-heading');
  let programs = new Array();
  for(let row of rows) {
    programs.push(row.$('h4').getText());
  }
  return programs;
}

/**
 * Get a list of the indicator buttons in the main programs table
 * @returns {Array<buttons>} returns an array of clickable "buttons",
 * which are actually anchor (<a />) elements, from the programs table
 */
function getProgramIndicatorButtons() {
  let rows = browser.$('div#toplevel_div').$$('div.panel-body');
  let buttons = new Array();
  for (let row of rows) {
    buttons.push(row.$('a.btn.btn-sm.btn-success'));
  }
  return buttons;
}

/**
 * Get the current error string, if any, from the error box for
 * the target first event name field on the targets tab of the
 * indictor detail screen
 * @returns {string} The error text present, if any
 */
function getTargetFirstEventErrorHint() {
    let errorBox = browser.$('#hint_id_target_frequency_custom.help-block');
    let errorHint = errorBox.getText();
    return errorHint;
}

/**
 * Get the current error string, if any, from the error box for
 * the target first period field on the targets tab of the
 * indictor detail screen
 * @returns {string} The error text present, if any
 */
function getTargetFirstPeriodErrorHint() {
  let errorBox = browser.$('#hint_id_target_frequency_start.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/**
 * Get the currently selected target frequency from the Target Frequency
 * dropdown
 * @returns {string} The currently selected target frequency as a text string
 */
function getTargetFrequency() {
  clickTargetsTab();
  let val = $('select#id_target_frequency').getValue();
  if (val == 0) {
    return '---------';
  } else {
    let list = $('select#id_target_frequency').getText();
    let rows = list.split('\n');
    let result = rows[val];
    return result.trim();
  }
}

/**
 * Get a list of the target value input boxes on a target entry form
 * @returns {Array} A list of input target value input boxes on the
 * current target entry form
 */
function getTargetInputBoxes() {
    // Find the input boxes
    let inputBoxes = browser.$$('input#pt-undefined.form-control.input-value');
    return inputBoxes;
}
/**
 * Get the current error string, if any, from the target creation
 * screen on the Targets tab
 * @returns {string} The error text present, if any
 */
function getTargetValueErrorHint() {
  let errorBox = browser.$('.target-value-error');
  let errorHint = errorBox.getText();
  return errorHint;
}

/**
 * Get the current value of the Unit of measure text field
 * @returns {integer} The current value as an integer
 */
function getUnitOfMeasure() {
  clickTargetsTab();
  let val = $('input#id_unit_of_measure').getValue();
  return val;
}

/**
 * Open the specified page in the browser
 * @param {string} url The URL to display in the browser; defaults
 * to the baseurl value from the config file
 * @returns Nothing
 */
function open(url = parms.baseurl) {
  browser.url(url);
}

// FIXME: This should be a property
/**
 * Return the page title
 * @returns {string} The title of the current page
 */
function pageName() {
  // On this page, the "title" is actually the <h2> caption
  return browser.$('h2').getText();
}

/**
 * Click the "Save changes" button on the Indicator edit screen
 * @returns Nothing
 */
function saveIndicatorChanges() {
  let saveChanges = $('input[value="Save changes"]');
  saveChanges.click();
}

/**
 * Click the "save" button on the new indicator to save a new basic indicator
 * @returns Nothing
 */
function saveNewIndicator() {
  // Accept the default values
  let saveNew = $('form').$('input[value="save"]');
  saveNew.click();
}

/**
 * Type a baseline value into the baseline text field on the Targets
 * tab unless the "Not applicable" check box has been checked
 * @param {integer|boolean} value The non-negative integer baseline
 * value. If set to false, ignore the baseline requirement and check
 * the "Not applicable" check box
 * @returns Nothing
 */
function setBaseline(value) {
  clickTargetsTab();
  let baseline = $('input#id_baseline');
  baseline.setValue(value);
}

/**
 * Click the "Not applicable" checkbox for baseline targets on the
 * indicator detail form
 * @returns Nothing
 */
function setBaselineNA() {
  clickTargetsTab();
  browser.$('#id_baseline_na').click()
}

/**
 * Set the endline target on the targets detail screen to the
 * specifed value
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setEndlineTarget(value) {
  clickTargetsTab();
  if (! browser.isVisible('div>input[name="Endline"]')) {
    browser.waitForVisible('div>input[name="Endline"]');
  }
  let endline = $('div>input[name="Endline"]');
  endline.setValue(value);
}

/**
 * Set the name of the first event to the specified value when
 * working with event-based periodic targets
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setFirstEventName(value) {
  let textBox = browser.$('input#id_target_frequency_custom');
  if (value == 0) {
    textBox.clear();
  } else {
    textBox.setValue(value);
  }
}

/**
 * Sets the date of the first target period to the 1st day of the
 * current month
 * @returns Nothing
 */
function setFirstTargetPeriod() {
  browser.moveToObject('div.controls.col-sm-6>input#id_target_frequency_start');
  browser.moveToObject('div.controls.col-sm-6>input#id_target_frequency_num_periods');
}

/**
 * Type the specified indicator name into the Name field on thei
 * Performance tab of the indicator detail screen
 * @param {string} name The new name for the indicator
 * @returns Nothing
 */
function setIndicatorName(name) {
  if (! browser.isVisible('=Performance')) {
    browser.waitForVisible('=Performance');
  }
  let perfTab = browser.$('=Performance');
  perfTab.click();
  let indName = $('input#id_name');
  indName.setValue(name);
}

/**
 * Type LoP target value name into "Life of Program (LoP) target" text
 * field on the Targets tab of the indicator edit screen
 * @param {string} name The new name for the indicator
 * @returns Nothing
 */
function setLoPTarget(value) {
  clickTargetsTab();
  let lopTarget = $('input#id_lop_target');
  lopTarget.setValue(value);
}

/**
 * Set the midline target on the targets detail screen to the
 * specifed value
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setMidlineTarget(value) {
  clickTargetsTab();
  if (! browser.isVisible('div>input[name="Midline"]')) {
    browser.waitForVisible('div>input[name="Midline"]');
  }
  let midline = $('div>input[name="Midline"]');
  midline.setValue(value);
}

/**
 * Set the number of events to the specified value when working with
 * event-based periodic targets.
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setNumTargetEvents(value) {
  let textBox = browser.$('input#id_target_frequency_num_periods');
  if (value == 0) {
    textBox.clearElement();
  } else {
    textBox.setValue(value);
  }
}

/**
 * Set the number of periods to the specified value when working with
 * interval-based periodic targets
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setNumTargetPeriods(value) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  browser.$('input#id_target_frequency_num_periods').setValue(value);
}

/**
 * Select the target frequency from the Target Frequency dropdown on the
 * the Targets tab of the indicator edit screen
 * @param {string} value The target frequency to select from the dropdown
 * @returns Nothing
 */
function setTargetFrequency(freqName) {
  clickTargetsTab();

  let frequencies = ['', 'Life of Program (LoP) only',
    'Midline and endline', 'Annual', 'Semi-annual',
    'Tri-annual', 'Quarterly', 'Monthly', 'Event'];
  let freqValue = frequencies.indexOf(freqName);
  let targetFreq = $('select#id_target_frequency');
  targetFreq.selectByValue(freqValue);
}

/**
 * Type the unit of measure into the Unit of measure text field on
 * the Targets tab of the indicator edit screen
 * @param {string} unit The new name for the indicator
 * @returns Nothing
 */
function setUnitOfMeasure(unit) {
  clickTargetsTab();
  let bucket = $('input#id_unit_of_measure');
  bucket.setValue(unit);
}

exports.clickIndicatorDataButton = clickIndicatorDataButton;
exports.clickIndicatorDeleteButton = clickIndicatorDeleteButton;
exports.clickIndicatorEditButton = clickIndicatorEditButton;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickProgramIndicator = clickProgramIndicator;
exports.clickProgramIndicatorsButton = clickProgramIndicatorsButton;
exports.clickResetButton = clickResetButton;
exports.clickTargetsTab = clickTargetsTab;
exports.getAlertMsg = getAlertMsg;
exports.getBaseline = getBaseline;
exports.getBaselineErrorHint = getBaselineErrorHint;
exports.getIndicatorName = getIndicatorName;
exports.getLoPErrorHint = getLoPErrorHint;
exports.getLoPTarget = getLoPTarget;
exports.getNumTargetEvents = getNumTargetEvents;
exports.getNumTargetPeriods = getNumTargetPeriods;
exports.getProgramIndicatorsTable = getProgramIndicatorsTable;
exports.getProgramIndicatorsTableCount = getProgramIndicatorsTableCount;
exports.getProgramsTable = getProgramsTable;
exports.getProgramIndicatorButtons = getProgramIndicatorButtons;
exports.getTargetFirstEventErrorHint = getTargetFirstEventErrorHint;
exports.getTargetFirstPeriodErrorHint = getTargetFirstPeriodErrorHint;
exports.getTargetFrequency = getTargetFrequency;
exports.getTargetInputBoxes = getTargetInputBoxes;
exports.getNumTargetEventsErrorHint = getNumTargetEventsErrorHint;
exports.getTargetValueErrorHint = getTargetValueErrorHint;
exports.getUnitOfMeasure = getUnitOfMeasure;
exports.open = open;
exports.pageName = pageName;
exports.saveIndicatorChanges = saveIndicatorChanges;
exports.saveNewIndicator = saveNewIndicator;
exports.setBaseline = setBaseline;
exports.setBaselineNA = setBaselineNA;
exports.setEndlineTarget = setEndlineTarget;
exports.setFirstEventName = setFirstEventName;
exports.setFirstTargetPeriod = setFirstTargetPeriod;
exports.setIndicatorName = setIndicatorName;
exports.setLoPTarget = setLoPTarget;
exports.setMidlineTarget = setMidlineTarget;
exports.setNumTargetEvents = setNumTargetEvents;
exports.setNumTargetPeriods = setNumTargetPeriods;
exports.setTargetFrequency = setTargetFrequency;
exports.setUnitOfMeasure = setUnitOfMeasure;
