/**
 * "Page" model for testing the indicator evidence table
 * @module Evidence
 */
'use strict';

/**
 * Get the LoP target from the bottom of an indicator's evidence table.
 * @returns {integer} The value of the LoP target field
 */
function getLoPTarget() {
  let val = $('input#id_lop_target').getValue();
  return val;
}

function getSumOfTargets() {
    return false;
}

function getTargetsTable() {
    return false;
}

function getTargetPeriodValue(period, val) {
    return false;
}

function setTargetPeriodValue(period, val) {
    return false;
}

// Function exports
exports.getLoPTarget = getLoPTarget;
exports.getSumOfTargets = getSumOfTargets;
exports.getTargetsTable = getTargetsTable;
exports.getTargetPeriodValue = getTargetPeriodValue;
exports.setTargetPeriodValue = setTargetPeriodValue;

