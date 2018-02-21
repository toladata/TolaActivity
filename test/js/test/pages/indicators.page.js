/**
 * Page model for testing the Program Indicators screen.
 * @module indicators
 */
// Methods are listed in alphabetical order; please help
// keep them that way. Thanks!

var util = require('../lib/testutil.js');
var parms = util.readConfig();

// milliseconds
const msec = 1000;
parms.baseurl += '/indicators/home/0/0/0';

/*
 * dropdowns = $$('span.select2-selection--single');
 * programsDropdown = dropdowns[0];
 * indicatorsDropdown = dropdowns[1];
 * indicatorTypesDropdown = dropdowns[2]
*/

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
 * Get the number of program indicators for the table in a div named
 * targetId. This is the program indicators table for the the given
 * program.
 * @param {string} targetId The target div containing the table you
 * want to enumerate
 * @returns {integer} The number of indicators in the specified table
 */
function getProgramIndicatorsTableCount(targetId) {
  let container = browser.$('div#toplevel_div').$('div.panel.panel-default');
  let s = 'div' + targetId;
  let tableDiv = container.$(s)
  if (! browser.isVisible(s)) {
    browser.waitForVisible(s, 10*msec);
  }
  /*
  */
  let table = tableDiv.$('table.table.table-striped.hiddenTable');
  let tbody = table.$('tbody');
  let tableRows = tbody.$$('tr')
  let rowCnt = 0;
  for (let row of tableRows) {
    //let text = row.getText();
    //if (text.length > 0) {
    //  rowCnt++;
    //}
    let cells = row.$$('td');
    for (let cell of cells) {
      let link = cell.$('a.indicator-link');
      if (! link == undefined) { rowCnt++; }
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

exports.clickIndicatorsDropdown = clickIndicatorsDropdown;
exports.clickIndicatorsLink = clickIndicatorsLink;
exports.clickIndicatorTypeDropdown = clickIndicatorTypeDropdown;
exports.clickProgramsDropdown = clickProgramsDropdown;
exports.clickResetButton = clickResetButton;
exports.getAlertMsg = getAlertMsg;
exports.getIndicatorName = getIndicatorName;
exports.getIndicatorTypeList = getIndicatorTypeList;
exports.getIndicatorsDropdownList = getIndicatorsDropdownList;
exports.getProgramIndicatorsTableCount = getProgramIndicatorsTableCount;
exports.getProgramsDropdownList = getProgramsDropdownList;
exports.getProgramsTable = getProgramsTable;
exports.open = open;
exports.pageName = pageName;
exports.selectProgram = selectProgram;

