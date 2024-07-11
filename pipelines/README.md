# Data pipelines

The dataset generation for Dutch municipalities has partly been automated using Python-based Jupyter Notebooks. So far, two pipelines has been setup:

* Creating and/or updating datasets
* Built environment stock Dutch municipalities

These two are described in more detail below.

Note that the raw input data can be found in the [Quintel dropbox](https://www.dropbox.com/scl/fo/bq1jbkw0peq85gpzzri93/h?rlkey=skm3g8alwbqc3dvdusa5cx7vi&dl=0). Make sure to copy this data to the pipelines/data/raw directory.

## Creating and/or updating datasets


The [ETM Dataset Manager](https://data.energytransitionmodel.com) includes most of the ETM datasets, including the ones for Dutch municipalities. The base year of these datasets differs. Some are 2016-based, others are 2019-based. This depends on the dataset's base year that is offered in the ETM itself.

A while ago the municipal datasets for 2019 have been created using an Excel workflow. This Excel analysis can be found in the Quintel dropbox. In addition to this Excel workflow a pipeline in Jupyter Notebook (Python-based) was setup.

Let's take the municipality of Veenendaal as an example. Say that we would like to update the dataset to the 2019 data. In order to do that we both need the results of the Excel workflow as well as the ones from the Jupyter Notebook pipeline. The municipal dataset update consists of three migration steps in ETLocal. 

Below these steps are described in more detail:

#### Excel  workflow (migration steps 1 and 2)

* Follow the steps as described in this [guide](https://www.dropbox.com/scl/fi/7tg3r3om7xvkwkqdmyyuo/update_municipality_to_2019.docx?rlkey=kt2w0dbl4mw2wnhi7bmv2zpdy&dl=0).

* The results from the Excel workflow are stored in the [`modeling_experiments`](https://github.com/quintel/modeling_experiments/tree/master/etlocal/2019_update) Github repository. Make sure that the results align with the latest modelling of the ETM. For example, if dataset attributes have been removed during a modelling project, make sure to remove these from the data.

* Run the [`generate_migration`](https://github.com/quintel/modeling_experiments/blob/master/etlocal/2019_update/generate_migration.py) script in your terminal, e.g.: 

```
python3 etlocal/2019_update/generate_migration.py veenendaal_2019_update GM0345
```

* Make sure that the data aligns with the latest ETM modelling updates. If dataset attributes (interface elements) have been renamed or removed from ETLocal, make sure to rename or remove the corresponding keys in the input data for the script as well.

* < **to do Charlotte** | please elaborate on this if needed >

* If the script has successfully run, two migrations have been created in the ETLocal repository.

#### Jupyter Notebook workflow (migration step 3)

* Check out the "[getting started](https://github.com/quintel/etdataset/wiki/Creating-and-or-updating-municipal-datasets)" Github wiki for how to install the necessary libraries.

* For now, no raw input data is necessary to run the notebook. Hence, you can leave the data/raw directory empty.

* The config data does need to be checked. Make sure to update both the `config/data.csv` with the relevant list of municipalities as well as the `config/etlocal_interface_elements.csv` in order to match the latest ETM dataset structure. If new dataset attributes (interface elements) have been added to ETLocal, make sure to update this in the config file. Same goes for the update and removal of ETLocal dataset attributes.

* Then, you're ready to run the Notebook!
  * In the Scope section the list of municipalities from `config/data.csv` is collected. Here, you can also specify the parent dataset and the dataset year.
  * Then setup some files and data such as the parent data and the (empty) etlocal template.
  * Next, you can run the notebook cells for the different sectors (general, households, services, agriculture, transport, industry and energy production). Some parts of the notebook are still work in progress and therefore empty.
  * When the data is ready (i.e., the etlocal template has been filled with all the relevant data), it can be transformed to the required files for a dataset migration in the Migration section of the notebook.

Note that most of the steps are documented in more detail in the notebook itself.


## Built environment stock Dutch municipalities

For the improved modelling of heat (live in March 2024) new housing stock data was required for Dutch municipalities. A new pipeline in Jupyter Notebook ("Pipeline housing stock Dutch municipalities") was created to process this data for the datasets.

The pipeline distinguishes the data processes for households and buildings (or services) because both are based on different data sources. Despite the processes for households and buildings are based on different sources, they do undergo the same steps:

* **Extract**: collecting the data from the data sources 
* **Transform**: preprocessing, cleaning, enriching and aggregating the data
* **Load**: exporting the data to csv files that can be used to create or update datasets in the ETM Dataset Manager (ETLocal)

Below both processes for households and buildings are described in more detail.

### Households

The ETM municipal datasets require the following information per combination of housing type and construction period:

* Number of residences
* Typical useful demand in kWh/m2
* Share of total useful heat demand

The data above is derived from the **[EP-online](https://www.ep-online.nl/PublicData)** and **[PBL referentieverbruik warmte](https://dataportaal.pbl.nl/VIVET/Referentieverbruik_warmte/)** data sources. Both provide data on residential level.

#### Extract

In this step the raw data is collected for each of the data sources:

* **PBL referentieverbruik warmte** provides data about useful demand for space heating, property, energy labels, surface, construction year and housing type for all residences.

* **EP-online** provides data about energy labels and energy prestation indicators for all registered residences. This dataset therefore doesn't cover all residences.

#### Transform

In this step the raw data is transformed to the desired format with the following sub steps:

1. cleaning and preprocessing 
2. combining the different data sources
2. enriching the data with ETM classifications
3. aggregating the data to municipal level
4. deriving the required ETM dataset attributes
5. aggregating the data to national level


##### 1. Cleaning and preprocessing

First, the raw data is filtered for the relevant columns that should be kept. The other columns are not relevant and can be dropped.

From the **EP-online** data we use:

* `Pand_gebouwklasse` (used to filter for households)
* `Pand_warmtebehoefte` (represents the typical heat demand in kWh/m2)
* `Pand_energieklasse` (used to derive the typical heat demand from)
* `Pand_bagverblijfsobjectid` (used to merge this data with other data)

From the **PBL referentieverbruik warmte** data we use:

* `Woningkenmerken/eigendom` (used for information about property)
* `Woningkenmerken/oppervlakte` (used for calculations concerning the typical heat demand and the share of useful space heating demand)
* `Woningkenmerken/schillabel` (used to derive the typical heat demand from)
* `Woningkenmerken/bouwjaar` (used to classify the residences to a construction period)
* `Woningkenmerken/woningtype` (used to classify the residences to a housing type)
* `Functionele vraag/ruimteverwarming` (used to determine the shares of total useful heat demand)

Also, since the base year is 2019, the data is filtered for housings that were built in 2019 or before (either by dropping houses without a BAG VBO (verblijfsobject) ID or dropping houses that were built after 2019). 

Further, during the analysis a strange outlier with an insanely high heat demand was identified. This outlier is dropped as well.

Lastly, the formatting of the BAG VBO IDs was matched between the two data sources (in order to be able to match the two in the next sub step).

##### 2. Combining the EP-online and PBL data

Based on the BAG VBO ID the two datasets are merged into one. Note that the EP-online data didn't cover all residences. Hence, in the merged dataset part of the residences doesn't have data for the EP-online columns/attributes.

In this step the data is also corrected for relevant municipal reorganizations. For instance, Appingedam, Delfzijl and Loppersum have been merged into Eemsdelta. Therefore we replace the municipal codes of the first three by the municipal code of Eemsdelta in the data.

##### 3. Enriching the data with ETM classifications

To match the ETM dataset structure the residences are classified to the different housing types (apartments, terraced houses, semi-detached houses and detached houses) and construction periods (<1945, 1945-1964, 1965-1984, 1985-2004, >2005). Note that corner houses are classified to semi-detached houses. 

Also, if no typical heat demand in kWh/m2 (EP-online's `Pand_warmtebehoefte`) is available, the energy label is used to estimate the typical heat demand for a residence. We use the following mapping:

* Label A (and higher): 118 kWh/m2
* Label B: 175 kWh/m2
* Label C: 220 kWh/m2
* Label D: 270 kWh/m2
* Label E: 313 kWh/m2
* Label F: 358 kWh/m2
* Label G: 403 kWh/m2

< **to do Charlotte**: describe source or methodology behind mapping >

##### 4. Aggregating the data to municipal level

For each municipality we then group the data into the combinations of housing types and construction periods as specified by the ETM. If relevant, the data can also be grouped by owner ('koop' / 'particuliere huur' / 'sociale huur'). 

##### 5. Deriving the required ETM dataset attributes

Now we can derive the required ETM dataset attributes:

* Number of residences
* Typical useful demand in kWh/m2
* Share of total useful heat demand

The **number of residences** can be derived by applying a count on the data which is grouped by combination of housing types and construction periods.

The **typical useful demand** can either be derived from EP-online's `Pand_warmtebehoefte` or the mapping based on energy labels.

The **share of total useful heat demand** is calculated based on PBL's `Functionele vraag/ruimteverwarming` data. 

##### 6. Aggregating the data to national level

For the national dataset of the Netherlands, the same sub steps (1 through 5) should be taken. As opposed to the steps for municipalities, the data can now be grouped on national instead of municipal level.

#### Load

After completing the transformation steps, the data is ready to be exported to csv files.

### Buildings

The ETM municipal datasets require the following information for buildings:

* Number of buildings
* Typical useful demand in kWh/m2

The data above is derived from the **[Verrijkte BAG utiliteitsbouw](https://energy.nl/publications/verrijkte-bag-energetische-vraagstukken/)** by TNO. This data source provides data about a.o. energy labels, energy use and surface on a building level.

#### Extract

In this step the raw data is collected and stored in a dataframe.

#### Transform

In this step the raw data is transformed to the desired format with the following sub steps:

1. cleaning and preprocessing 
2. enriching the data with ETM classifications
3. aggregating the data to municipal level
4. deriving the required ETM dataset attributes
5. aggregating the data to national level


##### 1. Cleaning and preprocessing

First, the raw data is filtered for the relevant columns that should be kept. The other columns are not relevant and can be dropped.

From the **verrijkte BAG utiliteitsbouw** data we use:

* `pand_label_keus` (used to derive the typical heat demand from)
* `bouwjaar` (used to filter for buildings built in 2019 or before)
* `vbo_opp_m2` (used to calculate the useful heat demand)
* `gemeentenaam` (used to group the data by municipality)
* `gemeente_id` (used to group the data by municipality ID)
* `vboid`

Also, since the base year is 2019, the data is filtered for buildings that were built in 2019 or before.

Further, buildings with use functions "woon" and "industrie" are dropped since these do not classify as buildings according to the ETM definitions.
                                                
##### 3. Enriching the data with ETM classifications

For buildings there is no direct typical heat demand in kWh/m2 available. Hence, the energy label (`pand_label_keus`) is used to estimate the typical heat demand for a building. We use the same  mapping as we use for households:

* Label A (and higher): 118 kWh/m2
* Label B: 175 kWh/m2
* Label C: 220 kWh/m2
* Label D: 270 kWh/m2
* Label E: 313 kWh/m2
* Label F: 358 kWh/m2
* Label G: 403 kWh/m2

Also, we use the typical heat demand estimations to calculate the useful heat demand per building (by multiplying it with the building's surface).

##### 4. Aggregating the data to municipal level

We then group the data by municipality. 

##### 5. Deriving the required ETM dataset attributes

Now we can derive the required ETM dataset attributes:

* Number of buildings
* Typical useful demand in kWh/m2

The **number of buildings** can be derived by applying a count on the data.

The **typical useful demand** can be calculated by dividing the total useful heat demand by the total surface per municipality. 

##### 6. Aggregating the data to national level

For the national dataset of the Netherlands, the data can now be grouped on national instead of municipal level.

#### Load

After completing the transformation steps, the data is ready to be exported to csv files.

### Setup dataset migrations

When the housing stock data is ready for households and buildings, it can be transformed to the required files for a dataset migration.