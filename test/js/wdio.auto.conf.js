exports.config = {
    // Specify Test Files
    specs: [
        './test/specs/**/*.js'
    ],
    // Patterns to exclude.
    exclude: [
        // 'path/to/excluded/files'
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
    logOutput: 'webdriver.log',
    coloredLogs: true,
    deprecationWarnings: false,
    bail: 0,
    screenshotPath: './errorShots/',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: ['selenium-standalone'],
    seleniumLogs: './logs',
    framework: 'mocha',
    reporters: ['dot', 'concise', 'allure'],
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
