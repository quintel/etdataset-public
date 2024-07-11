"""TODO"""

# imports
import pandas as pd


class Transformer():
    """
    A class for basic transformations such as unit conversions,
    sums, share calculations, etc.
    """
    
    def __init__(self, municipalities, year):
        self.municipalities = municipalities
        self.year = year
        
        # Some example constant, to be extended!
        self.constants = {
            "m3_to_mj": 35.17, # this is the HHV (if the LHV is needed, change the value to 31.65)
            "tj_to_gwh": 3.6,
            "gj_to_tj": 0.001
        }
        
    
    def convert(self, source_value, source_unit, target_unit):
        """
        source_value   float, source value to be converted
        source_unit    str, string in lower case representing source unit (e.g. "m3")
        target_unit    str, string in lower case representing target unit (e.g. "tj")
        """
        # Get the constant
        const = self.constants[f"{source_unit}_to_{target_unit}"]
        
        # Calculate and return the target value
        return source_value * const

    
    def filter_km_data(self, keys, source_data, meta_data):
        """
        Filters Klimaatmonitor data on relevant keys
        
        keys           list, representing Klimaatmonitor keys
        source_data    DataFrame, representing Klimaatmonitor source data
        meta_data      DataFrame, representing Klimaatmonitor meta data
        """      
        # Create empty dataframe
        df = pd.DataFrame()
        
        # Create empty list to store the data that should eventually
        # be appended to the dataframe
        data_to_append = []
        
        for municipality in self.municipalities:
            for key in keys:
                # Transform Klimaatmonitor source data to the right format
                data = {
                    "code": municipality,
                    "key": key,
                    "value": float(source_data.loc[municipality, f"{key}_{self.year}"]),
                    "unit": meta_data.loc[key,"Eenheid"],
                    "topic": meta_data.loc[key,"Onderwerp"]
                }
                
                # Add data value to the list
                data_to_append.append(data)

        # Fill dataframe with transformed Klimaatmonitor data and return it
        return pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)
    
    
    def load_km_data(self, km_data, mapping, template, keys):
        """
        Loads Klimaatmonitor data in ETLocal template
        
        # TODO add comparison of source and target units
        # TODO add KM link to commit message
        # TODO see if this piece of code can be trimmed down
        
        km_data        DataFrame, representing the filtered Klimaatmonitor source data
        mapping        DataFrame, representing the mapping from Klimaatmonitor to ETLocal keys
        template       DataFrame, representing the ETLocal template that should be filled
        keys           list, representing relevant ETLocal keys in template
        """
        # Create empty dataframe
        # df = pd.DataFrame()

        for municipality in self.municipalities:
            # template["geo_id"] = municipality

            for interface_element in keys:
                if mapping['interface_elements'].isin([interface_element]).any():
                    # Look up Klimaatmonitor keys for the interface element
                    km_keys = mapping.loc[mapping["interface_elements"] == interface_element, "klimaatmonitor_keys"].values[0]

                    # Create list from keys
                    km_keys = km_keys.split(',')

                    # Initialise value and commit
                    value = 0
                    commit = "Klimaatmonitor."
            
                    # Update value and commit
                    for km_key in km_keys:
                        filtered_data = km_data[(km_data["key"] == km_key) & (km_data["code"] == municipality)]
                        value += filtered_data["value"].values[0]
                        topic = filtered_data["topic"].values[0]
                        commit += " Topic: " + topic + ", key: " + km_key + "."

                    template.loc[(municipality, slice(None), slice(None), interface_element), 'value'] = value
                    template.loc[(municipality, slice(None), slice(None), interface_element), 'commit'] = commit

            # Add municipal data to dataframe
            # df = pd.concat([df, template], ignore_index=True)
        
        # Return the dataframe after the KM data has been filled for all municipalities
        return template
        # return df
        