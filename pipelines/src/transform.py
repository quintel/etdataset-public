"""TODO"""

# imports
import pandas as pd
from dataclasses import dataclass
import pint

# Dataclass to represent a unit conversion rule
@dataclass
class ConversionRule:
    source_unit: str
    target_unit: str
    factor: float
    reversible: bool = True
    description: str = ""

# TransformerV2 class combining manual rules and Pint as a fallback
class TransformerV2:
    def __init__(self):
        # dictionary to store manual conversion rules
        self.rules = {}
        # Pint's unit registry
        self.ureg = pint.UnitRegistry()
        # Initialize manually defined rules
        self.intermediates = [] # List to store intermediate units
        self._init_rules()

    def _init_rules(self):
        """
        Private method to initialize manual conversion rules.
        Add key domain-specific conversion rules that require documentation or careful assumptions.
        Pint will be used for all other general-purpose unit conversions.

        To add a new manual conversion rule that is always available:
        1. Call the add_rule method with the source unit, target unit, conversion factor and description.
        2. Add the unit with the SI-prefix to the intermediates attribute. This way, derived units can also be converted.
        For example, adding "MJ" to the intermediates list allows for conversion of m3 (natural gas) to TJ as well.
        Do this if you expect to encounter derived units in the data.
        """
        self.add_rule(
            "m3 (natural gas)", "MJ", 31.65,
            description="LHV of natural gas, NL standard. Source: Gasunie"
        )
        self.intermediates.append("MJ") # 

        self.add_rule(
            "miljoen m3", "TJ", self.rules[("m3 (natural gas)", "MJ")].factor,
            description="LHV of natural gas, NL standard. Source: Gasunie"
        )
        self.intermediates.append("TJ") # Add TJ to intermediates for derived units

        self.add_rule(
            "tonne/m3", "tonne/TJ (natural gas)", self.rules[("MJ", "m3 (natural gas)")].factor * 1e6,
            description="Equal to [MJ to m3 (natural gas)] * 1e6. Based on LHV of natural gas, NL standard. Source: Gasunie"
        )

        self.add_rule(
            "tonne/kWh", "tonne/TJ (electricity)", 
            # Example: 1 tonne/kWh = 1 tonne/(3.6e-6 TJ/kWh) = 1 * 1/(3.6e-6 TJ/kWh) = 1 * [kWh to TJ]
            self.ureg.Quantity(1, "TJ").to("kWh").magnitude,
            description="Equal to 1 / [kWh to TJ] or [TJ to kWh]."
        )
        

    def add_rule(self, source_unit, target_unit, factor, reversible=True, description=""):
        """
        Manually add a conversion rule to the internal registry.
        """
        self.rules[(source_unit, target_unit)] = ConversionRule(source_unit, target_unit, factor, reversible, description)
        if reversible and factor != 0:
            self.rules[(target_unit, source_unit)] = ConversionRule(target_unit, source_unit, 1/factor, False, f"Inverted from {source_unit} → {target_unit}")
            self.rules[(target_unit, source_unit)] = ConversionRule(target_unit, source_unit, 1/factor, False, f"Inverted from {source_unit} → {target_unit}")

    def convert(self, value, source_unit, target_unit, return_factor=False):
        """
        Convert a value from source_unit to target_unit.
        Tries the following in order:
        
        1. Direct manual conversion via self.rules
        2. Direct Pint conversion if both units are recognized
        3. Fallback via an intermediate unit (e.g. MJ), using manual + Pint
        
        If return_factor is True, returns a tuple (converted_value, conversion_factor).
        """
        key = (source_unit, target_unit)
        
        # Step 1: Direct manual rule
        if key in self.rules:
            rule = self.rules[key]
            converted = value * rule.factor
            if return_factor:
                return converted, rule.factor
            return converted

        # Step 2: Direct Pint conversion
        try:
            # Perform the conversion using Pint
            q = value * self.ureg(source_unit)
            converted_value = q.to(target_unit).magnitude
            # Compute conversion factor by converting 1 unit
            factor = (1 * self.ureg(source_unit)).to(target_unit).magnitude
            if return_factor:
                return converted_value, factor
            return converted_value
        except Exception:
            pass  # try fallback

        # Step 3: Indirect fallback via known intermediate units
        for mid_unit in self.intermediates:
            step1 = (source_unit, mid_unit)
            if step1 in self.rules:
                # Manual conversion from source_unit to mid_unit
                mid_value = value * self.rules[step1].factor
                try:
                    # Use Pint to convert from intermediate unit to target_unit
                    final_value = (mid_value * self.ureg(mid_unit)).to(target_unit).magnitude
                    # Compute overall conversion factor:
                    # factor_manual: conversion factor from source_unit to mid_unit
                    factor_manual = self.rules[step1].factor
                    # factor_pint: conversion factor from 1 mid_unit to target_unit using Pint
                    factor_pint = (1 * self.ureg(mid_unit)).to(target_unit).magnitude
                    overall_factor = factor_manual * factor_pint
                    if return_factor:
                        return final_value, overall_factor
                    return final_value
                except Exception:
                    continue

        # No route found
        raise ValueError(
            f"Conversion {source_unit} → {target_unit} failed: "
            "no direct rule, no Pint conversion, and no valid intermediate found."
        )


    def list_rules(self):
        """
        Return a DataFrame listing all manually defined reversible conversion rules.
        """
        return pd.DataFrame([
            {
                "source": rule.source_unit,
                "target": rule.target_unit,
                "factor": rule.factor,
                "description": rule.description
            }
            for rule in self.rules.values()
            if rule.reversible
        ])

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
        