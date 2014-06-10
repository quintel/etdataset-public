# Data format for IEA data

The Research Analyses require the original IEA data to be in a very specific format. This document describes the steps you need to take to obtain the IEA data in this format.

## Extended Energy Balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of Non-OECD Countries (2014 preliminary edition)  / Extended Energy Balances

Re-arrange the COLUMNS and ROWS (by dragging and dropping) such that they look like this:

**COLUMNS:**

PRODUCT


**ROWS:**

UNIT

COUNTRY

TIME

FLOW

Then select ALL products, UNIT = TJ and ALL flows and the country and year you want to make a model for. Then click 'View as Table' and save the Energy Balance in `.xls` format.

## Autoproducer Table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2014 preliminary edition) / OECD, Net Electricity and Heat Production by Autoproducers

Re-arrange the COLUMNS and ROWS (by dragging and dropping) such that they look like this:

**COLUMNS:**

FLOW


**ROWS:**

COUNTRY

TIME

PRODUCT

PLANT

Then select ALL flows, ALL products and ALL plants and the country and year you want to make a model for. Then click 'View as Table' and save the Autoproducer Table in `.xls` format.




