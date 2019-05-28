### Building demand appliances - script
The data needs to be processed in order to match the ETM format. The input data (EDSN profiles, see ⁨etdataset⁩ ▸ ⁨curves⁩ ▸ ⁨demand⁩ ▸ ⁨buildings⁩ ▸ ⁨appliances⁩ ▸ ⁨data⁩ ▸ ⁨nl⁩ ▸ ⁨source⁩) are per 15 min ETM uses profiles per hour, that are normalized (sum of the profile should be 1/3600). This transformation is done in `buildings_appliances_edsn.py`



