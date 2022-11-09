import pandas as pd
from etm_tools.utils import EurostatAPI
from etm_tools.energy_balance_operations.input_files import EBConfig

class CHPCapacities:
    '''
    Wrapper around Eurostat CHP capacity download. Does some simplification and
    summing on the original download (see simplify method).
    '''

    # These will be merged into 'Steam Turbine CHP'
    STEAM_TURBINES = [
        'Steam - backpressure turbine',
        'Steam - condensing turbine (eff ≥ 80%)'
    ]


    def __init__(self, eb, year, area):
        self.eb = CHPCapacities.simplify(eb)
        self.year = year
        self.area = area


    def columns(self, level=0):
        return self.eb.columns.get_level_values(level).unique()


    def capacity(self, gen_tech, carrier='electricity'):
        '''Returns float capacity.'''
        return self.__lookup(gen_tech, carrier)


    def sum(self, techs, carrier='electricity'):
        return sum(self.__lookup(tech, carrier) for tech in techs)


    def __lookup(self, gen_tech, carrier):
        if carrier == 'electricity':
            return self.__loc('Maximum gross electricity capacity', gen_tech)
        elif carrier =='heat':
            return self.__loc('Maximum net thermal capacity', gen_tech)

        return 0


    def __loc(self, row, gen_tech):
        try:
            return self.eb.loc[row, gen_tech]
        except KeyError:
            return 0


    @classmethod
    def from_eurostat(cls, country, year, eb_type='energy_balance', use_cols={}):
        trnsl = EBConfig.load(eb_type=eb_type)

        frame = CHPCapacities.read_frame(country, eb_type, year, use_cols)

        # Remove unwanted countries
        frame = frame[frame['geo']==country]

        # Pivot into table view with multicolumns
        frame = frame.pivot_table(
            values='OBS_VALUE',
            index=['nrg_bal'],
            columns=['gen_tech', 'plants', 'lev_efcy']).fillna(0.0)

        frame.rename(
            index=trnsl.flow_translation(),
            columns= trnsl.product_translation(),
            inplace=True)


        return cls(frame, year, country)


    @staticmethod
    def read_frame(country, eb_type, year, use_cols):
        '''Connect to Eurostat to retrieve initial table. Returns a Dataframe'''
        try:
            return pd.read_csv(
                EurostatAPI().get_csv(country, csv_type=eb_type, year=year),
                index_col=['nrg_bal', 'gen_tech'],
                usecols=['nrg_bal', 'gen_tech', 'OBS_VALUE', 'geo', 'TIME_PERIOD'] +
                    list(use_cols.keys())
            )
        except pd.errors.EmptyDataError as exc:
            raise SystemExit('Data could not be retrieved from Eurostat.' +
                ' Please check if your country and year are available') from exc


    @staticmethod
    def simplify(frame):
        # Only keep ALL for lev_efcy
        frame = frame.drop(['HIGH', 'LOW'], axis=1, level=2).droplevel('lev_efcy', axis=1)

        # Remove the Total column
        frame = frame.drop('Total', axis=1, level='gen_tech')

        # Sum CHPU_LE and CHPU_HE
        frame = frame.groupby(level='gen_tech', axis=1).sum()

        # Merge Steam Turbines
        CHPCapacities.merge_steam_turbines(frame, CHPCapacities.STEAM_TURBINES)
        if not 'Steam Turbine CHP' in frame.columns:
            frame['Steam Turbine CHP'] = 0
            print('\033[93mWarning: No Steam Turbines found in Eurostat CHP download \033[0m')

        return frame


    @staticmethod
    def merge_steam_turbines(frame, turbines):
        try:
            frame['Steam Turbine CHP'] = frame[turbines].sum(axis=1)
            frame.drop(turbines, axis=1, inplace=True)
        except KeyError:
            if isinstance(turbines, list):
                for turbine in turbines:
                    CHPCapacities.merge_steam_turbines(frame, turbine)
        except ValueError:
            frame.rename({turbines: 'Steam Turbine CHP'}, axis=1, inplace=True)
