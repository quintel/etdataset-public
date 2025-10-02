"""TODO"""

# imports
# ...

class Checker():
    """
    A class for basic checks such as whether there are nan values,
    whether all values are numeric, etc.
    """
    
    def __init__(self):
        return
        
    
    def has_non_numeric_values(self, df):
        """
        df             DataFrame
        """
        non_float_columns = df.select_dtypes(exclude='float').columns

        has_non_numeric_values = True if len(non_float_columns) > 0 else False
        
        return has_non_numeric_values
        
        
    def get_non_numeric_columns(self, df):
        """
        df             DataFrame
        """
        return df.select_dtypes(exclude='float').columns
    
    
    def get_non_float_values(self, df, col):
        """
        df             DataFrame
        col            str, column name
        """
        return df.loc[~df[col].apply(lambda x: isinstance(x, float))][col]
        
        
    def has_missing_values(self, values):
        """
        values         float, source value to be converted
        """
        has_missing_values = False
        
        return has_missing_values
        
        """TODO"""
           
        
    def has_negative_values(self, values):
        """
        values         float, source value to be converted
        """
        has_negative_values = True
        
        # Check for negative values and print key-value combinations
        # negative_values = df.lt(0)
        # if negative_values.any().any():
        #     for column in negative_values:
        #         for index, value in negative_values[negative_values[column]].iteritems():
        #             print("Column:", column, "Index:", index, "Value:", df[column][index])
        
        return has_negative_values
        
        """TODO"""
               
        
    def data_types_of(self, df):
        """
        Checks the data type per column of the dataframe
        
        df             DataFrame with values
        """
        
        return df.dtypes