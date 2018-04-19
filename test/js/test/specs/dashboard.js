import { assert } from 'chai';
import Util from '../lib/testutil';
import LoginPage from '../pages/login.page';
import DashboardPage from '../pages/dashboard.page';
import NavBar from '../pages/navbar.page';

describe('TolaActivity Dashboard', function() {
    before(function() {
        this.timeout(0);
        browser.windowHandleMaximize();
        let parms = Util.readConfig();

        LoginPage.open(parms.baseurl); 
        if (parms.baseurl.includes('mercycorps.org')) {
            LoginPage.username = parms.username;
            LoginPage.password = parms.password;
            LoginPage.login.click();
        } else if (parms.baseurl.includes('localhost')) {
            LoginPage.googleplus.click();
            if ('TolaActivity' != LoginPage.title) {
                LoginPage.gUsername = parms.username + '@mercycorps.org';
                LoginPage.gPassword = parms.password;
            }
        }
    });

    it('should have a page header', function() {
        assert('Tola-Activity Dashboard' == DashboardPage.title);
    });

    it('should have a TolaActivity link', function() {
        assert(NavBar.TolaActivity != null);
        assert(NavBar.TolaActivity != undefined);
        NavBar.TolaActivity.click();
    });

    it('should have a Workflow dropdown', function() {
        assert(NavBar.Workflow != null);
        assert(NavBar.Workflow != undefined);
        NavBar.Workflow.click();
    });

    it('should have a Country Dashboard dropdown', function() {
        DashboardPage.CountryDashboardDropdown.click();
    });

    it('should have a Filter by Program link', function() {
        DashboardPage.FilterByProgramDropdown.click();
    });

    it('should have a Reports dropdown', function() {
        assert(NavBar.Reports != null);
        assert(NavBar.Reports != undefined);
        NavBar.Reports.click();
    });

    it('should have a Profile link', function() {
        assert(NavBar.UserProfile != null);
        assert(NavBar.UserProfile != undefined);
        NavBar.UserProfile.click();
    });

    it('should have a Sites panel', function() {
        assert(DashboardPage.SitesPanel != null);
        assert(DashboardPage.SitesPanel != undefined);
        assert('Sites' == DashboardPage.SitesPanel.getText());
    });

    it('should show map of country sites', function() {
        assert(DashboardPage.SitesMap != null);
        assert(DashboardPage.SitesMap != undefined);
    });

    it('should have a Program Projects by Status panel', function() {
        assert(DashboardPage.ProgramProjectsByStatusPanel != null);
        assert(DashboardPage.ProgramProjectsByStatusPanel != undefined);
    });

    it('should have a project status chart', function() {
        assert(DashboardPage.ProgramProjectsByStatusChart != null);
        assert(DashboardPage.ProgramProjectsByStatusChart != undefined);
    });

    it('should have a KPI Targets vs Actuals panel', function() {
        assert(DashboardPage.KpiTargetsVsActualsPanel != null);
        assert(DashboardPage.KpiTargetsVsActualsPanel != undefined);
    });

    it('should have a KPI Targets vs Actuals chart', function() {
        assert(DashboardPage.KpiTargetsVsActualsChart != null);
        assert(DashboardPage.KpiTargetsVsActualsChart != undefined);
    });

    // Enhancements?
    it('should be able to zoom in on the map');
    it('should be able to zoom out on the map');
    it('should display data points on the Sites map');
});
