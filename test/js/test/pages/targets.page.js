/**
 * Page model for testing the Program Indicators screen.
 * @module targets
 */
// Methods are listed in alphabetical order; please help
// keep them that way. Thanks!
const msec = 1000;

var util = require('../lib/testutil.js');
var dp = require('../lib/testutil.js').dp;
var selectProgram = require('../pages/indicators.page.js').selectProgram
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
 * Click the specified program's Indicators button to toggle the corresponding
 * table of indicators
 * @param {string} programName - The program name whose Indicators button
 * you want to click
 * @returns Nothing
 */
function clickProgramIndicatorsButton(programName) {
  selectProgram(programName);
  // find indicators button
  // click it
}

function clickResetButton() {
  browser.$('input[value="Reset"]').click();
}

/**
 * Create a new basic indicator with the specified required values
 * @param {string} name The new name for the indicator
 * @param {string} unit The unit of measurement for this target
 * @param {integer} lopTarget The LoP target for this indicator
 * @param {integer|boolean} Integer > 0 OR false if baseline is not applicable
 * @param {string} frequency One of the 8 pre-defined periodic intervals
 * @returns Nothing
 */
function createNewProgramIndicator(name, unit, lopTarget,
                                   baseline = false,
                                   frequency = 'Life of Program (LoP) only') {
  clickNewIndicatorButton();
  saveNewIndicator();
  setIndicatorName(name);
  setUnitOfMeasure(unit);
  setLoPTarget(lopTarget);
  if (baseline) {
    setBaseline(baseline);
  } else {
    setBaselineNA();
  }
  setTargetFrequency(frequency);
  saveIndicatorChanges();
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
  return alertDiv.$('p').getText();
}

/**
 * Get the current value of the target baseline from the indicators detail screen
 * @returns {integer} The current value of the Baseline text field
 */
function getBaseline() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
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
  let targetsTab = browser.$('=Performance');
  targetsTab.click();
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
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('input#id_lop_target').getValue();
  return val;
}

/**
 * Get the current value of the "Number of target periods" field on the
 * target indicators detail page
 * @returns {integer} The value of the field, if any
 */
function getNumTargetPeriods() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('input#id_target_frequency_num_periods').getValue();
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
 * Get the currently selected target frequency from the Target Frequency
 * dropdown
 * @returns {string} The currently selected target frequency as a text string
 */
function getTargetFrequency() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('select#id_target_frequency').getValue();
  return val;
}

function getTargetFirstPeriodErrorHint() {
  let errorBox = browser.$('#hint_id_target_frequency_start');
  let errorHint = errorBox.getText();
  return errorHint;
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
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
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
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let baseline = $('input#id_baseline');
  baseline.setValue(value);
}

/**
 * Click the "Not applicable" checkbox for baseline targets on the
 * indicator detail form
 * @returns Nothing
 */
function setBaselineNA() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  browser.$('#id_baseline_na').click()
}

/**
 * Set the endline target on the targets detail screen to the
 * specifed value
 * @param {integer} value The value to set
 * @returns Nothing
 */
function setEndlineTarget(value) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  if (! browser.isVisible('div>input[name="Endline"]')) {
    browser.waitForVisible('div>input[name="Endline"]');
  }
  let endline = $('div>input[name="Endline"]');
  endline.setValue(value);
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
  let targetsTab = $('=Targets');
  targetsTab.click();
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
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  if (! browser.isVisible('div>input[name="Midline"]')) {
    browser.waitForVisible('div>input[name="Midline"]');
  }
  let midline = $('div>input[name="Midline"]');
  midline.setValue(value);
}

function setNumTargetPeriods(value) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  $('input#id_target_frequency_num_periods').setValue(value);
}

/**
 * Select the target frequency from the Target Frequency dropdown on the
 * the Targets tab of the indicator edit screen
 * @param {string} value The target frequency to select from the dropdown
 * @returns Nothing
 */
function setTargetFrequency(freqName) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();

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
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let bucket = $('input#id_unit_of_measure');
  bucket.setValue('Buckets');
}

exports.clickIndicatorDataButton = clickIndicatorDataButton;
exports.clickIndicatorDeleteButton = clickIndicatorDeleteButton;
exports.clickIndicatorEditButton = clickIndicatorEditButton;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickProgramIndicator = clickProgramIndicator;
exports.clickProgramIndicatorsButton = clickProgramIndicatorsButton;
exports.clickResetButton = clickResetButton;
exports.createNewProgramIndicator = createNewProgramIndicator;
exports.getAlertMsg = getAlertMsg;
exports.getBaseline = getBaseline;
exports.getBaselineErrorHint = getBaselineErrorHint;
exports.getIndicatorName = getIndicatorName;
exports.getLoPErrorHint = getLoPErrorHint;
exports.getLoPTarget = getLoPTarget;
exports.getNumTargetPeriods = getNumTargetPeriods;
exports.getProgramIndicatorsTable = getProgramIndicatorsTable;
exports.getProgramIndicatorsTableCount = getProgramIndicatorsTableCount;
exports.getProgramsTable = getProgramsTable;
exports.getProgramIndicatorButtons = getProgramIndicatorButtons;
exports.getTargetFrequency = getTargetFrequency;
exports.getTargetFirstPeriodErrorHint = getTargetFirstPeriodErrorHint;
exports.getTargetValueErrorHint = getTargetValueErrorHint;
exports.getUnitOfMeasure = getUnitOfMeasure;
exports.open = open;
exports.pageName = pageName;
exports.saveIndicatorChanges = saveIndicatorChanges;
exports.saveNewIndicator = saveNewIndicator;
exports.setBaseline = setBaseline;
exports.setBaselineNA = setBaselineNA;
exports.setEndlineTarget = setEndlineTarget;
exports.setIndicatorName = setIndicatorName;
exports.setLoPTarget = setLoPTarget;
exports.setMidlineTarget = setMidlineTarget;
exports.setNumTargetPeriods = setNumTargetPeriods;
exports.setTargetFrequency = setTargetFrequency;
exports.setUnitOfMeasure = setUnitOfMeasure;
