// indicator.page.js -- page object for testing the top-level Program
// Indicators page 

function openIndicatorsPage(url) {
  browser.url(url);
}

/*
clickProgramIndicatorsButton() vs expandIndicatorsTable()
clickNewIndicatorButton() vs addNewIndicator()
clickSaveNewIndicatorButton() vs saveNewIndicator(0
clickPerformanceTab() vs viewPerformanceTab()
setIndicatorName()
clickTargetsTab() vs fiewTargetsTab()
setUnitOfMeasure()
setLoPTarget()
setBaselineValue()
selectProgramFromDropdown()
selectTargetFrequencyFromDropdown()
clickSaveChangesButton() vs saveChanges()
clickIndicatorEditButton() vs editIndicator()
clickIndicatorDataButton() vs viewIndicatorEvidence()
clickIndicatorDeleteButton() vs deleteIndicator()
*/

exports.clickIndicatorDataButton = clickIndicatorDataButton;
exports.clickIndicatorDeleteButton = clickIndicatorDeleteButton;
exports.clickIndicatorEditButton = clickIndicatorEditButton;
exports.clickNewIndicatorButton = clickNewIndicatorButton;
exports.clickPerformanceTab = clickPerformanceTab;
exports.clickProgramIndicatorsButton = selectProgram;
exports.clickSaveChangesButton = clickSaveChangeButton;
exports.clickSaveNewIndicatorButton = clickSaveNewIndicatorButton;
exports.clickTargetsTab = clickTargetsTab;
exports.selectProgram = selectProgram;
exports.selectTargetFrequency = selectTargetFrequency;
exports.setBaselineValue = setBaselineValue;
exports.setIndicatorName = setIndicatorName;
exports.setLoPTarget = setLoPTarget;
exports.setUnitOfMeasure = setUnitOfMeasure;
