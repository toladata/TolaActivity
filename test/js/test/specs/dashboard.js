let assert = require('chai').assert;
let LoginPage = require('../pages/login.page.js');
let util = require('../lib/testutil.js');

describe('TolaActivity Dashboard', function() {
  before(function() {
    this.timeout(0);
    browser.windowHandleMaximize();
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
  });

  it('should have a page header', function() {
    browser.waitForVisible('div.panel.panel-default');

    let panel = browser.$('div.panel.panel-default');
    let header = panel.$('div.panel-heading');
    let h4 = header.$('div.row').$('div.col-md-4').$('h4');
    assert(h4.getText() == 'Tola-Activity Dashboard');
  });

  it('should have a TolaActivity link', function() {
    let xp = '/html/body/nav/div/div[1]/a/img';
    let link = $(xp);
    link.click();
  });

  it('should have a Workflow dropdown', function() {
    let link = browser.$('=Workflow');
    assert(link.getText() == 'Workflow');
    link.click();
  });

  it('should have a Country Dashboard dropdown', function() {
    let link = $('button#dropdownMenu1');
    assert(link.getText() == 'Country Dashboard');
    link.click();
  });

  it('should have a Filter by Program link', function() {
    let link = $('button#dropdownMenu3');
    assert(link.getText() == 'Filter by Program');
    link.click();
  });

  it('should have a Form Library dropdown', function() {
    let link = $('=Form Library');
    assert(link.getText() == 'Form Library');
    link.click();
  });

  it('should have a Reports link', function() {
    let navbar = $('div#navbar-collapse-1');
    let link = navbar.$('=Reports');
    assert(link.getText() == 'Reports');
    link.click();
  });

  it('should have a Profile link', function() {
    let xp = '/html/body/nav/div/div[2]/ul[2]/li[1]/a';
    let link = $(xp);
    link.click();
  });

  it('should have a Bookmarks link', function() {
    let link = $('=Bookmarks');
    link.click();
  });

  it('should have an Indicator Evidence panel', function() {
    let xp = '/html/body/div[1]/div[4]/div[1]/div[1]/div[1]';
    let panel = $(xp);
    assert(panel.getText() == 'Indicator Evidence');
  }); // end indicator evidence panel tests

  it('should have a Strategic Objectives panel', function() {
    let xp = '/html/body/div[1]/div[4]/div[1]/div[2]/div[1]';
    let panel = $(xp);
    assert(panel.getText() == 'Strategic Objectives');
  }); // end strategic objectives panel tests

  it('should have a sites panel', function() {
    let xp = '/html/body/div[1]/div[4]/div[2]/div[1]/div/p';
    let panel = $(xp);
    assert(panel.getText() == 'Sites');
  });

  it('should show map of country sites', function() {
    let map = $('#map');
    assert(map.isVisible);
  });

  it('should have a Program Projects by Status panel', function() {
    let panel = $('div.highcharts-0');
    assert(panel.isVisible);
  });

  it('should have a project status chart', function() {
    let panel = $('svg');
    assert(panel.isVisible);
  });

  it('should have an Indicators performance panel', function() {
    let xp = '/html/body/div[1]/div[5]/div/div/div[1]';
    let panel = $(xp);
    assert(panel.getText() == 'Indicators');
  });

  it('should have a KPI status chart', function() {
    let panel = $('div.highcharts-2');
    assert(panel.isVisible);
    let svg = $('svg');
    assert(svg.isVisible);
  });

  // Enhancements?
  it('should be able to zoom in on the map');
  it('should be able to zoom out on the map');
  it('should display data points on the Sites map');
});
