var assert = require('chai').assert;
var LoginPage = require('../pages/login.page.js');
var util = require('../lib/testutil.js');
    
describe('TolaActivity Dashboard', function() {
  it('should require unauthenticated users to login', function() {
    let parms = util.readConfig();
    LoginPage.open(parms.baseurl);
    LoginPage.setUserName(parms.username);
    LoginPage.setPassword(parms.password);
    LoginPage.clickLoginButton();
  });

  // after all of that, we should wind up at the dashboard
  it('should have a page header', function() {
    browser.waitForText('h4', 5000)
    var h4 = $('h4');
    assert(h4.getText() == 'Tola-Activity Dashboard');
  });

  it('should have a TolaActivity link', function() {
    var xp = '/html/body/nav/div/div[1]/a/img';
    var link = $(xp);
    link.click();
  });

  it('should have a Workflow dropdown', function() {
    var xp = '/html/body/nav/div/div[2]/ul[1]/li[1]/a';
    var link = $(xp);
    assert(link.getText() == 'Workflow');
    link.click();
  });

  it('should have a Country Dashboard dropdown', function() {
    var link = $('#dropdownMenu1');
    assert(link.getText() == 'Country Dashboard');
    link.click();
  });

  it('should have a Filter by Program link', function() {
    var link = $('#dropdownMenu3');
    assert(link.getText() == 'Filter by Program');
    link.click();
  });

  it('should have a Form Library dropdown', function() {
    var xp = '/html/body/nav/div/div[2]/ul[1]/li[3]/a'
    var link = $(xp);
    assert(link.getText() == 'Form Library');
      
  });
  
  it('should have a Reports link', function() {
    var xp = '/html/body/nav/div/div[2]/ul[1]/li[4]/a'
    var link = $(xp);
    assert(link.getText() == 'Reports');
  });

  it('should have a Profile link', function() {
    var xp = '/html/body/nav/div/div[2]/ul[2]/li[1]/a';
    var link = $(xp);
    link.click();
  });

  it('should have a Bookmarks link', function() {
    var xp = '/html/body/nav/div/div[2]/ul[2]/li[2]/a';
    var link = $(xp);
    link.click();
  });

  describe('Indicator Evidence panel', function() {
    it('should be present on dashboard', function() {
      var xp = '/html/body/div[1]/div[4]/div[1]/div[1]/div[1]';
      var panel = $(xp);
      assert(panel.getText() == 'Indicator Evidence');
    });
  }); // end indicator evidence panel tests

  describe('Strategic Objectives panel', function() {
    it('should be present on dashboard', function() {
      var xp = '/html/body/div[1]/div[4]/div[1]/div[2]/div[1]';
      var panel = $(xp);
      assert(panel.getText() == 'Strategic Objectives');
    });
  }); // end strategic objectives panel tests

  describe('Sites panel', function() {
    it('should be present on dashboard', function() {
      var xp = '/html/body/div[1]/div[4]/div[2]/div[1]/div/p';
      var panel = $(xp);
      assert(panel.getText() == 'Sites');
    });

    it('should show map of country sites', function() {
      var map = $('#map');
      assert(map.isVisible);
    });

    it('should be able to zoom in on the map');
    it('should be able to zoom out on the map');
    it('should display data points on the Sites map');
  }); // end sites panel tests

  describe('Program Projects by Status panel', function() {
    it('should be present on dashboard', function() {
      var panel = $('div.highcharts-0');
      assert(panel.isVisible);
    });

    it('should have a project status chart', function() {
      var panel = $('svg');
      assert(panel.isVisible);
    });
  }); // end program projects by status tests

  describe('Indicators performance panel', function() {
    it('should be present on dashboard', function() {
      var xp = '/html/body/div[1]/div[5]/div/div/div[1]';
      var panel = $(xp);
      assert(panel.getText() == 'Indicators');
    });

    it('should have a KPI status chart', function() {
      var panel = $('div.highcharts-2');
      assert(panel.isVisible);
      var svg = $('svg');
      assert(svg.isVisible);
    });
  }); // end indicators performance panel tests
});
