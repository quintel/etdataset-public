# Nomenclature

This document describes the nomenclature used in on ETdataset (and in the company in general). Please conform to these standards, so that we maintain consistency. 


## ETdataset

This terminology is frequently used in our data creation process.

- **Analysis**: See **Research Data Analysis**.
- **Assumptions**: Used specifically to denote the standardized assumptions users of Research Data Analyses 
need to make in order to analyse / interpret / manipulate Research Data
- **Input Data**: The final product of the research dataflow. The data that 
do not change anymore before being used to generate and initialize the ETM / graph.
- **Research Data**: Data that is uniform regardless of the country or region it belongs to. It is used to generate Input Data for the ETM / graph. Note that this means the structure 
is always the same, but the contents can differ between countries. e.g. attributes for specific groups of 'converter nodes' are both uniform and invariant between countries. IEA energy balance data are uniform but obviously different for each country.
- **Research Data Analysis**: also know as Analysis. This is a standardized analysis to manipulate or interpret uniform Research Data. Each analysis is the same irrespective of the country whose Research Data It is applied to. Input for these analyses are Research Data and Assumptions (from Sources).
- **Research Dataset**: The complete set of Research Data that Quintel maintains. Typically used for a
specific region or country, e.g. the Research Dataset for NL.
- **Source**: Any country-specific document used to fill in / quantify / research Assumptions in the Research Data Analyses. Note that if such a document had been uniform instead of country specific, it would be Research Data. Requirements for Source material are less strict than for Research Data.
- **Source analysis**: An analysis of country-specific source data, used to fill in / quantify / research Assumptions in the Research Data Analyses. Note that if such an analysis can be uniform instead of country specific, it should be Research Data Analysis. Requirements for Source Analyses are less strict than for Research Data Analyses.


## ETM nomenclature

- **Application split**: Energy use for different applications (e.g. space heating versus lighting).
- **Technology split**: Energy use by different technologies for a given aplication (e.g. gas-fired heater and heat pump for space heating).
