exports.config = {
    specs: [
        './test/specs/**/*.js'
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
    // Capabilities
    maxInstances: 1,
    capabilities: [
        {
            // maxInstances can get overwritten per capability
            browserName: 'chrome',
            //maxInstances: 3,
            chromeOptions: {
                //[]
            }
        },
        {
            browserName: 'firefox',
            maxInstances: 1,
            'moz:firefoxOptions': {
                //[]
             }
        }
    ],
    sync: true,
    logLevel: 'silent',
    coloredLogs: true,
    deprecationWarnings: true,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: [],
    seleniumLogs: './logs',
    framework: 'mocha',
    reporters: ['spec', 'allure'],
    reporterOptions: {
        allure: {
            outputDir: './allure-results'
        }
    },
    mochaOpts: {
        ui: 'bdd',
        compilers: ['js:babel-register']
        //require: 'babel-register'
    }
}
