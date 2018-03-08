/**
 * Page model for testing the Program Indicators screen.
 * @module indicators
 */
// Methods are listed in alphabetical order; please help
// keep them that way. Thanks!
const TargetsTab = require('../pages/targets.page.js');
const util = require('../lib/testutil.js');
// milliseconds
const msec = 1000;
var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

/*
 * dropdowns = $$('span.select2-selection--single');
 * programsDropdown = dropdowns[0];
 * indicatorsDropdown = dropdowns[1];
 * indicatorTypesDropdown = dropdowns[2]
*/

/**
 * Click the Export All button on the grid/print report page,
 * saving it in the file specified by fileName
 * @param {string} fileName The name of the output file
 * @returns Nothing
 */
function clickExportAllButton(fileName) {
  let button = $('button[type="submit"]');
  let height = browser.getViewportSize('height');
  browser.scroll(0, 5000);
  button.click();
}
 
/**
 * Click the Indicators dropdown button
 * @returns Nothing
 */
function clickIndicatorsDropdown() {
  let span = $$('span.select2-selection--single')[1];
  let indicatorsDropdown = span.$('span#select2-id_indicators_filter_dropdown-container');
  indicatorsDropdown.click();
}

/**
 * Click the Indicators link on the toolbar
 * @returns Nothing
 */
function clickIndicatorsLink() {
  let indicatorsLink = browser.$('ul.nav.navbar-nav').$('=Indicators');
  indicatorsLink.click();
  browser.waitForVisible('h2=Program Indicators');
}

/**
 * Click the Indicator Type dropdown
 * @returns Nothing
 */
function clickIndicatorTypeDropdown() {
  let span = $$('span.select2-selection--single')[2];
  let indicatorTypesDropdown = span.$('span#select2-id_indicatortypes_filter_dropdown-container');
  indicatorTypesDropdown.click();
}

// FIXME: Should this be a per-program method?
/**
 * Click the New Indicator button for the current program
 * @param {string} The name of the indicator
 * @returns Nothing
 */
function clickNewIndicatorButton() {
  let progList = browser.$$('panel-heading>h4');
  browser.$('=New Indicator').click();
}

/**
 * Click the Programs dropdown button
 * @returns Nothing
 */
function clickProgramsDropdown() {
  let span = $$('span.select2-selection--single')[0];
  let programsDropdown = span.$('span#select2-id_programs_filter_dropdown-container');
  programsDropdown.click();
}

/**
 * Click the Reset button on the current form
 * @returns Nothing
 */
function clickResetButton() {
  browser.$('input[value="Reset"]').click();
}

/**
 * Create a new "basic" indicator. This is just enough of an indicator
 * to be able to save and still be able to modify it in other more
 * specific calls.
 */
function createBasicIndicator() {
  if ($('h2').getText() != 'Program Indicators') {
    clickIndicatorsLink();
  }
  clickNewIndicatorButton();
  saveNewIndicator();
}

/** 
 * Delete the first indicator for the first program currently displayed
 * on the screen
 * @param {string} indName This parameter is currently ignored but reserved
 * for future use.
 * @returns Nothing
 */
function deleteIndicator(indName = 'default') {
    let indButtons = TargetsTab.getProgramIndicatorButtons();
    let indButton = indButtons[0];
    indButton.click();
    let deleteBtns = TargetsTab.getProgramIndicatorsTable();
    let deleteBtn = deleteBtns[0];
    deleteBtn.click();
    let confirmBtn = $('input[value="Confirm"]');
    confirmBtn.click();
}

/** 
 * Edit the first indicator for the first program currently displayed
 * on the screen
 * @param {string} indName This parameter is currently ignored but reserved
 * for future use.
 * @returns Nothing
 */
function editIndicator(indName = 'default') {
    let indButtons = TargetsTab.getProgramIndicatorButtons();
    let indButton = indButtons[0];
    indButton.click();

    let editBtns = TargetsTab.getProgramIndicatorEditButtons();
    let editBtn = editBtns[0];
    editBtn.click();
}

/**
 * Get the text of the current alert message, if any, and return it as a string
 * @returns {string} The current alert message as a string. Fails ugly if the
 * element isn't found.
 */
function getAlertMsg() {
  let alertDiv = browser.$('div#alerts');
  return alertDiv.getText();
}

/**
 * Get the current indicator name (from the Performance tab) on the indicator
 * detail screen
 * @returns {string} The indicator name
 */
function getIndicatorName() {
  let targetsTab = browser.$('=Performance');
  targetsTab.click();
  let val = $('input#id_name').getValue();
  return val;
}

/**
 * Get a list of the indicator types in the Indicator Type dropdown
 * @returns {Array<string>} returns an array of the text strings making up the
 * indicator types dropdown menu
 */
function getIndicatorTypeList() {
  let selectList = browser.$('select#id_indicatortypes_filter_dropdown');
  let listItems = selectList.$$('option');
  let indicatorTypes = new Array();
  for (let listItem of listItems) {
    let s = listItem.getText();
    if (! s.includes('-- All --')) {
      indicatorTypes.push(s);
    }
  }
  return indicatorTypes;
}

/**
 * Get a list of the indicators in the Indicators dropdown
 * @returns {Array<string>} returns an array of the text strings making up the
 * indicators dropdown menu
 */
function getIndicatorsDropdownList() {
  let selectList = browser.$('select#id_indicators_filter_dropdown');
  let listItems = selectList.$$('option');
  let indicators = new Array();
  for (let listItem of listItems) {
    let s = listItem.getText();
    if (! s.includes('-- All --')) {
      indicators.push(s);
    }
  }
  return indicators;
}

/**
 * Get a count of the indicators in the currently displayed program table
 * @returns {integer}j The number of indicators displayed in the program
 * table
 */
function getProgramIndicatorsTableCount(targetId) {
  if (browser.isVisible('div#ajaxloading')) {
    browser.waitForVisible('div#ajaxloading', 10*msec, true);
  }
  let tableDiv = browser.$('div#toplevel_div').$('div.panel');
  let table = tableDiv.$(targetId).$('table.hiddenTable');
  let rows = table.$$('tbody>tr>td>a');
  let rowCnt = 0;
  for (let row of rows) {
    let text = row.getText();
    if (text.length > 0) {
      rowCnt++;
    }
  }
  return rowCnt;
}

/**
 * Get a list of the program name in the Programs dropdown.
 * @returns {Array<string>} an array of the text strings in the Programs 
 * dropdown menu
 */
function getProgramsDropdownList() {
  let selectList = browser.$('select#id_programs_filter_dropdown');
  let listItems = selectList.$$('option');
  let programs = new Array();
  for (let listItem of listItems) {
    let s = listItem.getText();
    if (! s.includes('-- All --'))
      programs.push(s);
    }
    return programs;
}

/**
 * Get a list of the program names in the main Programs table
 * @returns {Array<string>} returns an array of the text strings of the
 * program names in the programs table
 */
function getProgramsTable() {
  let rows = browser.$('div#toplevel_div').$$('div.panel-heading');
  let programs = new Array();
  for(let row of rows) {
    let s = row.$('h4').getText();
    programs.push(s);
  }
  return programs;
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

/**
 * Return the page title
 * @returns {string} The title of the current page
 */
function getPageName() {
  // On this page, the "title" is actually the <h2> caption
  return browser.$('h2').getText();
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
 * Select the specified program from the Programs dropdown
 * @param {string} program The name of the program to select
 * from the Programs dropdown menu
 * @returns Nothing
 */
function selectProgram(program) {
  clickProgramsDropdown();
  let span = $$('span.select2-selection--single')[0];
  let programsDropdown = span.$('span#select2-id_programs_filter_dropdown-container');
  let listItems = programsDropdown.$$('option');
  for (let listItem of listItems) {
    let s = listItem.getText();
    let v = listItem.getValue();
    if (s.includes(program)) {
      selectList.selectByValue(v);
      break;
    }
  }
}

exports.clickExportAllButton = clickExportAllButton;
exports.clickIndicatorsDropdown = clickIndicatorsDropdown;
exports.clickIndicatorsLink = clickIndicatorsLink;
exports.clickIndicatorTypeDropdown = clickIndicatorTypeDropdown;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickProgramsDropdown = clickProgramsDropdown;
exports.clickResetButton = clickResetButton;
exports.createBasicIndicator = createBasicIndicator;
exports.deleteIndicator = deleteIndicator;
exports.editIndicator = editIndicator;
exports.getAlertMsg = getAlertMsg;
exports.getIndicatorName = getIndicatorName;
exports.getIndicatorTypeList = getIndicatorTypeList;
exports.getIndicatorsDropdownList = getIndicatorsDropdownList;
exports.getProgramIndicatorsTableCount = getProgramIndicatorsTableCount;
exports.getProgramsDropdownList = getProgramsDropdownList;
exports.getProgramsTable = getProgramsTable;
exports.open = open;
exports.getPageName = getPageName;
exports.saveNewIndicator = saveNewIndicator;
exports.selectProgram = selectProgram;

