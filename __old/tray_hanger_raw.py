
import pandas as pd
import xlwings as xw
from pandas.api.types import is_string_dtype #for checking if the dataframe is string or not https://stackoverflow.com/questions/19900202/how-to-determine-whether-a-column-variable-is-numeric-or-not-in-pandas-numpy
# import re #for regex

# import shutil #this is for copying file
# import os  #for checking if file exist
# from os import path#for checking if file exist
# import pathlib

import time #defaultInterpreterPathfor sleep
import pymsgbox #https://pymsgbox.readthedocs.io/en/latest/native.html






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

        self.tray_columns = ['HANDLE', 'BLOCKNAME', 'BLOCK', 'NO', 'AT_SITE', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE']
        self.tray_blocknames = ['ELECT_CWAY_TRAYBLOCK_A', 'ELECT_CWAY_TRAY_BLOCK_TRO']

        self.bracket_columns = ['BLOCKNAME', 'SUPPORT_CODE', 'SUPPORT_NO', 'BLOCK', 'NO']
        self.bracket_blocknames = ['ELECT_BRACKET']

        self.input_parent_path = 'data/_csv_input/'
        self.input_file_path = str(self.input_parent_path + self.input_file_name)
        

    def process_object_handle(self, object_handle):
        
        object_handle = object_handle[1:]

        new_handle = f'SELECT (HANDENT "{object_handle}")'

        return new_handle

        
    #read csv input and convert to dataframe
    def get_tray_dataframe(self):
        print('\n')
        print('MAIN function: --get_tray_dataframe--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "w")
        print('---> process logger <---', file=f)
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --get_tray_dataframe--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################


        read_csv = pd.read_csv(self.input_file_path, sep='\t')
        df_tray = pd.DataFrame(read_csv, columns=self.tray_columns)


        #filter only trays
        df_tray = df_tray[df_tray['BLOCKNAME'].isin(self.tray_blocknames)]
        df_tray = df_tray.sort_values(by=['BLOCK','NO'], ascending=True)

        try:
            #replace values for lugs and TRO angle
            df_tray['NO_OF_LUGS'].replace(['<>','0','1','2'],['','X','O','T'], inplace=True)
            df_tray['TRO_ANGLE'].replace('<>','',inplace=True)

            #add 'R' to the TRO ang column
            df_tray['TRO_ANGLE']=df_tray['TRO_ANGLE'].apply(lambda row_val: '' if row_val=='' else row_val+'R')
        except:
            pass
        
        #create new column "BLOCK-NO"
        df_tray['BLOCK-NO'] = df_tray['BLOCK'] + "-" + df_tray['NO']

        #re-arrange column headers
        df_tray = df_tray[['HANDLE', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO',  'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE','AT_SITE']]
        df_tray.to_excel("data/_output_temp_data/1_df_tray.xlsx")
        
        #get frame dataframe
        df_bracket = self.get_bracket_dataframe()
        df_bracket.to_excel("data/_output_temp_data/2_df_bracket.xlsx")

        #merge df_tray and df_bracket
        df_merged = self.get_merged_tray_bracket_dataframe(df_tray, df_bracket)
        df_merged.to_excel("data/_output_temp_data/3_df_merged.xlsx")

        #clean merged dataframe and assign it to be the new tray dataframe
        df_tray_cleaned = self.clean_tray_dataframe(df_merged)
        df_tray_cleaned.to_excel("data/_output_temp_data/4_df_tray_cleaned.xlsx")
        
        #create new columns headers for preparation
        df_tray = self.create_new_columns_tray(df_tray_cleaned)
        df_tray.to_excel("data/_output_temp_data/5_df_tray.xlsx")

        # PROCESS OBJECT HANDLE STRINGS
        df_tray['HANDLE'] = df_tray['HANDLE'].apply(self.process_object_handle)



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
        

        return df_bracket


    def get_merged_tray_bracket_dataframe(self, df_tray, df_bracket):
        print('\n')
        print('function: --get_merged_tray_bracket_dataframe--')

        df_merged = pd.merge(df_tray, df_bracket, on='BLOCK-NO', how='outer')
        df_merged.columns = ['HANDLE', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO', 'TRAY_SIZE', 'NO_OF_LUGS', 'TRO_ANGLE', 'AT_SITE', 'SUPPORT_CODE', 'SUPPORT_NO', 'COUNT']


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

        # CREATE/OPEN TEXT FILE FOR LOGGER
        f = open("process_logger.txt", "a")
        # print(df_tray_cleaned.head())
        print(df_tray_cleaned, file=f)
        f.close()

        return df_tray_cleaned

    def create_new_columns_tray(self, df_input):
        print('\n')
        print('function: --create_new_columns_tray--')

        print("df_input",df_input)

        #expand columns with "-" for tray and bracket, new columns are to be created
        df_input['tray_TYPE'] = df_input.apply(lambda x: self.split_and_get_tray(x['TRAY_SIZE'],x['TRO_ANGLE'],"-",0),axis=1)
        df_input['tray_WIDTH'] = df_input.apply(lambda x: self.split_and_get_tray(x['TRAY_SIZE'],x['TRO_ANGLE'],"-",1),axis=1)
        df_input['tray_LENGTH'] = df_input.apply(lambda x: self.split_and_get_tray(x['TRAY_SIZE'],x['TRO_ANGLE'],"-",2),axis=1)

        df_input['bracket_TYPE'] = df_input.apply(lambda x: self.split_and_get_bracket(x['SUPPORT_CODE'],"-",0),axis=1)
        df_input['bracket_WIDTH'] = df_input.apply(lambda x: self.split_and_get_bracket(x['SUPPORT_CODE'],"-",1),axis=1)
        df_input['bracket_HEIGHT'] = df_input.apply(lambda x: self.split_and_get_bracket(x['SUPPORT_CODE'],"-",2),axis=1)

        return df_input

    # splitting the TRAY_SIZE column values
    def split_and_get_tray(self, string_to_split, option_string, separator, returned_index):
        #   sample values
            #   string_to_split => To-60-16.7, TR0-50
            #   option_string => 90R
            #   separator => "-"
            #   returned_index => 0, 1, 2

        ret_val = string_to_split.split(separator)

        #to identify if the current value is from TO or TRO
        if len(ret_val) < 3:
            ret_val.append(option_string)
            print("string_to_split", "ret_val", ret_val)

        print("string_to_split", "ret_val", ret_val)

        return ret_val[returned_index]


    # splitting the SUPPORT_CODE column values and applying calculation
    def split_and_get_bracket(self, string_to_split, separator, returned_index):
        #   sample values
            #   string_to_split => U-60-85, U-60-85/45
            #   separator => "-"
            #   returned_index => 0, 1, 2

        #check first if the current value is EMPTY
        if string_to_split == "":
            pass
            #this means if the value us empty, the program will exit if statement

        else:
            ret_val = str(string_to_split).split(separator)    

            if returned_index == 0:

                return str(ret_val[0])
            elif returned_index == 1:

                val_1 = float(ret_val[1])
                val_1 = val_1*10

                return str(val_1)
            elif returned_index == 2:
                if "/" in ret_val[2]:
                    # print('theres "/"')
                    #separate values
                    val_2 = str(ret_val[2]).split("/")

                    val_2[0] = round(float(val_2[0])*10)
                    val_2[1] = round(float(val_2[1])*10)

                    new_val_2 = str(val_2[0]) + "/" + str(val_2[1])

                    return str(new_val_2)
                else:
                    return str(round(float(ret_val[2])*10))
            else:
                return ""




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
        self.hanger_blocknames = ['ELECT_HANGER_SX-TYPE', 'ELECT_HANGER_H-TYPE', 'ELECT_HANGER_S-TYPE', 'ELECT_HANGER_HV-TYPE']

        self.input_parent_path = 'data/_csv_input/'
        self.input_file_path = str(self.input_parent_path + self.input_file_name)


    def process_object_handle_hanger(self, object_handle):
        
        object_handle_hanger = object_handle[1:]

        new_handle = f'SELECT (HANDENT "{object_handle_hanger}")'

        return new_handle
        

    #read csv input and convert to dataframe
    def get_hanger_dataframe(self):
        print('\n')
        print('function: --get_hanger_dataframe--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --get_hanger_dataframe--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################

        read_csv = pd.read_csv(self.input_file_path, sep='\t')
        df_hanger = pd.DataFrame(read_csv, columns=self.hanger_columns)

        #filter only trays
        df_hanger = df_hanger[df_hanger['BLOCKNAME'].isin(self.hanger_blocknames)]
        df_hanger = df_hanger.sort_values(by=['BLOCK','NO'], ascending=True)
        df_hanger.to_excel("data/_output_temp_data/6_df_hanger.xlsx")

        #strip all the white-spaces in every column
        col_heads = list(df_hanger.columns)

        for col in col_heads:
            if is_string_dtype(df_hanger[col]):
                # df_merged[val] = df_merged[val].str.replace(' ','')
                df_hanger[col] = df_hanger[col].str.replace(' ', '')
                df_hanger[col] = df_hanger[col].str.replace('<>', '')
                df_hanger[col] = df_hanger[col].str.replace('L=', '')
                df_hanger[col] = df_hanger[col].str.replace('DH=', '')
                df_hanger[col] = df_hanger[col].str.replace('H=', '')

                #need to set REGEX =FALSE for parentheses characters
                df_hanger[col] = df_hanger[col].str.replace('(', '', regex=False)
                df_hanger[col] = df_hanger[col].str.replace(')', '', regex=False)

        #replace all NAN OR NULL values with EMPTY STRING
        df_hanger.fillna('',inplace=True)

        #remove apostrophe in the HANDLE column
        # df_hanger['HANDLE'] = df_hanger['HANDLE'].apply(lambda x: x[1:]).astype(str)
        
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
        df_hanger['h_height_a'] = df_hanger.apply(lambda x: self.h_height(x['HANGER_HEIGHT'], x['HANGER_LENGTH'], x['hang_TYPE'], 'leg_a'),axis=1)
        df_hanger['h_height_b'] = df_hanger.apply(lambda x: self.h_height(x['HANGER_HEIGHT'], x['HANGER_LENGTH'], x['hang_TYPE'], 'leg_b'),axis=1)

        df_hanger.to_excel("data/_output_temp_data/7_df_hanger.xlsx")

        #combine unique blocks
        df_hanger_leg = df_hanger.groupby(['BLOCK-NO'])['HANGER_HEIGHT'].count().reset_index(name='COUNT')
        df_hanger_leg.to_excel("data/_output_temp_data/8_df_hanger.xlsx")

        #merge both dataframes
        df_hang_merged = pd.merge(df_hanger, df_hanger_leg, on='BLOCK-NO', how='outer')
        
        #drop duplicate values
        df_hang_merged = df_hang_merged.drop_duplicates(subset=["BLOCK-NO"])

        #re-name and re-arrange columns headers
        df_hang_merged = df_hang_merged[['HANDLE', 'BLOCKNAME', 'BLOCK-NO', 'BLOCK', 'NO',  'HANGER_SIZE', 'HANGER_HEIGHT', 'HANGER_TYPE_LABEL', 'LEG_CATEGORY', 'COUNT','hang_TYPE', 'hang_WIDTH', 'HANGER_LENGTH', 'h_height_a', 'h_height_b', 'AT_SITE']]
        df_hang_merged.to_excel("data/_output_temp_data/9_df_hanger.xlsx")

        # PROCESS OBJECT HANDLE STRINGS
        df_hang_merged['HANDLE'] = df_hang_merged['HANDLE'].apply(self.process_object_handle_hanger)


        return df_hang_merged
        

    def what_hanger(self, hanger_size, hanger_length, hanger_type_label):
        
        h_size = hanger_size.upper()
        h_length = hanger_length
        h_type = hanger_type_label
        h_types =['X1', 'X2', 'V1', 'V2', 'H1', 'H2', 'H3', 'H4','S1', 'S2', 'S3', 'S4']

        
        for h in h_types:
            #for X1, X2, V1, V2, S3, S4, H3, H4
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


    def h_height(self, hanger_height, hanger_length, hang_type, leg_no):
            
        #remove 'H=' label
        if 'H=' in hanger_height:
            #remove 'H=' by slicing the string
            hanger_height = hanger_height[2:]

        #check if there are 2 leg heights, separated with '/'
        if '/' not in hanger_height:

            if hang_type in ['V1', 'V2']:
                h_height = int(hanger_height) + int(hanger_length) + 25
                return h_height

            elif hang_type in ['X1', 'X2']:
                h_height = int(hanger_height) + 25
                return h_height
            
            elif hang_type in ['S3', 'S4', 'H3', 'H4']:
                h_height = int(hanger_height) + 50
                return h_height

            else:
                h_height = int(hanger_height) - 10
                return h_height

        else:
            h_height = hanger_height.split('/') #returns list of values

            #for leg a
            if leg_no == 'leg_a':
                h_height = int(h_height[0]) - 10
                return h_height

            #for leg b
            if leg_no == 'leg_b':
                h_height = int(h_height[1]) - 10
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


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --output_to_excel_in_one_file--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################


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