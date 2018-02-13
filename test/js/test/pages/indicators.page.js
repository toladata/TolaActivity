/**
 * Page model for testing the Program Indicators screen.
 * @module indicators
 */
// Methods are listed in alphabetical order; please help
// keep them that way. Thanks!
const msec = 1000;

var util = require('../lib/testutil.js');

var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

/**
 * Click the Indicators dropdown button
 * @returns Nothing
 */
function clickIndicatorsDropdown() {
  browser.$('#dropdownIndicator').click();
}

/**
 * Click the Indicators link on the toolbar
 * @returns Nothing
 */
function clickIndicatorsLink() {
  browser.$('ul.nav.navbar-nav').$('=Indicators').click();
}

/**
 * Click the Indicator Type dropdown
 * @returns Nothing
 */
function clickIndicatorTypeDropdown() {
  browser.$('#dropdownIndicatorType').click();
}

/**
 * Click the Programs dropdown
 * @returns Nothing
 */
function clickProgramsDropdown() {
  browser.$('#dropdownProgram').click();
}

/**
 * Click the Reset button on the current form
 * @returns Nothing
 */
function clickResetButton() {
  browser.$('input[value="Reset"]').click();
}

/**
 * Get the text of the current alert message, if any, and return it as a string
 * @returns {string} The current alert message as a string. Fails ugly if the
 * element isn't found.
 */
function getAlertMsg() {
  let alertDiv = browser.$('div#alerts');
  return alertDiv.$('p').getText();
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
 * Get a list of the indicator types in the Indicator Type dropdown
 * @returns {Array<string>} returns an array of the text strings making up the
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

/**
 * Get a list of the indicators in the Indicators dropdown
 * @returns {Array<string>} returns an array of the text strings making up the
 * indicators dropdown menu
 */
function getIndicatorsDropdownList() {
  let list = browser.$('ul.dropdown-menu[aria-labelledby="dropdownIndicator"]');
  let listItems = list.$$('li>a');
  let indicators = new Array();
  for (let listItem of listItems) {
    indicators.push(listItem.getText());
  }
  return indicators;
}

/**
 * Get a list of the program names in the Programs dropdown
 * @returns {Array<string>} returns an array of the text strings making up the
 * Programs dropdown menu
 */
function getProgramsDropdownList() {
	clickProgramsDropdown();
  let list = browser.$('ul.dropdown-menu[aria-labelledby="dropdownProgram"]');
  let listItems = list.$$('li>a');
  let programs = new Array();
  for (let listItem of listItems) {
	  if (! listItem.getText().includes('-- All --')) {
	    programs.push(listItem.getText());
		}
  }
	clickProgramsDropdown();
	return programs;
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
 * Select the specified program from the Programs dropdown
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

exports.clickIndicatorsDropdown = clickIndicatorsDropdown;
exports.clickIndicatorsLink = clickIndicatorsLink;
exports.clickIndicatorTypeDropdown = clickIndicatorTypeDropdown;
exports.clickProgramsDropdown = clickProgramsDropdown;
exports.clickResetButton = clickResetButton;
exports.getAlertMsg = getAlertMsg;
exports.getIndicatorName = getIndicatorName;
exports.getIndicatorTypeList = getIndicatorTypeList;
exports.getIndicatorsDropdownList = getIndicatorsDropdownList;
exports.getProgramsDropdownList = getProgramsDropdownList;
exports.getProgramsTable = getProgramsTable;
exports.open = open;
exports.pageName = pageName;
exports.selectProgram = selectProgram;

