import pandas as pd
import numpy as np

def process_new_emissions_data(excel_file_path):
    """
    Process the NEW emissions data file (new_1990_emissions_data.xlsx)
    Applies the same Excel analysis logic to the new data format
    """
    
    # Load the new data format
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)
    
    # Get the emissions data (main data sheet)
    emissions_data = excel_data['Emissies']  # This is the main data sheet in new format
    
    print(f"Loaded {len(emissions_data)} emission records")
    print(f"Data covers: {emissions_data['Gebied'].nunique()} unique areas")
    print(f"Sectors found: {emissions_data['Sector'].unique()}")
    
    # Step 1: Create lookup table equivalent to code_1990
    print("\nStep 1: Creating lookup table from new data...")
    print(f"Available columns: {list(emissions_data.columns)}")
    
    # Group by area and sector to get emissions per area-sector combination
    lookup_table = emissions_data.groupby(['Code_gebied', 'Sector']).agg({
        'Gebied': 'first',
        'Emissie': 'sum'  # Sum emissions for each area-sector combo (this is the actual emissions column)
    }).reset_index()
    
    # Create the composite key like Excel does
    lookup_table['CODE_GEBIEDDOELGROEP'] = (
        lookup_table['Code_gebied'].astype(str) + 
        lookup_table['Sector'].astype(str)
    )
    
    print(f"Created lookup table with {len(lookup_table)} area-sector combinations")
    
    # Step 2: Get unique municipalities/areas
    print("\nStep 2: Setting up municipality base...")
    municipalities = emissions_data[['Code_gebied', 'Gebied']].drop_duplicates()
    municipalities = municipalities.rename(columns={
        'Code_gebied': 'KM_code_number',
        'Gebied': 'Gemeentenaam'
    })
    
    print(f"Found {len(municipalities)} unique municipalities")
    
    # Step 3: Filter sectors to match original Excel analysis
    available_sectors = emissions_data['Sector'].unique()
    print(f"\nAvailable sectors in new data: {list(available_sectors)}")
    
    # Define the sectors that were actually used in the original Excel analysis
    excel_sectors_used = [
        'Consumenten',
        'Handel, Diensten en Overheid (HDO)',
        'Verkeer en vervoer', 
        'Overige industrie',
        'Chemische Industrie',
        'Afvalverwijdering',
        'Bouw',
        'Raffinaderijen',
        'Landbouw',
        'Riolering en waterzuiveringsinstallaties'
    ]
    
    # Only use sectors that were in the original Excel AND exist in new data
    sectors_to_use = [sector for sector in excel_sectors_used if sector in available_sectors]
    excluded_sectors = [sector for sector in available_sectors if sector not in excel_sectors_used]
    
    print(f"✅ Using {len(sectors_to_use)} sectors (matching original Excel):")
    for sector in sectors_to_use:
        print(f"  - {sector}")
    
    print(f"❌ Excluding {len(excluded_sectors)} sectors (not used in Excel):")
    for sector in excluded_sectors:
        print(f"  - {sector}")
    
    if len(excluded_sectors) == 0:
        print("  (None - all sectors match)")
    
    # Step 4: Perform INDEX/MATCH lookups for each sector
    print(f"\nStep 3: Performing lookups for {len(sectors_to_use)} sectors (matching Excel analysis)...")
    
    # Create lookup dictionary for speed
    lookup_dict = {}
    for _, row in lookup_table.iterrows():
        key = str(row['CODE_GEBIEDDOELGROEP'])
        lookup_dict[key] = row['Emissie']  # Use 'Emissie' column instead of '1990'
    
    # Create the main analysis dataframe
    co2_analysis = municipalities.copy()
    
    # For each sector, look up emissions
    for sector in sectors_to_use:
        co2_analysis[sector] = co2_analysis['KM_code_number'].apply(
            lambda km_code: lookup_dict.get(str(km_code) + str(sector), 0)
        )
    
    # Step 5: Calculate totals (Excel column M: SUM across sectors)
    print("\nStep 4: Calculating aggregations...")
    co2_analysis['co2_1990_kg'] = co2_analysis[sectors_to_use].sum(axis=1)
    
    # Step 6: Calculate scaling (Excel column N: proportion of total)
    total_kg = co2_analysis['co2_1990_kg'].sum()
    co2_analysis['co2_1990_scaled'] = co2_analysis['co2_1990_kg'] / total_kg
    
    # Step 7: Convert to megatons (Excel column O)
    scaling_factor = 158.7190073  # Updated scaling factor
    co2_analysis['co2_1990_mt'] = co2_analysis['co2_1990_scaled'] * scaling_factor
    
    # Step 8: Create final output matching Excel output format
    print("\nStep 5: Creating final output...")
    output = co2_analysis[['Gemeentenaam', 'KM_code_number', 'co2_1990_mt']].copy()
    output.columns = ['Gemeentenaam', 'KM_code', 'co2_1990_mt']
    
    # Sort by municipality name (like Excel)
    output = output.sort_values('Gemeentenaam').reset_index(drop=True)
    
    print(f"\nProcessing complete!")
    print(f"- {len(output)} municipalities processed")
    print(f"- Total emissions: {output['co2_1990_mt'].sum():.2f} MT")
    print(f"- Average per municipality: {output['co2_1990_mt'].mean():.4f} MT")
    print(f"- Top emitter: {output.loc[output['co2_1990_mt'].idxmax(), 'Gemeentenaam']} ({output['co2_1990_mt'].max():.2f} MT)")
    
    return output, co2_analysis  # Return both final output and detailed analysis

def run_analysis_on_new_data(excel_file='new_1990_emissions_data.xlsx'):
    """
    Simple function to run the analysis on new emissions data
    """
    try:
        results, detailed = process_new_emissions_data(excel_file)
        return results, detailed
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# Example usage:
if __name__ == "__main__":
    print("Processing new emissions data file...")
    print("=" * 50)
    
    # Process the new data file
    results, detailed_analysis = run_analysis_on_new_data('new_1990_emissions_data.xlsx')
    
    if results is not None:
        print("\n" + "="*50)
        print("RESULTS PREVIEW:")
        print("="*50)
        print(results.head(10).to_string(index=False))
        
        print(f"\n" + "="*50)
        print("TOP 5 EMITTERS:")
        print("="*50)
        top_5 = results.nlargest(5, 'co2_1990_mt')
        print(top_5.to_string(index=False))
        
        # Save results
        results.to_csv('co2_emissions_new_data.csv', index=False)
        print(f"\n✅ Results saved to: co2_emissions_new_data.csv")
        
        # Also save detailed analysis with all sectors
        if detailed_analysis is not None:
            detailed_analysis.to_csv('co2_emissions_detailed.csv', index=False)
            print(f"✅ Detailed analysis saved to: co2_emissions_detailed.csv")
            
        print(f"\n" + "="*50)
        print("SUMMARY STATISTICS:")
        print("="*50)
        print(f"Total municipalities: {len(results)}")
        print(f"Total emissions: {results['co2_1990_mt'].sum():.2f} MT")
        print(f"Average emissions: {results['co2_1990_mt'].mean():.4f} MT")
        print(f"Median emissions: {results['co2_1990_mt'].median():.4f} MT")
        print(f"Zero emissions: {(results['co2_1990_mt'] == 0).sum()} municipalities")
        print(f"Max emissions: {results['co2_1990_mt'].max():.2f} MT")
    else:
        print("❌ Processing failed!")