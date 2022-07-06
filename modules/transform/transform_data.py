import pandas as pd

class RawData:
    def __init__(self, raw_data_file_path):
        self.raw_data_file_path = raw_data_file_path
        self.df_raw_data = pd.DataFrame()
        self.df_raw_tray = pd.DataFrame()
        self.df_raw_hanger = pd.DataFrame()
        self.df_raw_bracket = pd.DataFrame()

        self.return_error = ''

        # column headers
        self.tray_columns = ['HANDLE', 'BLOCKNAME', 'BLOCK', 'NO', 'AT_SITE', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE']
        self.bracket_columns = ['BLOCKNAME', 'SUPPORT_CODE', 'SUPPORT_NO', 'BLOCK', 'NO']
        self.hanger_columns = ['HANDLE', 'BLOCKNAME', 'BLOCK', 'NO', 'HANGER_SIZE', 'HANGER_HEIGHT', 'AT_SITE', 'HANGER_TYPE_LABEL', 'HANGER_LENGTH']

        # ['BLOCKNAMES']
        self.hanger_blocknames = ['ELECT_HANGER_SX-TYPE', 'ELECT_HANGER_H-TYPE', 'ELECT_HANGER_S-TYPE', 'ELECT_HANGER_HV-TYPE']
        self.bracket_blocknames = ['ELECT_BRACKET']
        self.tray_blocknames = ['ELECT_CWAY_TRAYBLOCK_A', 'ELECT_CWAY_TRAY_BLOCK_TRO']

        self._read_data()
        # self._get_raw_tray()
        self._get_raw_hanger()


    def _read_data(self):
        print(self.raw_data_file_path)
        try:
            self.df_raw_data = pd.read_csv(self.raw_data_file_path, sep='\t')
            return self.df_raw_data
        except:
            self.return_error = 'INVALID INPUT CONTENTS'

    def _check_raw_data_headers(self, df_raw, preset_headers):
        df_raw_headers = list(df_raw.columns)
        
        # use Sets to get the difference between two lists
        template_set = set(preset_headers)
        existing_set = set(df_raw_headers)

        diff_set = list(template_set.difference(existing_set)) # the difference is/are lacking colums
        print('diff_set', diff_set)

        if len(diff_set) > 0:
            for item in diff_set:
                df_raw[item] = '' # create new column

        return df_raw

    def _separate_tray_bracket_hanger(self):
        pass
    
    def _get_raw_tray(self):
        df_raw_tray = (self.df_raw_data).copy()
        print(self.df_raw_data)

        # filter only trays
        df_raw_tray = df_raw_tray[df_raw_tray['BLOCKNAME'].isin(self.tray_blocknames)]
        df_raw_tray = df_raw_tray.sort_values(by=['BLOCK', 'NO'], ascending=True)
        
        # add missing columns
        df_raw_tray = self._check_raw_data_headers(df_raw_tray, self.tray_columns)
        
        # create new column "BLOCK-NO"
        df_raw_tray['BLOCK-NO'] = df_raw_tray['BLOCK'] + "-" + df_raw_tray['NO']

        # re-arrange column headers
        df_raw_tray = df_raw_tray[['HANDLE', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE', 'AT_SITE']]


        self.df_raw_tray = df_raw_tray
        print(self.df_raw_tray)

    def _get_raw_hanger(self):
        df_raw_hanger = (self.df_raw_data).copy()
        print(self.df_raw_hanger)

        # filter only hangers
        df_raw_hanger = df_raw_hanger[df_raw_hanger['BLOCKNAME'].isin(self.hanger_columns)]
        df_raw_hanger = df_raw_hanger.sort_values(by=['BLOCK', 'NO'], ascending=True)
        
        # add missing columns
        df_raw_hanger = self._check_raw_data_headers(df_raw_hanger, self.hanger_columns)

        # create new column "BLOCK-NO"
        df_raw_hanger['BLOCK-NO'] = df_raw_hanger['BLOCK'] + "-" + df_raw_hanger['NO']

        self.df_raw_hanger = df_raw_hanger
        print(self.df_raw_hanger)
    
    def _check_tray_entry_columns(self):
        pass