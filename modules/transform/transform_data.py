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
        self.tray_columns = ['HANDLE', 'SELECTION', 'ZOOM', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE', 'AT_SITE']
        self.bracket_columns = ['BLOCKNAME', 'SELECTION', 'ZOOM', 'BLOCK-NO', 'BLOCK', 'NO', 'SUPPORT_CODE', 'SUPPORT_NO']
        self.hanger_columns = ['HANDLE', 'SELECTION', 'ZOOM', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO', 'HANGER_SIZE', 'HANGER_HEIGHT', 'HANGER_TYPE_LABEL', 'HANGER_LENGTH', 'AT_SITE']

        # ['BLOCKNAMES']
        self.hanger_blocknames = ['ELECT_HANGER_SX-TYPE', 'ELECT_HANGER_H-TYPE', 'ELECT_HANGER_S-TYPE', 'ELECT_HANGER_HV-TYPE']
        self.bracket_blocknames = ['ELECT_BRACKET']
        self.tray_blocknames = ['ELECT_CWAY_TRAYBLOCK_A', 'ELECT_CWAY_TRAY_BLOCK_TRO']

        self._read_data()
        self._get_raw_tray()
        self._get_raw_hanger()
        self._get_raw_bracket()


    def _read_data(self):
        # print(self.raw_data_file_path)
        try:
            df_raw_data = pd.read_csv(self.raw_data_file_path, sep='\t')
            df_raw_data['SELECTION'] = df_raw_data.apply(lambda x: self._apply_create_selection_tag(x['HANDLE']), axis=1)
            df_raw_data['ZOOM'] = df_raw_data.apply(lambda x: self._apply_create_zoom_tag(x['HANDLE']), axis=1)
            df_raw_data.fillna('', inplace=True)
            self.df_raw_data = df_raw_data
            return self.df_raw_data
        except:
            self.return_error = 'INVALID INPUT CONTENTS'

    def _replace_nulls(self, df):
        df = df.fillna(None)
        col_heads = list(df.columns)
        
        for col in col_heads:
            df[col] = df[col].str.replace('<>', '')
        
        return df

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
        # print(self.df_raw_data)

        # filter only trays
        df_raw_tray = df_raw_tray[df_raw_tray['BLOCKNAME'].isin(self.tray_blocknames)]
        df_raw_tray = df_raw_tray.sort_values(by=['BLOCK', 'NO'], ascending=True)
        
        # add missing columns
        df_raw_tray = self._check_raw_data_headers(df_raw_tray, self.tray_columns)
        
        # create new column "BLOCK-NO"
        df_raw_tray['BLOCK-NO'] = df_raw_tray['BLOCK'] + "-" + df_raw_tray['NO']

        # re-arrange column headers
        df_raw_tray = df_raw_tray[self.tray_columns]

        self.df_raw_tray = df_raw_tray
        # print(self.df_raw_tray)

    def _get_raw_hanger(self):
        df_raw_hanger = (self.df_raw_data).copy()
        # print(self.df_raw_hanger)

        # filter only hangers
        df_raw_hanger = df_raw_hanger[df_raw_hanger['BLOCKNAME'].isin(self.hanger_blocknames)]
        df_raw_hanger = df_raw_hanger.sort_values(by=['BLOCK', 'NO'], ascending=True)
        
        # add missing columns
        df_raw_hanger = self._check_raw_data_headers(df_raw_hanger, self.hanger_columns)

        # create new column "BLOCK-NO"
        df_raw_hanger['BLOCK-NO'] = df_raw_hanger['BLOCK'] + "-" + df_raw_hanger['NO']

        # re-arrange column headers
        df_raw_hanger = df_raw_hanger[self.hanger_columns]

        self.df_raw_hanger = df_raw_hanger
        # print(self.df_raw_hanger)

    def _get_raw_bracket(self):
        df_raw_bracket = (self.df_raw_data).copy()

        # filter only bracket
        df_raw_bracket = df_raw_bracket[df_raw_bracket['BLOCKNAME'].isin(self.bracket_blocknames)]
        df_raw_bracket = df_raw_bracket.sort_values(by=['BLOCK', 'NO'], ascending=True)

        # add missing columns
        df_raw_bracket = self._check_raw_data_headers(df_raw_bracket, self.bracket_columns)

        # create new column "BLOCK-NO"
        df_raw_bracket['BLOCK-NO'] = df_raw_bracket['BLOCK'] + "-" + df_raw_bracket['NO']

        # re-arrange column headers
        df_raw_bracket = df_raw_bracket[self.bracket_columns]

        self.df_raw_bracket = df_raw_bracket

    
    def _apply_create_selection_tag(self, handle_str):
        selection_str = f'SELECT (HANDENT"{handle_str[1:]}")'
        # print(selection_str)
        return selection_str

    def _apply_create_zoom_tag(self, handle_str):
        selection_str = f'ZOOM OBJECT (HANDENT"{handle_str[1:]}")  '
        # print(selection_str)
        return selection_str


# class Checker:
#     def __init__(self):
#         pass
    
#     def check_rows_with_nulls(self, df):

#         return df[df.isna().any(axis=1)]

#     def check_tray(self, df_tray):
#         if len(df_tray) == 0:
#             return df_tray
#         else:
#             # df_tray['BLOCK'] = df_tray['BLOCK'].astype('string')
#             # check all columns
#             df_tray['BLOCK_ERROR'] = df_tray.apply(lambda x: self._apply_check_block(x['BLOCK']), axis=1)
#             df_tray['NO_ERROR'] = df_tray.apply(lambda x: self._apply_check_no(x['NO'], 'TRAY'), axis=1)
#             df_tray['TRAY_SIZE_ERROR'] = df_tray.apply(lambda x: self._apply_check_tray_size(x['TRAY_SIZE']), axis=1)
#             df_tray['LUGS_ERROR'] = df_tray.apply(lambda x: self._apply_check_tray_lugs(x['NO_OF_LUGS']), axis=1)
#             df_tray['TRO_ANGLE_ERROR'] = df_tray.apply(lambda x: self._apply_check_tro_angle(x['BLOCKNAME'], x['TRO_ANGLE']), axis=1)
#             df_tray['AT_SITE_ERROR'] = df_tray.apply(lambda x: self._apply_check_atsite(x['AT_SITE']), axis=1)


#             self._mark_tray_rows_with_errors(df_tray)            
#             return df_tray
    
#     def _mark_tray_rows_with_errors(self, df):
#         # df['ROW_WITH_ERROR'] = df[df['BLOCK_ERROR']=='X' or df['NO_ERROR']=='X']
#         df.loc[
#                 (df['BLOCK_ERROR'] == 'X') | 
#                 (df['NO_ERROR'] == 'X') | 
#                 (df['TRAY_SIZE_ERROR'] == 'X') | 
#                 (df['LUGS_ERROR'] == 'X') | 
#                 (df['TRO_ANGLE_ERROR'] == 'X') | 
#                 (df['AT_SITE_ERROR'] == 'X'),
#                 'ROW_WITH_ERROR'] = 'X'

        
#     def _apply_check_block(self, _block):
#         if _block is None:
#             return 'X'
#         if _block == '':
#             return 'X'

#     def _apply_check_no(self, _no, _hanger_or_tray_or_bracket):
#         if _no is None:
#             return 'X'
#         if _no == '':
#             return 'X'
#         if _hanger_or_tray_or_bracket == 'TRAY' or _hanger_or_tray_or_bracket == 'BRACKET':
#             if len(_no.strip()) != 1:
#                 return 'X'
#         if _hanger_or_tray_or_bracket == 'HANGER':
#             if len(_no.strip()) != 2:
#                 return 'X'
#             if _no.strip() == 'XX':
#                 return 'X'

#     def _apply_check_tray_size(self, tray_size):
#         try:
#             ret_val = ''
#             tray_size = tray_size.strip().upper()
#             print(tray_size)
#             if tray_size is None:
#                 return 'X'
#             if tray_size == '':
#                 return 'X'

#             # slice, sample: To-50-19.5, TRo-25
#             _tray = tray_size.split('-')
            
#             # SEPARATE TRO & TO
#             if len(_tray) == 2: # means TRO
#                 if _tray[0] != 'TRO': ret_val = 'X'
#                 if len(_tray[1]) != 2: ret_val = 'X'
#             elif len(_tray) == 3: # means TO
#                 if _tray[0] != 'TO': ret_val = 'X'
#                 if (float(_tray[2])*100) > 2440: ret_val = 'X' # means tray lenth is greater that 2440
#             else:
#                 ret_val = ''
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_tray_lugs(self, lugs):
#         try:
#             ret_val = ''
#             if lugs == '<>': # means null
#                 pass
#             elif int(lugs) in [0, 1, 2]:
#                 pass
#             else:
#                 ret_val = 'X'
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_tro_angle(self, block_name, tro_angle):
#         try:
#             ret_val = ''
            
#             if block_name == 'ELECT_CWAY_TRAYBLOCK_A': # means null
#                 if tro_angle == '<>' or tro_angle == '':
#                     pass
#             elif len(tro_angle) == 2 and block_name == 'ELECT_CWAY_TRAY_BLOCK_TRO':
#                 pass
#             else:
#                 ret_val = 'X'
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_atsite(self, atsite):
#         try:
#             ret_val = ''
#             if atsite.strip() in ['NO', 'YES']:
#                 pass
#             else:
#                 ret_val = 'X'
#             return ret_val
#         except:
#             return 'X'
            
#     def check_hanger(self, df_hanger):
#         if len(df_hanger) == 0:
#             return df_hanger
#         else:
#             df_hanger['BLOCK_ERROR'] = df_hanger.apply(lambda x: self._apply_check_block(x['BLOCK']), axis=1)
#             df_hanger['NO_ERROR'] = df_hanger.apply(lambda x: self._apply_check_no(x['NO'], 'HANGER'), axis=1)
#             df_hanger['HANGER_SIZE_ERROR'] = df_hanger.apply(lambda x: self._apply_check_hanger_size(x['HANGER_SIZE']), axis=1)
#             df_hanger['HANGER_HEIGHT_ERROR'] = df_hanger.apply(lambda x: self._apply_check_hanger_height(x['HANGER_HEIGHT']), axis=1)
#             df_hanger['HANGER_TYPE_LABEL_ERROR'] = df_hanger.apply(lambda x: self._apply_check_hanger_type_label(x['BLOCKNAME'], x['HANGER_TYPE_LABEL']), axis=1)
#             df_hanger['HANGER_LENGTH_ERROR'] = df_hanger.apply(lambda x: self._apply_check_hanger_length(x['HANGER_LENGTH']), axis=1)
#             df_hanger['AT_SITE_ERROR'] = df_hanger.apply(lambda x: self._apply_check_atsite(x['AT_SITE']), axis=1)

#             self._mark_hanger_rows_with_errors(df_hanger)
#             return df_hanger

#     def _mark_hanger_rows_with_errors(self, df):
       
#         df.loc[
#                 (df['BLOCK_ERROR'] == 'X') | 
#                 (df['NO_ERROR'] == 'X') | 
#                 (df['HANGER_SIZE_ERROR'] == 'X') | 
#                 (df['HANGER_HEIGHT_ERROR'] == 'X') | 
#                 (df['HANGER_TYPE_LABEL_ERROR'] == 'X') | 
#                 (df['HANGER_LENGTH_ERROR'] == 'X') | 
#                 (df['AT_SITE_ERROR'] == 'X'),
#                 'ROW_WITH_ERROR'] = 'X'

#     def _apply_check_hanger_size(self, hanger_size):
#         try:
#             hanger_size = hanger_size.upper()
#             ret_val = ''
#             print(hanger_size, hanger_size.find('AX'), hanger_size.find('AX2'))
#             if (hanger_size.find('A') != -1) or (hanger_size.find('AX2') != -1):
#                 pass # means the string is found
#             else:
#                 ret_val = 'X'
#             if (hanger_size.find('AX') > 0) and (hanger_size.find('AX2') == -1): # special case
#                 ret_val = 'X'
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_hanger_height(self, hanger_height):
#         try:
#             ret_val = ''
#             hanger_height = hanger_height.strip()

#             if hanger_height == None: ret_val = 'X'
#             if hanger_height == '': ret_val = 'X'

#             if hanger_height.find('/') > 0: # means that there two heights
#                 if hanger_height.find(')') > 0:
#                     hanger_height = hanger_height[hanger_height.find('=')+1:-1]
#                     h1, h2 = hanger_height.split('/')
#                 else:
#                     hanger_height = hanger_height[hanger_height.find('=')+1:]                
#                     h1, h2 = hanger_height.split('/')
#                 print(hanger_height, h1, h2)
#                 try:
#                     h1 = int(h1)
#                     h2 = int(h2)
#                 except:
#                     return 'X'

#                 return ret_val
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_hanger_type_label(self, block_name, hanger_type_label):
#         try:
#             ret_val = ''
#             hanger_type_label = hanger_type_label.strip().upper()

#             if hanger_type_label == None: ret_val = 'X'
#             if hanger_type_label == '': ret_val = 'X'

#             found_ctr = 0
#             for label in ['TYPE', 'X1', 'X2', 'V1', 'V2', 'S3', 'S4', 'H3', 'H4']:
#                 if hanger_type_label.find(label) > 0: found_ctr += 1
            
#             if found_ctr == 0:
#                 if (hanger_type_label == '<>') and (block_name in ['ELECT_HANGER_S-TYPE', 'ELECT_HANGER_H-TYPE']):
#                     pass
#                 else:
#                     ret_val = 'X' 
#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_hanger_length(self, hanger_length):
#         try:
#             ret_val = ''

#             hanger_length = hanger_length.strip('()L=-').upper()

#             if hanger_length == None: ret_val = 'X'
#             if hanger_length == '': ret_val = 'X'
#             if hanger_length == 0: ret_val = 'X'
#             if hanger_length == '<>':
#                 pass
#             elif int(hanger_length) not in [300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700]: ret_val = 'X'
    
#             return ret_val

#         except:
#             return 'X'

#     def check_bracket(self, df_bracket):
#         if len(df_bracket) == 0:
#             return df_bracket
#         else:
#             # df_tray['BLOCK'] = df_tray['BLOCK'].astype('string')
#             # check all columns
#             df_bracket['BLOCK_ERROR'] = df_bracket.apply(lambda x: self._apply_check_block(x['BLOCK']), axis=1)
#             df_bracket['NO_ERROR'] = df_bracket.apply(lambda x: self._apply_check_no(x['NO'], 'BRACKET'), axis=1)
#             df_bracket['SUPPORT_CODE_ERROR'] = df_bracket.apply(lambda x: self._apply_check_bracket_support_code(x['SUPPORT_CODE']), axis=1)
#             df_bracket['SUPPORT_NO_ERROR'] = df_bracket.apply(lambda x: self._apply_check_bracket_support_no(x['SUPPORT_NO']), axis=1)

#             self._mark_bracket_rows_with_errors(df_bracket)            
#             return df_bracket

#     def _mark_bracket_rows_with_errors(self, df):
       
#         df.loc[
#                 (df['BLOCK_ERROR'] == 'X') | 
#                 (df['NO_ERROR'] == 'X') | 
#                 (df['SUPPORT_CODE_ERROR'] == 'X') | 
#                 (df['SUPPORT_NO_ERROR'] == 'X'),
#                 'ROW_WITH_ERROR'] = 'X'

#     def _apply_check_bracket_support_code(self, support_code):
#         try:
#             ret_val = ''
#             support_code = support_code.strip().upper()
#             c1, c2, c3 = support_code.split('-')

#             if c1 not in ['E', 'I', 'U', 'L']: ret_val = 'X'

#             c2 = float(c2)

#             if c3.find('/') > 0: # means  different leg heights
#                 c3_a, c3_b = c3.split('/')

#                 c3_a = float(c3_a)
#                 c3_b = float(c3_b)
#             else:
#                 c3 = float(c3)

#             return ret_val
#         except:
#             return 'X'

#     def _apply_check_bracket_support_no(self, support_no):
#         try:
#             ret_val = ''
#             support_no = support_no.strip().upper()

#             if len(support_no) < 3: ret_val = 'X'

#             support_no = int(support_no)
            
#             return ret_val
#         except:
#             return 'X'