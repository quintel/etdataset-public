# Merit order load profiles

Hourly load profiles are used in the merit order module to determine the availability of volatile electricity sources and the run profiles of must-run technologies. The sources of these load profiles as well as the load profiles themselves are stored in ETDataset. For now, these load profiles are copied to the merit repositories. In addition, the total demand hourly load profile is copied to ETSource, where it is used in the Loss of Load Expectation calculation.


## Solar pv load profiles

The hourly solar pv load profile is based on [SoDa data](http://www.soda-is.com/eng/index.html). We exported the hourly solar data for the center of the Netherlands (52°30' N, 5°45' E, according to the [CIA World Fact Book](https://www.cia.gov/library/publications/the-world-factbook/fields/2011.html)) for 2004 and 2005. If available, we use the 2005 value for a specific hour in the year. If this is not available, we use the 2004 value for this hour. As with all load profiles, we normalize the load profiles to 1/3600. The solar pv profiles is exported to `/etdataset/data/nl/2012/12_merit/output/`.

