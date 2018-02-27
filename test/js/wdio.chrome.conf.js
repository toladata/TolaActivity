exports.config = {
    execArgv: ['--inspect'],
    specs: [
        './test/specs/**/*.js'
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
    // Capabilities
    maxInstances: 1,
    capabilities: [{
        // maxInstances can get overwritten per capability
        browserName: 'chrome',
        maxInstances: 1,
        chromeOptions: {
            //[]
        }
    }],
    sync: true,
    logLevel: 'silent',
    logOutput: './log',
    coloredLogs: true,
    deprecationWarnings: false,
    bail: 0,
    screenshotPath: './errorShots',
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 90000,
    connectionRetryCount: 3,
    services: [],
    seleniumLogs: './log',
    framework: 'mocha',
    reporters: ['dot', 'spec', 'allure'],
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
