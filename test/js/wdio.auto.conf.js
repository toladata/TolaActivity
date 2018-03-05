exports.config = {
    // Specify Test Files
    specs: [
        './test/specs/**/*.js'
    ],
    // Patterns to exclude.
    exclude: [
        //'./test/specs/indicators_*.js'
    ],
    // Capabilities
    maxInstances: 1,
    capabilities: [{
        // maxInstances can get overwritten per capability
        maxInstances: 1,
        browserName: 'chrome'
    },
    {
        maxInstances: 1,
        browserName: 'firefox'
    }],
    // Test Configurations
    sync: true,
    logLevel: 'verbose',
    logOutput: './log',
    coloredLogs: true,
    deprecationWarnings: false,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: ['selenium-standalone'],
    seleniumLogs: './log',
    framework: 'mocha',
    reporters: ['dot', 'allure'],
    reporterOptions: {
        allure: {
            outputDir: './allure-results'
        }
    },
    mochaOpts: {
        ui: 'bdd',
        compilers: ['js:babel-register']
    }
}
