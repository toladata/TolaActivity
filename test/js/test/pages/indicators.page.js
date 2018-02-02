// indicators.page.js -- page object for testing the top-level Program
// Indicators page 
var util = require('../lib/testutil.js');

var parms = util.readConfig();
parms.baseurl += '/indicators/home/0/0/0';

function open(url = parms.baseurl) {
  browser.url(url);
}

exports.open = open;
/*
exports.clickProgramsDropdown = clickProgramsDropdown;
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
