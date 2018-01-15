# Environment Canada Federal Contaminated Sites Inventory (FCSI) XML parser/exporter
# Tested with Python 2.7.10
# Created by Randal Greene (rgreene@feaverslane.com), January 2018

# Input: XML dump of contaminated sites, described at https://www.tbs-sct.gc.ca/fcsi-rscf/home-accueil-eng.aspx and
#        downloaded from https://www.tbs-sct.gc.ca/fcsi-rscf/opendata-eng.aspx
# Output: CSV tables that can be imported into a relational database system or GIS software
# Note: Exports UTF-8 encoding; non-ASCII characters will display incorrectly in Excel, which assumes UTF-16
#       Force Site ID to be quoted (string) because initial row appears numeric, but it is alphanumeric in some rows
#       To output French text, search and replace 'EN' with 'FR'; you may also want to translate field names
#       Some sites have no lat/lon, even though LocationMiniMapURL shows a point for them!
#       Consider enhancement to extract the following repeating values into lookup tables:
#           Classification
#           ReasonForFederalInvolvement
#           ManagementType
#           Contamination
#           Medium

# License: CC-BY-SA (see https://creativecommons.org/licenses/by-sa/4.0/legalcode)


import xml.etree.ElementTree as ET
import unicodecsv as csv


# replace with appropriate local path
starting_path = 'C:/GIS/ECCC/FCSI/'


# function to check for optional element, with optional sub-element and sub-sub-element, and return element text
# check for both the "doesn't exist" case and the "empty element" case (although it appears the data only has latter)
def optional_element_lookup(parent_element, element_name, sub_element_name=None, sub_sub_element_name=None):
    ret = ''
    element = parent_element.find(element_name)
    if element is not None:
        if sub_element_name is not None:
            sub_element = element.find(sub_element_name)
            if sub_element is not None:
                if sub_sub_element_name is not None:
                    sub_sub_element = sub_element.find(sub_sub_element_name)
                    if sub_sub_element is not None:
                        if sub_sub_element.text is not None:
                            ret = sub_sub_element.text
                else:
                    if sub_element.text is not None:
                        ret = sub_element.text
        else:
            if element.text is not None:
                ret = element.text
    return ret


# main logic
root = ET.parse(starting_path + 'fcsi-rscf.xml').getroot()

# ReportingOrganizations
with open(starting_path + 'reporting_organization.csv', 'wb') as reporting_organization_file:
    reporting_organization_writer = csv.writer(reporting_organization_file, dialect='excel', encoding='utf-8')
    # column headers
    reporting_organization_writer.writerow(['ReportingOrganizationCode',
                                            'ReportingOrganizationName'])
    # data rows
    for reporting_organizations in root.findall('ReportingOrganizations'):
        for reporting_organization in reporting_organizations.findall('ReportingOrganization'):
            reporting_organization_writer.writerow([reporting_organization.find('Code').text,
                                                    reporting_organization.find('EN').text])

# Sites
try:
    site_file = open(starting_path + 'site.csv', 'wb')
    site_writer = csv.writer(site_file, dialect='excel', encoding='utf-8')
    # 1:M related tables
    management_strategy_file = open(starting_path + 'management_strategy.csv', 'wb')
    management_strategy_writer = csv.writer(management_strategy_file, dialect='excel', encoding='utf-8')
    contaminated_medium_file = open(starting_path + 'contaminated_medium.csv', 'wb')
    contaminated_medium_writer = csv.writer(contaminated_medium_file, dialect='excel', encoding='utf-8')
    annual_data_file = open(starting_path + 'annual_data.csv', 'wb')
    annual_data_writer = csv.writer(annual_data_file, dialect='excel', encoding='utf-8')

    # column headers
    site_writer.writerow(['FederalSiteID',
                          'ReportingOrganizationCode',
                          'Created',
                          'LastModified',
                          'Name',
                          'SiteStatus',
                          'StatusDescription',
                          'ClassificationCode',
                          'ClassificationName',
                          'PropertyNumber',
                          'ReasonForFederalInvolvement',
                          'LocationSGCCode',
                          'LocationFEDCode',
                          'LocationMiniMapURL',
                          'LocationLatitude',
                          'LocationLongitude',
                          'LocationMunicipality',
                          'LocationProvince',
                          'LocationFederalElectoralDistrict',
                          'LocationCountry',
                          'ContaminationEstimateCubicMetres',
                          'ContaminationEstimateHectares',
                          'ContaminationEstimateTons',
                          'ActionPlan',
                          'AdditionalInformation',
                          'PopulationKM1',
                          'PopulationKM5',
                          'PopulationKM10',
                          'PopulationKM25',
                          'PopulationKM50'])
    management_strategy_writer.writerow(['FederalSiteID',
                                         'ManagementTypeCode',
                                         'ManagementTypeName'])
    contaminated_medium_writer.writerow(['FederalSiteID',
                                         'ContaminationCode',
                                         'ContaminationName',
                                         'ContaminatedMediumCode',
                                         'ContaminatedMediumName'])
    annual_data_writer.writerow(['FederalSiteID',
                                 'FiscalYear',
                                 'ReportingOrganizationCode',
                                 'HighestStepCompleted',
                                 'TotalAssessmentExpenditure',
                                 'TotalRemediationExpenditure',
                                 'TotalCareMaintenanceExpenditure',
                                 'TotalMonitoringExpenditure',
                                 'FCSAPAssessmentExpenditure',
                                 'FCSAPRemediationExpenditure',
                                 'FCSAPCareMaintenanceExpenditure',
                                 'FCSAPMonitoringExpenditure',
                                 'RemediationAmountCubicMetres',
                                 'RemediationAmountHectares',
                                 'RemediationAmountTons',
                                 'Closed'])
    # data rows
    for sites in root.findall('Sites'):
        for site in sites.findall('Site'):
            # handle optional elements
            name = optional_element_lookup(site, 'Name', 'EN')
            classification_code = optional_element_lookup(site, 'Classification', 'Code')
            classification_name = optional_element_lookup(site, 'Classification', 'Name', 'EN')
            property_number = optional_element_lookup(site, 'PropertyNumber')
            mini_map_url = optional_element_lookup(site, 'Location', 'MiniMapURL')
            latitude = optional_element_lookup(site, 'Location', 'Latitude')
            longitude = optional_element_lookup(site, 'Location', 'Longitude')
            municipality = optional_element_lookup(site, 'Location', 'Municipality')
            province = optional_element_lookup(site, 'Location', 'Province')
            federal_electoral_district = optional_element_lookup(site, 'Location', 'FederalElectoralDistrict', 'EN')
            contamination_estimate_cubic_metres = optional_element_lookup(site,
                                                                          'ContaminationDetails',
                                                                          'ContaminationEstimates',
                                                                          'CubicMetres')
            contamination_estimate_hectares = optional_element_lookup(site,
                                                                      'ContaminationDetails',
                                                                      'ContaminationEstimates',
                                                                      'Hectares')
            contamination_estimate_tons = optional_element_lookup(site,
                                                                  'ContaminationDetails',
                                                                  'ContaminationEstimates',
                                                                  'Tons')
            action_plan = optional_element_lookup(site, 'ActionPlan', 'EN')
            additional_information = optional_element_lookup(site, 'AdditionalInformation', 'EN')
            population_km1 = optional_element_lookup(site, 'PopulationCounts', 'KM1')
            population_km5 = optional_element_lookup(site, 'PopulationCounts', 'KM5')
            population_km10 = optional_element_lookup(site, 'PopulationCounts', 'KM10')
            population_km25 = optional_element_lookup(site, 'PopulationCounts', 'KM25')
            population_km50 = optional_element_lookup(site, 'PopulationCounts', 'KM50')
            # output row
            site_writer.writerow(['"' + site.get('FederalSiteIdentifier') + '"',
                                  site.get('ReportingOrganization'),
                                  site.get('Created'),
                                  site.get('LastModified'),
                                  name,
                                  site.find('SiteStatus').find('Status').find('EN').text,
                                  site.find('SiteStatus').find('Description').find('EN').text,
                                  classification_code,
                                  classification_name,
                                  property_number,
                                  site.find('ReasonForFederalInvolvement').find('EN').text,
                                  site.find('Location').get('sgc'),
                                  site.find('Location').get('fed'),
                                  mini_map_url,
                                  latitude,
                                  longitude,
                                  municipality,
                                  province,
                                  federal_electoral_district,
                                  site.find('Location').find('Country').find('EN').text,
                                  contamination_estimate_cubic_metres,
                                  contamination_estimate_hectares,
                                  contamination_estimate_tons,
                                  action_plan,
                                  additional_information,
                                  population_km1,
                                  population_km5,
                                  population_km10,
                                  population_km25,
                                  population_km50])
            # 1:m related tables
            management_strategy = site.find("ManagementStrategy")
            if management_strategy is not None:
                for management_type in management_strategy.findall("ManagementType"):
                    management_strategy_writer.writerow(['"' + site.get('FederalSiteIdentifier') + '"',
                                                         management_type.get('code'),
                                                         management_type.find('EN').text])
            contamination_details = site.find('ContaminationDetails')
            if contamination_details is not None:
                contaminated_media = contamination_details.findall("ContaminatedMedia")
                if contaminated_media is not None:
                    for contaminated_medium in contaminated_media:
                        contaminated_medium_writer.writerow(['"' + site.get('FederalSiteIdentifier') + '"',
                                                             contaminated_medium.find('Contamination').get('code'),
                                                             contaminated_medium.find('Contamination').find('EN').text,
                                                             contaminated_medium.find('Medium').get('code'),
                                                             contaminated_medium.find('Medium').find('EN').text])
            for annual_data in site.findall("AnnualData"):
                remediation_amount_cubic_metres = optional_element_lookup(annual_data,
                                                                          'RemediationAmounts',
                                                                          'CubicMetres')
                remediation_amount_cubic_hectares = optional_element_lookup(annual_data,
                                                                            'RemediationAmounts',
                                                                            'Hectares')
                remediation_amount_cubic_tons = optional_element_lookup(annual_data,
                                                                        'RemediationAmounts',
                                                                        'Tons')
                annual_data_writer.writerow(['"' + site.get('FederalSiteIdentifier') + '"',
                                             annual_data.get('FiscalYear'),
                                             annual_data.get('ReportingOrganization'),
                                             annual_data.find('HighestStepCompleted').text,
                                             annual_data.find('TotalAssessmentExpenditure').text,
                                             annual_data.find('TotalRemediationExpenditure').text,
                                             annual_data.find('TotalCareMaintenanceExpenditure').text,
                                             annual_data.find('TotalMonitoringExpenditure').text,
                                             annual_data.find('FCSAPAssessmentExpenditure').text,
                                             annual_data.find('FCSAPRemediationExpenditure').text,
                                             annual_data.find('FCSAPCareMaintenanceExpenditure').text,
                                             annual_data.find('FCSAPMonitoringExpenditure').text,
                                             remediation_amount_cubic_metres,
                                             remediation_amount_cubic_hectares,
                                             remediation_amount_cubic_tons,
                                             annual_data.find('Closed').text])

finally:
    if site_file is not None:
        site_file.close()
    if management_strategy_file is not None:
        management_strategy_file.close()
    if contaminated_medium_file is not None:
        contaminated_medium_file.close()
