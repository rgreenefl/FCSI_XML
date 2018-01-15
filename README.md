# FCSI_XML
Environment Canada Federal Contaminated Sites Inventory (FCS) Python XML parser/exporter
Tested with Python 2.7.10
Created by Randal Greene (rgreene@feaverslane.com), January 2018

Input: XML dump of contaminated sites, described at https://www.tbs-sct.gc.ca/fcsi-rscf/home-accueil-eng.aspx and
       downloaded from https://www.tbs-sct.gc.ca/fcsi-rscf/opendata-eng.aspx
Output: CSV tables that can be imported into a relational database system or GIS software
Note: Exports UTF-8 encoding; non-ASCII characters will display incorrectly in Excel, which assumes UTF-16
      Force Site ID to be quoted (string) because initial row appears numeric, but it is alphanumeric in some rows
      To output French text, search and replace 'EN' with 'FR'; you may also want to translate field names
      Some sites have no lat/lon, even though LocationMiniMapURL shows a point for them!
      Consider enhancement to extract the following repeating values into lookup tables:
          Classification
          ReasonForFederalInvolvement
          ManagementType
          Contamination
          Medium

License: CC-BY-SA (see https://creativecommons.org/licenses/by-sa/4.0/legalcode)
