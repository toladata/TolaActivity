// indicators.page.js -- page object for testing the top-level Program
// Indicators page object model; methods are listed in alphabetical order
// so please help maintain that order.
var util = require('../lib/testutil.js');

var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

/** Click the indicator data button for the specified indicator
 * @param {string} indicatorName The name of the indicator
 * @returns Nothing
 */
function clickIndicatorDataButton(indicatorName) {
}

/** Click the delete button for the specified indicator
 * @param {string} indicatorName The name of the indicator to delete
 * @returns Nothing
 */
function clickIndicatorDeleteButton(indicatorName) {
}

/** Click the indicator data button for the specified indicator
 * @param {string} indicatorName The name of the indicator to edit
 * @returns Nothing
 */
function clickIndicatorEditButton(indicatorName) {
}

/** Click the Indicators dropdown button
 * @returns Nothing
 */
function clickIndicatorsDropdown() {
  browser.$('#dropdownIndicator').click();
}

/** Click the Indicators link on the toolbar
 * @returns Nothing
 */
function clickIndicatorsLink() {
  browser.$('ul.nav.navbar-nav').$('=Indicators').click();
}

/** Click the Indicator Type dropdown
 * @returns Nothing
 */
function clickIndicatorTypeDropdown() {
  browser.$('#dropdownIndicatorType').click();
}

// FIXME: Should this be a per-program method?
/** Click the New Indicator button for the current program
 * @param {string} The name of the indicator
 * @returns Nothing
 */
function clickNewIndicatorButton() {
  browser.waitForVisible('=New Indicator');
  browser.$('=New Indicator').click();
}

/** Click the Programs dropdown
 * @returns Nothing
 */
function clickProgramsDropdown() {
  browser.$('#dropdownProgram').click();
}

/** Clicks the Reset button on the current form
 * @returns Nothing
 */
function clickResetButton() {
  browser.$('input[value="Reset"]').click();
}

/** Create a new basic indicator with the specified required values
 * @param {string} name The new name for the indicator (defaults to "Temporary")
 * @param {string} unit The unit of measurement for this target
 * @param {integer} lopTarget The LoP target for this indicator
 * @param {integer|boolean} Non-zero integer OR false if a baseline is not applicable
 * @param {string} frequency One of the 8 pre-defined periodic intervals
 * @returns Nothing
 */
function createNewProgramIndicator(name, unit, lopTarget, baseline, frequency) {
  clickNewIndicatorButton();
  saveNewIndicator();
  setIndicatorName(name);
  setUnitOfMeasure(unit);
  setLoPTarget(lopTarget);
  setBaseline(baseline);
  setTargetFrequency(frequency);
  saveIndicatorChanges();
}

/** Get the text of the current alert message, if any, and return it as a string
 * @returns {string} The current alert message as a string. Fails ugly if the
 * element isn't found.
 */
function getAlertMsg() {
  let alertDiv = browser.$('div#alerts');
  return alertDiv.$('p').getText();
}

/** Get the current value of the target baseline from the indicators detail screen
 * @returns {integer} The current value of the Baseline text field
 */
function getBaseline() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('input#id_baseline').getValue();
  return val;
}

/** Get the contents of the error hint for Baseline value conformance
 * errors
 * @returns {string} The contents of the hint as a string
 */
function getBaselineErrorHint() {
  let errorBox = browser.$('span#hint_id_baseline_na.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/** Get the current indicator name (from the Performance tab)
 * @returns {string} The current value of the indicator name from the Performance
 * tab of the indicator detail screen
 */
function getIndicatorName() {
  let targetsTab = browser.$('=Performance');
  targetsTab.click();
  let val = $('input#id_name').getValue();
  return val;
}

/** Get a list of the indicator types in the Indicator Type dropdown
 * Returns {Array<string>} returns an array of the text strings making up the
 * indicator types dropdown menu
 */
function getIndicatorTypeList() {
  let list = browser.$('ul.dropdown-menu[aria-labelledby="dropdownIndicatorType"]');
  let listItems = list.$$('li>a');
  let indicatorTypes = new Array();
  for (let listItem of listItems) {
    indicatorTypes.push(listItem.getText());
  }
  return indicatorTypes;
}

/** Get a list of the indicators in the Indicators dropdown
 * Returns {Array<string>} returns an array of the text strings making up the
 * indicators dropdown menu
 */
function getIndicatorsList() {
  let list = browser.$('ul.dropdown-menu[aria-labelledby="dropdownIndicator"]');
  let listItems = list.$$('li>a');
  let indicators = new Array();
  for (let listItem of listItems) {
    indicators.push(listItem.getText());
  }
  return indicators;
}

/** Get the contens of the error hint for LoP tarbet conformance errors
 * @returns {string} The contents of the hint as a string
 */
function getLoPErrorHint() {
  let errorBox = browser.$('span#hint_id_lop_target.help-block');
  let errorHint = errorBox.getText();
  return errorHint;
}

/** Get the current LoP target from the the target indicators detail page
 * @returns {integer} The current value of the LoP target field
 */
function getLoPTarget() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('input#id_lop_target').getValue();
  return val;
}

function getProgramIndicators(programName) {
  selectProgram(programName);
}

/** Get a list of the program names in the Programs dropdown
 * Returns {Array<string>} returns an array of the text strings making up the
 * Programs dropdown menu
 */
function getProgramsList() {
  let list = browser.$('ul.dropdown-menu[aria-labelledby="dropdownProgram"]');
  let listItems = list.$$('li>a');
  let programs = new Array();
  for (let listItem of listItems) {
    programs.push(listItem.getText());
  }
  return programs;
}

/** Get a list of the program names in the main Program table
 * Returns {Array<string>} returns an array of the text strings of the
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

/** Get a list of the indicator buttons in the main programs table
 * Returns {Array<buttons>} returns an array of clickable "buttons",
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

/** Get the currently selected target frequency from the Target Frequency
 *  dropdown
 * @returns {string} The currently selected target frequency as a text string
 */
function getTargetFrequency() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('select#id_target_frequency').getValue();
  return val;
}

/** Get the current value of the Unit of measure text field
 * @returns {integer} The current value as an integer
 */
function getUnitOfMeasure() {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let val = $('input#id_unit_of_measure').getValue();
  return val;
}

/** Open the specified page in the browser
 * @param {string} url The URL to display in the browser; defaults
 * to the baseurl value from the config file
 * @returns Nothing
 */
function open(url = parms.baseurl) {
  browser.url(url);
}

// FIXME: This should be a property
/** Return the page title
 * @returns {string} The title of the current page
 */
function pageName() {
  // On this page, the "title" is actually the <h2> caption
  return browser.$('h2').getText();
}

/** Reload the current page. Just a wrapper around the API call.
 * @returns Nothing
 */
function refresh() {
  browser.refresh();
}

/** Click the "Save changes" button on the Indicator edit screen
 * @returns Nothing
 */
function saveIndicatorChanges() {
  let saveChanges = $('input[value="Save changes"]');
  saveChanges.click();
}

/** Click the "save" button on the new indicator to save a new basic indicator
 * @returns Nothing
 */
function saveNewIndicator() {
  // Accept the default values
  let saveNew = $('form').$('input[value="save"]');
  saveNew.click();
}

/** Select the specified program from the Programs dropdown
 * @param {string} program The name of the program to select
 * from the Programs dropdown menu
 * @returns Nothing
 */
function selectProgram(program) {
  browser.$('#dropdownProgram').click();
  let items = browser.$('div.btn-group').$('ul.dropdown-menu').$$('li>a');
  for (let item of items) {
    let s = item.getText();
    if(s.includes(program)) {
      item.click();
      break;
    }
  }
}

/** Type a baseline value into the baseline text field on the Targets
 * tab unless the "Not applicable" check box has been checked
 * @param {integer|boolean} value The non-negative integer baseline
 * value. If set to false, ignore the baseline requirement and check
 * the "Not applicable" check box
 * @returns Nothing
 */
function setBaseline(value = false) {
  if (value) {
    let targetsTab = browser.$('=Targets');
    targetsTab.click();
    let baseline = $('input#id_baseline');
    baseline.setValue(value);
  } else {
      setBaselineNA();
  }
}

/** Click the "Not applicable" checkbox for baseline target values
 * @returns Nothing
 */
function setBaselineNA() {
  browser.$('#id_baseline_na').click()
}

/** Type the specified indicator name into the Name field on thei
 * Performance tab of the indicator detail screen
 * @param {string} name The new name for the indicator
 * @returns Nothing
 */
function setIndicatorName(name) {
  let perfTab = browser.$('=Performance');
  perfTab.click();
  let indName = $('input#id_name');
  indName.setValue(name);
}

/** Type LoP target value name into "Life of Program (LoP) target" text
 * field on the Targets tab of the indicator edit screen
 * @param {string} name The new name for the indicator
 * @returns Nothing
 */
function setLoPTarget(value) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let lopTarget = $('input#id_lop_target');
  lopTarget.setValue(value);
}

// FIXME: should not be hard-coding the value to select
/** Select the target frequency from the Target Frequency dropdown on the
 *  the Targets tab of the indicator edit screen
 * @param {string} value The target frequency to select from the dropdown
 * @returns Nothing
 */
function setTargetFrequency(value) {
  let targetsTab = browser.$('=Targets');
  targetsTab.click();
  let targetFreq = $('select#id_target_frequency');
  targetFreq.selectByValue(1);
}

/** Type the unit of measure into the Unit of measure text field on
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
exports.clickIndicatorTypeDropdown = clickIndicatorTypeDropdown;
exports.clickIndicatorsDropdown = clickIndicatorsDropdown;
exports.clickIndicatorsLink = clickIndicatorsLink;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickProgramsDropdown = clickProgramsDropdown;
exports.clickResetButton = clickResetButton;
exports.createNewProgramIndicator = createNewProgramIndicator;
exports.getAlertMsg = getAlertMsg;
exports.getBaseline = getBaseline;
exports.getIndicatorsList = getIndicatorsList;
exports.getIndicatorName = getIndicatorName;
exports.getIndicatorTypeList = getIndicatorTypeList;
exports.getLoPErrorHint = getLoPErrorHint;
exports.getLoPTarget = getLoPTarget;
exports.getProgramIndicatorButtons = getProgramIndicatorButtons;
exports.getProgramsList = getProgramsList;
exports.getProgramsTable = getProgramsTable;
exports.getTargetFrequency = getTargetFrequency;
exports.getUnitOfMeasure = getUnitOfMeasure;
exports.open = open;
exports.pageName = pageName;
exports.refresh = refresh;
exports.saveIndicatorChanges = saveIndicatorChanges;
exports.saveNewIndicator = saveNewIndicator;
exports.selectProgram = selectProgram;
exports.setIndicatorName = setIndicatorName;
exports.setUnitOfMeasure = setUnitOfMeasure;
exports.setLoPTarget = setLoPTarget;
exports.setBaseline = setBaseline;
exports.setBaselineNA = setBaselineNA;
exports.setTargetFrequency = setTargetFrequency;

/*
exports.clickPerformanceTab = clickPerformanceTab;
exports.clickTargetsTab = clickTargetsTab;
*/
