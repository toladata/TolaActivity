/**
 * Page model and methods for the TolaActivity home page or
 * dashboard
 * @module DashboardPage
 */
'use strict';
import Page from './page';
import Util from '../lib/testutil';

class DashboardPage extends Page {
    get title() {
        browser.waitForVisible('div.panel.panel-default');

        let panel = browser.$('div.panel.panel-default');
        let header = panel.$('div.panel-heading');
        let h4 = header.$('div.row').$('div.col-md-4').$('h4');
        return h4.getText();
    }
    get CountryDashboardDropdown() { return $('button#dropdownMenu1'); }
    get FilterByProgramDropdown() { return $('button#dropdownMenu3'); }
    get IndicatorEvidencePanel() { return $('/html/body/div[1]/div[4]/div[1]/div[1]/div[1]'); }
    get StrategicObjectivesPanel() { return $('/html/body/div[1]/div[4]/div[1]/div[2]/div[1]'); }
    get SitesPanel() { return $('/html/body/div[1]/div[4]/div[2]/div[1]/div/p'); }
    get SitesMap() { return $('#map'); }
    get ProgramProjectsByStatusPanel() { return $('div#highcharts-0'); }
    get ProgramProjectsByStatusChart() { return $('div#highcharts-0').$('svg'); }
    get KpiTargetsVsActualsPanel() { return $('div#highcharts-2'); }
    get KpiTargetsVsActualsChart() { return $('div#highcharts-2').$('svg'); }

    open() {
        let parms = Util.readConfig();
        super.open(parms.baseurl);
    }
}
export default new DashboardPage();
