## Households cooling - script

For households cooling the electricity demand profile [NEDU](https://www.nedu.nl/documenten/verbruiksprofielen/). From this website an Excel-file can be downloaded in which curves are given for different categories (for an explanation on the different categories see "profielen 2015 ELEKTRICITEIT readme.docx" in the source-folder). We are only using the first category (E1a), which is: <= 3x 25 Ampère, enkel telwerk.

The data needs to be processed in order to match the ETM format. The EDSN profiles are per 15 min and we want profiles per hour, that are normalized (sum of the profile should be 1/3600). This transformation is done in households_cooling.py