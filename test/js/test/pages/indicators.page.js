// indicators.page.js -- page object for testing the top-level Program
// Indicators page 
var util = require('../lib/testutil.js');

var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

function clickProgramsDropdown() {
  browser.$('#dropdownProgram').click();
}

function clickIndicatorsDropdown() {
	browser.$('#dropdownIndicator').click();
}

function clickIndicatorTypeDropdown() {
	browser.$('#dropdownIndicatorType').click();
}

function getIndicatorsList() {
  let items = browser.$('#dropdownIndicator>div.btn-group').$('ul.dropdown-menu').$$('li>a');
  let indicators = new Array();
  for (let item of items) {
    indicators.push(item.getText());
	}
	return indicators;
}

function getIndicatorTypeList() {
}

function getProgramsList() {
  let items = browser.$('div.btn-group').$('ul.dropdown-menu').$$('li>a');
  let programs = new Array();
  for (let item of items) {
    programs.push(item.getText());
  }
  return programs;
}

function getProgramsTable() {
  let rows = browser.$('div#toplevel_div').$$('div.panel-heading');
  let programs = new Array();
  for(let row of rows) {
    programs.push(row.$('h4').getText());
  }
  return programs;
}

function open(url = parms.baseurl) {
  browser.url(url);
}

// FIXME: This should be a property
function pageName() {
  // On this page, the "title" is actually the <h2> caption
  return browser.getText('h2=Program Indicators');
}

function selectProgram(program) {
  browser.$('#dropdownProgram').click();
  let items = browser.$('div.btn-group').$('ul.dropdown-menu').$$('li>a');
  for (let item of items) {
    if (program == item.getText()) {
      item.click();
      break;
    }
  }
}

exports.clickProgramsDropdown = clickProgramsDropdown;
exports.clickIndicatorsDropdown = clickIndicatorsDropdown;
exports.clickIndicatorTypeDropdown = clickIndicatorTypeDropdown;
exports.getIndicatorsList = getIndicatorsList;
exports.getProgramsList = getProgramsList;
exports.getProgramsTable = getProgramsTable;
exports.open = open;
exports.pageName = pageName;
exports.selectProgram = selectProgram;

/*
exports.clickIndicatorDataButton = clickIndicatorDataButton;
exports.clickIndicatorDeleteButton = clickIndicatorDeleteButton;
exports.clickIndicatorEditButton = clickIndicatorEditButton;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickPerformanceTab = clickPerformanceTab;
exports.clickProgramIndicatorsButton = selectProgram;
exports.clickSaveChangesButton = clickSaveChangeButton;
exports.clickSaveNewIndicatorButton = clickSaveNewIndicatorButton;
exports.clickTargetsTab = clickTargetsTab;
exports.selectTargetFrequency = selectTargetFrequency;
exports.setBaselineValue = setBaselineValue;
exports.setIndicatorName = setIndicatorName;
exports.setLoPTarget = setLoPTarget;
exports.setUnitOfMeasure = setUnitOfMeasure;
*/
