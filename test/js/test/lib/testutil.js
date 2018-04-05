/**
 * Hodgepodge of helper code that doesn't fit elsewhere
 * @module testutil
 */

/**
 * Read the configuration file to get user session data (username,
 * password, base URL)
 * @param {string} configFile - Path to config file; defaults to config.json
 * @returns {JSON} - JSON object containing user session data
 */
function readConfig(configFile = 'config.json') {
    let fs = require('fs');
    let data = fs.readFileSync(configFile);
    return JSON.parse(data);
}

/**
 * Print the specific string to the console
 * @param {string} s The string to print
 * @returns Nothing
 */
function dp(s) { console.log('***%s***', s); }

exports.dp = dp;
exports.readConfig = readConfig;
