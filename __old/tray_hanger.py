
import pandas as pd
import xlwings as xw
from pandas.api.types import is_string_dtype #for checking if the dataframe is string or not https://stackoverflow.com/questions/19900202/how-to-determine-whether-a-column-variable-is-numeric-or-not-in-pandas-numpy
import re #for regex

import shutil #this is for copying file
import os  #for checking if file exist
from os import path#for checking if file exist
import pathlib

import time #defaultInterpreterPathfor sleep
import pymsgbox #https://pymsgbox.readthedocs.io/en/latest/native.html

from _settings import *


class InputCsv:
    # cls_att_space_loaded = ''
    # cls_att_unique_blocks = []
    # cls_att_ship_no = ''

    def __init__(self):
        self.expected_column_headers = ['HANDLE', 
                                        'BLOCKNAME', 
                                        'BLOCK', 
                                        'NO', 
                                        'HANGER_SIZE', 
                                        'HANGER_HEIGHT', 
                                        'AT_SITE', 
                                        'HANGER_LENGTH', 
                                        'HANGER_TYPE_LABEL', 
                                        'SUPPORT_CODE', 
                                        'SUPPORT_NO', 
                                        'TRAY_SIZE', 
                                        'TRAY_HEIGHT', 
                                        'NO_OF_LUGS', 
                                        'TRO_ANGLE']



        self.return_string = ''
        self.space_loaded = ''
        self.unique_blocks = ''
        self.ship_no = ''



    def check_csv(self, input_csv):
        print('\n')
        print('function: --check_csv--')

        # try:
        print(f'input_csv: {input_csv}')

        read_csv = pd.read_csv(input_csv, sep='\t')
        df = pd.DataFrame(read_csv)

        csv_column_headers = self.get_column_headers(df)


        no_of_cols_expected = int(len(self.expected_column_headers))
        no_of_cols_found = 0

        # check if there csv headers are all in the expected column lists
        for col in self.expected_column_headers:

            if col in csv_column_headers:
                no_of_cols_found += 1

        
        print(f'expected_column_headers: {no_of_cols_expected}')
        print(f'no_of_cols_found: {no_of_cols_found}')

        # CHECK IF THE BLOCKS FROM THE INPUT CSV EXISTED IN THE PRE-DEFINED SORTED BLOCKS

        settings = Setting()
        setting_items = settings.items


        _path_split = input_csv.split('/')
        _file = _path_split[-1]
        print("file name", _file)

        # CHECK IF THEIR ARE EXACTLY 2 "_" FOR STANDARD FILE NAME FORMAT
        if _file.count('_') == 2:

            # GET THE SHIP NO
            str_idx = _file.find('_')
            self.ship_no = _file[:str_idx]
            

            # GET THE SPACE
            if "CW_ER" in _file:
                predef_blocks = setting_items['blocks'].get("er")
                self.space_loaded = "er"
                print(self.space_loaded)
            elif "CW_ACC" in _file:
                predef_blocks = setting_items['blocks'].get("acc")
                self.space_loaded = "acc"
                print(self.space_loaded)
            elif "CW_STG" in _file:
                predef_blocks = setting_items['blocks'].get("stg")
                self.space_loaded = "stg"
                print(self.space_loaded)
            elif "CW_BOSN" in _file:
                predef_blocks = setting_items['blocks'].get("bos")
                self.space_loaded = "bos"
                print(self.space_loaded)
            else:
                self.return_string = 'The input CSV file name is not Valid. Sample: SCXXX_CW_ER or SCXXX_CW_ACC or SCXXX_CW_STG or SCXXX_CW_BOSN'
                self.space_loaded = ""
                return False, self.return_string
            
        
        else:
            self.return_string = 'The input CSV file name is not Valid.'
            self.space_loaded = ""
            return False, self.return_string
        
        


        unique_blocks = list(set(df['BLOCK'].to_list()))
        print("unique_blocks", unique_blocks)

        try:
            unique_blocks.remove('<>')
            self.unique_blocks = unique_blocks
        except:
            self.unique_blocks = unique_blocks
        # unique_blocks.remove('<>')
        # self.cls_att_unique_blocks = unique_blocks

        blocks_not_found = []
        for block in unique_blocks:
            # print(x)

            if block in predef_blocks:
                pass
            else:
                print(block, "NOT EXIST")
                blocks_not_found.append(block)
        
        
        # DUMP TO TEXT FILE
        x_file = open("loaded_file_data.txt", "w")
        print(self.ship_no, file=x_file)
        print(self.space_loaded, file=x_file)
        blocks = ','.join([str(item) for item in self.unique_blocks])
        print(blocks, file=x_file)
        x_file.close()



        if len(blocks_not_found) != 0:
            self.return_string = f'{blocks_not_found} does not found in settings.json'
            print(self.return_string)
            return False, self.return_string

        # check the number of expected columns matched with the input csv
        if no_of_cols_found <= no_of_cols_expected:
            self.return_string = 'The input CSV is Valid.'
            print(self.return_string)
            return True, self.return_string

        else:
            self.return_string = 'The input CSV file is not Valid.'
            print(self.return_string)
            return False, self.return_string
        
        

    def get_column_headers(self, df_input):
        print('\n')
        print('function: --get_column_headers--')

        col_heads = df_input.columns
        #output in list
        col_list = col_heads.tolist()

        print(col_list)


        return col_list

#################################################################################################
#################################################################################################
########                                                                                  #######
########                                PROCESS FOR TRAY                                  #######
########                                                                                  #######
#################################################################################################
#################################################################################################

class Tray:
    """A class for Tray Processing"""


    def __init__(self, input_file_name):

        self.input_file_name = input_file_name

        self.tray_columns = ['BLOCKNAME', 'BLOCK', 'NO', 'AT_SITE', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE']
        self.tray_blocknames = ['ELECT_CWAY_TRAYBLOCK_A', 'ELECT_CWAY_TRAY_BLOCK_TRO']

        self.bracket_columns = ['BLOCKNAME', 'SUPPORT_CODE', 'SUPPORT_NO', 'BLOCK', 'NO']
        self.bracket_blocknames = ['ELECT_BRACKET']

        self.input_parent_path = 'data/_csv_input/'
        self.input_file_path = str(self.input_parent_path + self.input_file_name)
        

        
    #read csv input and convert to dataframe
    def get_tray_dataframe(self):
        print('\n')
        print('function: --get_tray_dataframe--')

        read_csv = pd.read_csv(self.input_file_path, sep='\t')
        df_tray = pd.DataFrame(read_csv, columns=self.tray_columns)

        #filter only trays
        df_tray = df_tray[df_tray['BLOCKNAME'].isin(self.tray_blocknames)]
        df_tray = df_tray.sort_values(by=['BLOCK','NO'], ascending=True)

        #replace values for lugs and TRO angle
        df_tray['NO_OF_LUGS'].replace(['<>','0','1','2'],['','X','O','T'], inplace=True)
        df_tray['TRO_ANGLE'].replace('<>','',inplace=True)

        #add 'R' to the TRO ang column
        df_tray['TRO_ANGLE']=df_tray['TRO_ANGLE'].apply(lambda row_val: '' if row_val=='' else row_val+'R')

        #create new column "BLOCK-NO"
        df_tray['BLOCK-NO'] = df_tray['BLOCK'] + "-" + df_tray['NO']

        #re-arrange column headers
        df_tray = df_tray[['BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO',  'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE','AT_SITE']]


        print(df_tray.head())

        return df_tray



    def get_bracket_dataframe(self):
        print('\n')
        print('function: --get_bracket_dataframe--')

        read_csv = pd.read_csv(self.input_file_path, sep='\t')
        df_bracket = pd.DataFrame(read_csv, columns=self.bracket_columns)

        #filter by blockname and sort by block no
        df_bracket = df_bracket[df_bracket['BLOCKNAME'].isin(self.bracket_blocknames)]
        df_bracket = df_bracket.sort_values(by=['BLOCK','NO'], ascending=True)

        #create new column "BLOCK-NO"
        df_bracket['BLOCK-NO'] = df_bracket['BLOCK'] + "-" + df_bracket['NO']

        #re-arrange column headers
        df_bracket = df_bracket[['BLOCKNAME', 'BLOCK-NO','BLOCK', 'NO','SUPPORT_CODE', 'SUPPORT_NO']]

        df_bracket = df_bracket.groupby(['BLOCK-NO','SUPPORT_CODE', 'SUPPORT_NO'])['SUPPORT_CODE'].count().reset_index(name='COUNT')
        

        print(df_bracket.head())

        return df_bracket


    def get_merged_tray_bracket_dataframe(self, df_tray, df_bracket):
        print('\n')
        print('function: --get_merged_tray_bracket_dataframe--')

        df_merged = pd.merge(df_tray, df_bracket, on='BLOCK-NO', how='outer')
        df_merged.columns = ['BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE', 'AT_SITE', 'SUPPORT_CODE', 'SUPPORT_NO', 'COUNT']


        print(df_merged.head())

        return df_merged


    def clean_tray_dataframe(self, df_input):
        print('\n')
        print('function: --clean_tray_dataframe--')

        #get column headers of the dataframe
        cols_heads = self.get_column_headers(df_input)

        #strip all white-spaces in every column
        for col in cols_heads:
            if is_string_dtype(df_input[col]):
                # df_merged[val] = df_merged[val].str.replace(' ','')
                df_input[col] = df_input[col].str.replace(' ', '')


        #replace all NAN OR NULL values with EMPTY STRING
        df_tray_cleaned = df_input.fillna('')

        print(df_tray_cleaned.head())

        return df_tray_cleaned

    def get_column_headers(self, df_input):
        print('\n')
        print('function: --get_column_headers--')

        col_heads = df_input.columns
        #output in list
        col_list = col_heads.tolist()

        print(col_list)


        return col_list
    



#################################################################################################
#################################################################################################
########                                                                                  #######
########                                PROCESS FOR HANGER                                #######
########                                                                                  #######
#################################################################################################
#################################################################################################

class Hanger:
    """A class for Hanger Processing"""


    def __init__(self, input_file_name):

        self.input_file_name = input_file_name

        self.hanger_columns = ['HANDLE', 'BLOCKNAME','BLOCK','NO','HANGER_SIZE','HANGER_HEIGHT','AT_SITE','HANGER_TYPE_LABEL','HANGER_LENGTH']
        self.hanger_blocknames = ['ELECT_HANGER_X-TYPE', 'ELECT_HANGER_H-TYPE', 'ELECT_HANGER_S-TYPE', 'ELECT_HANGER_V-TYPE']

        self.input_parent_path = 'data/_csv_input/'
        self.input_file_path = str(self.input_parent_path + self.input_file_name)


        
    #read csv input and convert to dataframe
    def get_hanger_dataframe(self):
        print('\n')
        print('function: --get_hanger_dataframe--')

        read_csv = pd.read_csv(self.input_file_path, sep='\t')
        df_hanger = pd.DataFrame(read_csv, columns=self.hanger_columns)

        #filter only trays
        df_hanger = df_hanger[df_hanger['BLOCKNAME'].isin(self.hanger_blocknames)]
        df_hanger = df_hanger.sort_values(by=['BLOCK','NO'], ascending=True)

        #strip all the white-spaces in every column
        col_heads = list(df_hanger.columns)

        for col in col_heads:
            if is_string_dtype(df_hanger[col]):
                # df_merged[val] = df_merged[val].str.replace(' ','')
                df_hanger[col] = df_hanger[col].str.replace(' ', '')
                df_hanger[col] = df_hanger[col].str.replace('<>', '')
                df_hanger[col] = df_hanger[col].str.replace('L=', '')

                #need to set REGEX =FALSE for parentheses characters
                df_hanger[col] = df_hanger[col].str.replace('(', '', regex=False)
                df_hanger[col] = df_hanger[col].str.replace(')', '', regex=False)

        #replace all NAN OR NULL values with EMPTY STRING
        df_hanger.fillna('',inplace=True)

        #remove apostrophe in the HANDLE column
        df_hanger['HANDLE'] = df_hanger['HANDLE'].apply(lambda x: x[1:]).astype(str)
        
        #create new column for HANGER TYPE
        #df_merged['tray_TYPE'] = df_merged.apply(lambda x: split_and_get_tray(x['TRAY_SIZE'],x['TRO_ANGLE'],"-",0),axis=1)
        df_hanger['hang_TYPE'] = df_hanger.apply(lambda x: self.what_hanger(x['HANGER_SIZE'],x['HANGER_LENGTH'],x['HANGER_TYPE_LABEL']),axis=1)

        #create new column for leg length (values: H=<400, H>400)
        df_hanger['LEG_CATEGORY'] = df_hanger.apply(lambda x: self.leg_category(x['HANGER_HEIGHT']),axis=1)

        #create new column "BLOCK-NO"
        df_hanger['BLOCK-NO'] = df_hanger['BLOCK'] + "-" + df_hanger['NO']

        #create new column hang_WIDTH
        df_hanger['hang_WIDTH'] = df_hanger.apply(lambda x: self.h_width(x['HANGER_SIZE']),axis=1)

        #create new columns for height 'a' and height 'b'
        df_hanger['h_height_a'] = df_hanger.apply(lambda x: self.h_height(x['HANGER_HEIGHT'], 'leg_a'),axis=1)
        df_hanger['h_height_b'] = df_hanger.apply(lambda x: self.h_height(x['HANGER_HEIGHT'], 'leg_b'),axis=1)

        #combine unique blocks
        df_hanger_leg = df_hanger.groupby(['BLOCK-NO'])['HANGER_HEIGHT'].count().reset_index(name='COUNT')

        #merge both dataframes
        df_hang_merged = pd.merge(df_hanger, df_hanger_leg, on='BLOCK-NO', how='outer')
        
        #drop duplicate values
        df_hang_merged = df_hang_merged.drop_duplicates(subset=["BLOCK-NO"])

        #re-name and re-arrange columns headers
        df_hang_merged = df_hang_merged[['HANDLE', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO',  'HANGER_SIZE', 'HANGER_HEIGHT', 'HANGER_TYPE_LABEL', 'LEG_CATEGORY', 'COUNT','hang_TYPE', 'hang_WIDTH', 'HANGER_LENGTH', 'h_height_a', 'h_height_b', 'AT_SITE']]

 


        print(df_hang_merged.head())

        return df_hang_merged
        

    def what_hanger(self, hanger_size, hanger_length, hanger_type_label):
        
        h_size = hanger_size.upper()
        h_length = hanger_length
        h_type = hanger_type_label
        h_types =['X1', 'X2', 'V1', 'V2', 'H1', 'H2']

        
        for h in h_types:
            #for X1, X2, V1, V2
            if h in h_type:
                return h

        #for H1, H2, S1, S2
        if 'AX2' in h_size and h_length == '' and h_type == '':
                return 'S2'
        elif 'AX2' in h_size and h_length != '' and h_type == '':
            return 'H2'
        elif 'AX2' not in h_size and h_length == '' and h_type == '':
            return 'S1'
        elif 'AX2' not in h_size and h_length != '' and h_type == '':
            return 'H1'
        else:
            return ''    
                
        
    def leg_category(self, hanger_height):
        
        #remove string 'H='
        leg_height = hanger_height.replace('H=', '')
        
        #check if there are 2 leg heights, separated with '/'
        if '/' in leg_height:
            leg_separated = leg_height.split('/') #returns list of values


            #return which is greater
            if leg_separated[0] > leg_separated[1]:
                leg_height = leg_separated[0]
                # return leg_height
            else:
                leg_height = leg_separated[1]
                # return leg_height

        #check if the leg height is H>400 or not
        if int(leg_height) <= 400:
            leg_height = 'H<=400'
        else:
            leg_height = 'H>400'

        return leg_height


    def h_width(self, hanger_size):

        x_pos = hanger_size.find('A')

        #slice string
        h_width = hanger_size[:x_pos]

        return h_width


    def h_height(self, hanger_height, leg_no):
        
        #remove 'H=' label
        if 'H=' in hanger_height:
            #remove 'H=' by slicing the string
            hanger_height = hanger_height[2:]


        #for leg a
        if leg_no == 'leg_a':

            #check if there are 2 leg heights, separated with '/'
            if '/' not in hanger_height:
                h_height = hanger_height
                return h_height

            else:
                h_height = hanger_height.split('/') #returns list of values
                # print(h_height[0] + '  ' + h_height[1])
                h_height = h_height[0]
                return h_height

        #for leg b
        if leg_no == 'leg_b':

            #check if there are 2 leg heights, separated with '/'
            if '/' not in hanger_height:
                h_height = hanger_height
                return h_height

            else:
                h_height = hanger_height.split('/') #returns list of values
                # print(h_height[0] + '  ' + h_height[1])
                h_height = h_height[1]
                return h_height



    def get_column_headers(self, df_input):
        print('\n')
        print('function: --get_column_headers--')

        col_heads = df_input.columns
        #output in list
        col_list = col_heads.tolist()

        print(col_list)


        return col_list
    

    
   

   
#################################################################################################
#################################################################################################
########                                                                                  #######
########                      FOR OUTPUTING DATAFRAMES TO EXCEL                           #######
########                                                                                  #######
#################################################################################################
#################################################################################################


class CreateExcelOutput:

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output_parent_path = 'data/_output/'


    def output_to_excel(self, input_df, output_sheet_name):
        '''
            Create only ONE excel file
        '''

        print('\n')
        print('function: --output_to_excel--')

        output_file = self.output_parent_path + self.output_file_name + '.xlsx'
        print(f'output_file: {output_file}')
        input_df.to_excel(output_file, sheet_name=output_sheet_name, index=False)
        
        print(f'file {output_file} created')
    


    def output_to_excel_in_one_file(self, input_dfs, output_sheet_names):

        ''' 
            *** CREATING ONE EXCEL FILE WITH MULTIPLE SHEETS ***
            REFERENCE: https://www.geeksforgeeks.org/how-to-write-pandas-dataframes-to-multiple-excel-sheets/

                input_dfs: list of dataframes
                output_sheet_names: list of sheet_names for each assigned dataframe

                !!! both lists should be the same in length
        '''
        print('\n')
        print('function: --output_to_excel_in_one_file--')

        df_list = input_dfs
        sheet_name_list = output_sheet_names

        output_file = self.output_parent_path + self.output_file_name + '.xlsx'

        print(f'output_file: {output_file}')
        
        
        # create a excel writer object
        with pd.ExcelWriter(output_file) as writer:

            sheet_list_index_val = 0

            #loop thru all dataframes
            for df in df_list:
                
                current_sheet_name = sheet_name_list[sheet_list_index_val]
                df.to_excel(writer, sheet_name = current_sheet_name, index=False)

                print(f'sheet "{current_sheet_name}" created')
                sheet_list_index_val += 1



        print(f'file {output_file} created')