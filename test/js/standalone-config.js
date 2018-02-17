module.exports = {
  baseURL: 'https://selenium-release.storage.googleapis.com',
  version: '3.9.1',
  drivers: {
    chrome: {
      version: '2.33',
      arch: process.arch,
      baseURL: 'https://chromedriver.storage.googleapis.com'
  },
    firefox: {
      version: '0.19.1',
      arch: process.arch,
      baseURL: 'https://github.com/mozilla/geckodriver/releases/download'
  },
}

