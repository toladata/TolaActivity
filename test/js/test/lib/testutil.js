// testutil.js -- Dumping ground for utility methods and objects
// used in testing that don't fit anywhere else

function readConfig(configFile = 'config.json') {
  let fs = require('fs');
  let data = fs.readFileSync(configFile);
  return JSON.parse(data);
}

exports.readConfig = readConfig;
