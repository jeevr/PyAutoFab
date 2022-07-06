# from ast import Pass
# from enum import unique
# from json import load
# from re import T
# from turtle import textinput
# from numpy import append
import pandas as pd
import xlwings as xw
import time

from _settings import Setting
# from tray_hanger import InputCsv


# from PySide6.QtGui import *
# from PySide6.QtCore import *
# from PySide6.QtWidgets import QInputDialog


class RawToExcelStandardFormat:

    def __init__(self):
        
        #excel file where raw data of tray and hanger saved
        self.source_file = 'data/_output/temp_output_data.xlsx'

        #excel file for the standard format
        self.destination_file = 'data/_output/THFL.xls'


        self.x_space_loaded = ''
        self.x_unique_blocks = ''
        self.x_ship_no = ''


    def get_unique_blocks_and_sort(self, df_input):
        print('\n')
        print('function: --get_unique_blocks_and_sort--')

        # get the unique blocks from the dataframe
        df_blocks = df_input['BLOCK'].unique()

        # create an empty list
        block_index_new = []

        # count the number for each unique blocks
        df_count_per_block = df_input.groupby(['BLOCK'])['BLOCK'].count().reset_index(name='counts')

        # create a algorithm that will interchange the block with (S) and (P)
        x=1
        for block in df_blocks:
            # for x in range(len(blocks)):
            if 'S' in block:
                block_index_new.append( x - 1 )
            elif 'P' in block:
                block_index_new.append( x + 1 )
            else:
                block_index_new.append( x )
            x += 1

        # create a new dataframe from the created dictionary of the sorted blocks
        new_df = {    'BLOCK':df_blocks,
                    'SORT_NO':block_index_new
                }

        df_sorted_blocks = pd.DataFrame(new_df).sort_values('SORT_NO')
        df_sorted_blocks =  df_sorted_blocks.reset_index(drop=True)

        sorted_block_list = df_sorted_blocks['BLOCK'].tolist()

 
        df_sorted_blocks = pd.merge(df_sorted_blocks, df_count_per_block, on='BLOCK', how='inner')


        return [sorted_block_list, df_sorted_blocks]


    def get_unique_blocks_and_sort_V2(self, df_input):
        print('\n')
        print('function: --get_unique_blocks_and_sort--')

        # get the unique blocks from the dataframe
        df_blocks = df_input['BLOCK'].unique() # list 1


        # count the number for each unique blocks
        df_count_per_block = df_input.groupby(['BLOCK'])['BLOCK'].count().reset_index(name='counts')

    
        # CREATE A NEW LIST OF SORTED BLOCKS
        # GET DATA FROM SETTINGS.JSON FILE
        _blocks_settings = Setting()
        _blocks = _blocks_settings.items

        loaded_file = open("loaded_file_data.txt", "r")
        self.x_ship_no = str(loaded_file.readline()).strip()
        self.x_space_loaded = str(loaded_file.readline()).strip()
        self.x_unique_blocks = str(loaded_file.readline()).split(',')
        self.x_unique_blocks[-1] = str(self.x_unique_blocks[-1]).strip()

        print('wiring space', self.x_space_loaded)
        _list_blocks = _blocks['blocks'][self.x_space_loaded] # list 2
        print("_list_blocks", _list_blocks)
        # apply list comprehension to get the sorted blocks as per predefined collection of blocks
        sorted_blocks = [x for x in _list_blocks if x in df_blocks]

        print("sorted blocks", sorted_blocks)

        # CREATE A DATAFRAME FROM THE SORTED LIST
        df_sorted_blocks = pd.DataFrame(sorted_blocks, columns =['BLOCK'])
        print(df_sorted_blocks)
 
        df_blocks_sorted = pd.merge(df_sorted_blocks, df_count_per_block, on='BLOCK', how='inner')
        print(df_sorted_blocks)

        return [sorted_blocks, df_blocks_sorted]


    def transform_raw_to_standard(self, df_tray, df_hanger):
        print('\n')
        print('function: --transform_raw_to_standard--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --transform_raw_to_standard--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################


        #open the excel file in the background
        with xw.App(visible=False):
            
            # open the source file
            wb_src = xw.Book(self.source_file)

            # assign for each sheets: tray and hanger
            # wb_src_sht_tray = self.wb_src.sheets['for_tray']
            # wb_src_sht_hanger = self.wb_src.sheets['for_hanger']


            # open the destination file
            wb_dst = xw.Book(self.destination_file) 
            
            # assign for each sheets: tray and hanger
            wb_dst_sht_tray = wb_dst.sheets['TFL-ER']
            wb_dst_sht_hanger = wb_dst.sheets['HFL-ER']

            
            # call the function to transform tray
            self.transform_tray(df_tray, wb_dst_sht_tray)

            
            # call the function to transform hanger
            self.transform_hanger_V2(df_hanger, wb_dst_sht_hanger)
            
            # PAGING (ADD PAGING INTO FORMAT)
            self.assign_page(wb_dst_sht_tray, wb_dst_sht_hanger)


            wb_dst.save(self.destination_file)
            wb_src.save(self.source_file)
            print('workbooks saved')

            time.sleep(1)
            
            wb_dst.close()
            wb_src.close()

            time.sleep(1)

            print('workbooks closed')


    def transform_tray(self, df_tray, wb_dst_sht_tray):
        print('\n')
        print('function: --transform_tray--')

        
        # get unique tray blocks
        # tray_blocks_sorted_list = self.get_unique_blocks_and_sort(df_tray)[0]
        # df_tray_count_per_block_sorted = self.get_unique_blocks_and_sort(df_tray)[1]
        tray_blocks_sorted_list = self.get_unique_blocks_and_sort_V2(df_tray)[0]
        df_tray_count_per_block_sorted = self.get_unique_blocks_and_sort_V2(df_tray)[1]

        print(tray_blocks_sorted_list)
        print('\n')
        print(df_tray_count_per_block_sorted)



        # transform the dataframe into the standard template
        #loop thru per page
        block_row = 3 #starting for blocks
        wb_dst_row = 9 #starting row for the destination wb 
        page_increment = 48
        index_val = 0
        
        for val in tray_blocks_sorted_list:
            wb_dst_sht_tray.range('N' + str(block_row)).value = val

            curr_block_count = df_tray_count_per_block_sorted.loc[index_val,'counts']
            

            df_tray_per_block = df_tray.loc[(df_tray['BLOCK'] == val)]
            df_tray_per_block = df_tray_per_block.reset_index(drop=True)


            print('iterating to output excel file')
            # for count in curr_block_count:

            index_val_row = 0
            current_tray_no = ''
            previous_tray_no = ''
            while curr_block_count > index_val_row:
                
                #additional conditional statements for columns: NO, tray_TYPE, tray_WIDTH, tray_LENGTH
                if index_val_row > 0:
                    current_tray_no = df_tray_per_block.loc[index_val_row, 'NO']
                    # previous_tray_no = wb_dst_sht_tray.range('B' + str(wb_dst_row + index_val_row -1)).value
                    

                    # if previous_tray_no == df_tray_per_block.loc[index_val_row, 'NO']:
                    if previous_tray_no == current_tray_no:
                        wb_dst_sht_tray.range('B' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('C' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('D' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('E' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('F' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('G' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('H' + str(wb_dst_row + index_val_row)).value = ''
                        wb_dst_sht_tray.range('I' + str(wb_dst_row + index_val_row)).value = ''
                    else:
                        wb_dst_sht_tray.range('B' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'NO']
                        wb_dst_sht_tray.range('C' + str(wb_dst_row + index_val_row)).value = '1'
                        wb_dst_sht_tray.range('D' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_TYPE']
                        wb_dst_sht_tray.range('E' + str(wb_dst_row + index_val_row)).value = '-'
                        wb_dst_sht_tray.range('F' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_WIDTH']
                        wb_dst_sht_tray.range('G' + str(wb_dst_row + index_val_row)).value = '-'
                        wb_dst_sht_tray.range('H' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_LENGTH']
                        wb_dst_sht_tray.range('I' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'NO_OF_LUGS']
                    
                else:
                    wb_dst_sht_tray.range('B' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'NO']
                    wb_dst_sht_tray.range('C' + str(wb_dst_row + index_val_row)).value = '1'
                    wb_dst_sht_tray.range('D' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_TYPE']
                    wb_dst_sht_tray.range('E' + str(wb_dst_row + index_val_row)).value = '-'
                    wb_dst_sht_tray.range('F' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_WIDTH']
                    wb_dst_sht_tray.range('G' + str(wb_dst_row + index_val_row)).value = '-'
                    wb_dst_sht_tray.range('H' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'tray_LENGTH']
                    wb_dst_sht_tray.range('I' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'NO_OF_LUGS']


                #additional if statement incase tray has no support assigned
                # if df_tray_per_block.loc[index_val_row, 'SUPPORT_CODE'] == '' and df_tray_per_block.loc[index_val_row, 'SUPPORT_NO'] == '' and df_tray_per_block.loc[index_val_row, 'COUNT'] == '':
                if df_tray_per_block.loc[index_val_row, 'SUPPORT_CODE'] == '' or df_tray_per_block.loc[index_val_row, 'SUPPORT_CODE'] == None:
                    # wb_dst_sht_tray.range('I' + str(wb_dst_row + index_val_row)).value = '-'
                    wb_dst_sht_tray.range('J' + str(wb_dst_row + index_val_row)).value = '-'
                    wb_dst_sht_tray.range('K' + str(wb_dst_row + index_val_row)).value = '-'
                    wb_dst_sht_tray.range('L' + str(wb_dst_row + index_val_row)).value = '---'
                    wb_dst_sht_tray.range('M' + str(wb_dst_row + index_val_row)).value = '---'
                else:
                    wb_dst_sht_tray.range('J' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'COUNT']
                    wb_dst_sht_tray.range('K' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'bracket_TYPE']
                    wb_dst_sht_tray.range('L' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'bracket_WIDTH']
                    wb_dst_sht_tray.range('M' + str(wb_dst_row + index_val_row)).value = df_tray_per_block.loc[index_val_row, 'bracket_HEIGHT']


                if df_tray_per_block.loc[index_val_row, 'NO_OF_LUGS'] == '' or df_tray_per_block.loc[index_val_row, 'NO_OF_LUGS'] == None:
                    wb_dst_sht_tray.range('I' + str(wb_dst_row + index_val_row)).value = 'X'

    
                if df_tray_per_block.loc[index_val_row, 'AT_SITE'] == 'YES':
                    wb_dst_sht_tray.range('N' + str(wb_dst_row + index_val_row)).value = 'AT SITE'
                else:
                    wb_dst_sht_tray.range('N' + str(wb_dst_row + index_val_row)).value = ''
                
                wb_dst_sht_tray.range('O' + str(wb_dst_row + index_val_row)).value = str(df_tray_per_block.loc[index_val_row, 'SUPPORT_NO'])
                            
                # rows = rows + 1
                index_val_row = index_val_row + 1

                previous_tray_no = current_tray_no
                
        
            index_val = index_val + 1
            block_row = block_row + page_increment
            wb_dst_row = wb_dst_row + page_increment





    def transform_hanger_V2(self, df_hanger, wb_dst_sht_hanger):


        def insert_into_flatbar_section(hang_no, qty, hang_type, hang_width, length, leg_qty, height_a, height_b, remarks):
            
            wb_dst_sht_hanger.range('B' + str(wb_dst_row_left)).value = hang_no
            wb_dst_sht_hanger.range('C' + str(wb_dst_row_left)).value = qty
            wb_dst_sht_hanger.range('D' + str(wb_dst_row_left)).value = hang_type
            wb_dst_sht_hanger.range('E' + str(wb_dst_row_left)).value = hang_width
            wb_dst_sht_hanger.range('F' + str(wb_dst_row_left)).value = length
            wb_dst_sht_hanger.range('G' + str(wb_dst_row_left)).value = leg_qty
            wb_dst_sht_hanger.range('H' + str(wb_dst_row_left)).value = height_a
            wb_dst_sht_hanger.range('I' + str(wb_dst_row_left)).value = height_b
            wb_dst_sht_hanger.range('J' + str(wb_dst_row_left)).value = remarks


        def insert_into_anglebar_section(hang_no, qty, hang_type, hang_width, length, leg_qty, height_a, height_b, remarks):
            wb_dst_sht_hanger.range('L' + str(wb_dst_row_right)).value = hang_no
            wb_dst_sht_hanger.range('M' + str(wb_dst_row_right)).value = qty
            wb_dst_sht_hanger.range('N' + str(wb_dst_row_right)).value = hang_type
            wb_dst_sht_hanger.range('O' + str(wb_dst_row_right)).value = hang_width
            wb_dst_sht_hanger.range('P' + str(wb_dst_row_right)).value = length
            wb_dst_sht_hanger.range('Q' + str(wb_dst_row_right)).value = leg_qty
            wb_dst_sht_hanger.range('R' + str(wb_dst_row_right)).value = height_a
            wb_dst_sht_hanger.range('S' + str(wb_dst_row_right)).value = height_b
            wb_dst_sht_hanger.range('T' + str(wb_dst_row_right)).value = remarks


        

        print('\n')
        print('function: --transform_hanger--')

        
        # get unique tray blocks
        # hanger_blocks_sorted_list = self.get_unique_blocks_and_sort(df_hanger)[0]
        # df_hanger_count_per_block_sorted = self.get_unique_blocks_and_sort(df_hanger)[1]
        hanger_blocks_sorted_list = self.get_unique_blocks_and_sort_V2(df_hanger)[0]
        df_hanger_count_per_block_sorted = self.get_unique_blocks_and_sort_V2(df_hanger)[1]

        print(hanger_blocks_sorted_list)
        print('\n')
        print(df_hanger_count_per_block_sorted)



        #loop thru per page
        block_row = 3 #starting for blocks
        wb_dst_row_left = 10 #starting row for the destination wb
        wb_dst_row_right = 10 #starting row for the destination wb
        wb_dst_row = 10 #starting row for the destination wb

        page_increment = 57
        index_val = 0
        
        #paste blocks values to destination
        for val in hanger_blocks_sorted_list:
            wb_dst_sht_hanger.range('T' + str(block_row)).value = val

            #get counts of items per block

            curr_block_count = df_hanger_count_per_block_sorted.loc[index_val,'counts']
            

            df_hanger_per_block = df_hanger.loc[(df_hanger['BLOCK'] == val)]
            df_hanger_per_block = df_hanger_per_block.reset_index(drop=True)
            print(df_hanger_per_block)

   
            print('iterating to output excel file')
            # for count in curr_block_count:
            # rows = 1
            index_val_row = 0
            wb_dst_row_left = wb_dst_row
            wb_dst_row_right = wb_dst_row
            while curr_block_count > index_val_row:
                


                # GET THE VALUES FROM THE CURRENT ROW DATA
                hang_no = df_hanger_per_block.loc[index_val_row, 'NO']
                hang_qty = df_hanger_per_block.loc[index_val_row, 'COUNT']
                hang_type = df_hanger_per_block.loc[index_val_row, 'hang_TYPE']
                hang_width = int(df_hanger_per_block.loc[index_val_row, 'hang_WIDTH'])
                hang_length = df_hanger_per_block.loc[index_val_row, 'HANGER_LENGTH']
                hang_leg_qty = ''
                hang_height_a = int(df_hanger_per_block.loc[index_val_row, 'h_height_a'])
                hang_height_b = int(df_hanger_per_block.loc[index_val_row, 'h_height_b'])
                hang_remarks = df_hanger_per_block.loc[index_val_row, 'AT_SITE']


                # RECTIFY VALUES FOR REMARKS (AT SITE)
                if hang_remarks == 'YES':
                    hang_remarks = 'AT SITE'
                else:
                    hang_remarks = ''


                # GET THE MAX HEIGHT FROM BOTH LEGS
                hang_height = max(hang_height_a, hang_height_b)

                if hang_type in ['S1', 'S3']:
                    hang_length = '---' # for length
                    hang_leg_qty = '1' # for leg qty

                    if hang_height <= 400 and hang_width <= 600:
                        insert_into_flatbar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                        wb_dst_row_left += 1
                    else:
                        insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                        wb_dst_row_right += 1

                elif hang_type in ['S2', 'S4']:
                    hang_length = '---' # for length
                    hang_leg_qty = '1' # for leg qty
    
                    insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                    wb_dst_row_right += 1


                elif hang_type in ['H1', 'H3']:
                    # CHECK RUNNER BAR LENGTH
                    if int(hang_length) <= 1500:
                        hang_leg_qty = '2'
                    else:
                        hang_leg_qty = '3'
                    
                    if hang_height <= 400 and hang_width <= 600:
                        insert_into_flatbar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                        wb_dst_row_left += 1
                    else:
                        insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                        wb_dst_row_right += 1


                elif hang_type in ['H2', 'H4']:
                    # CHECK RUNNER BAR LENGTH
                    if int(hang_length) <= 1500:
                        hang_leg_qty = '2'
                    else:
                        hang_leg_qty = '3'
                    
                    insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                    wb_dst_row_right += 1

          
                elif hang_type in ['X1', 'X2']:
                    hang_length = '---' # for length
                    hang_leg_qty = '1' # for leg qty

                    insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                    wb_dst_row_right += 1


                elif hang_type in ['V1', 'V2']:
                    hang_leg_qty = '1' # for leg qty

                    insert_into_anglebar_section(hang_no, hang_qty, hang_type, hang_width, hang_length, hang_leg_qty, hang_height_a, hang_height_b, hang_remarks)
                    wb_dst_row_right += 1


                index_val_row += 1


            index_val += 1
            block_row = block_row + page_increment
            wb_dst_row = wb_dst_row + page_increment

            
    def assign_page(self, wb_dst_sht_tray, wb_dst_sht_hanger):
        
        print('------- assigning page ------------')
        # GET ALL BLOCK NAMES FROM TRAY AND HANGER SHEETS
        tray_blocks = {}
        hanger_blocks = {}
        page_ctr = 0

        print('------- assigning page ------------')
        # GET STARTING PAGE
        _settings = Setting()
        _settings_items = _settings.items
        page_start = int(_settings_items['page_start'])
        
        page_ctr = page_start

        # while True:
        #     page_start = textinput('Page', 'Please input the start page for Fab List (number only):')
        #     text, ok = QInputDialog.getText(title='123', label='qwe')
        #     print(text, ok)
        #     if page_start.isnumeric():
        #         break
        

        # page_ctr = page_start
                

        print('------- assigning page ------------')
        # loop for tray sheet
        row_tray_no = 3 # CELL REFERENCE
        _tray = str(wb_dst_sht_tray.range('N' + str(row_tray_no)).value)
        print('_tray', _tray)
        print(type(_tray))

        while _tray is not None:
            print('_tray', _tray, row_tray_no)
            content =  {}
            content['block'] = f'N{row_tray_no}'
            content['page'] = f'N{row_tray_no - 2}'
            content['dwg_no'] = f'M{row_tray_no - 2}'
            content['space'] = f'B{row_tray_no - 2}'
            tray_blocks[_tray] = content
            # CELL INCREMENTS
            row_tray_no += 48
            _tray = wb_dst_sht_tray.range('N' + str(row_tray_no)).value
            print(_tray is not None)
            # if _tray is None:
            #     break
        print(f'tray_blocks: {tray_blocks}')

        print('------- assigning page ------------')
        # loop for hanger sheet
        row_hanger_no = 3 # CELL REFERENCE
        _hanger = str(wb_dst_sht_hanger.range('T' + str(row_hanger_no)).value)
        print('_hanger', _hanger)
        while _hanger is not None:
            print('_hanger', _hanger, row_hanger_no)
            content =  {}
            content['block'] = f'T{row_hanger_no}'
            content['page'] = f'T{row_hanger_no - 2}'
            content['dwg_no'] = f'R{row_hanger_no - 2}'
            content['space'] = f'B{row_hanger_no - 2}'
            hanger_blocks[_hanger] = content
            # CELL INCREMENTS
            row_hanger_no += 57
            _hanger = wb_dst_sht_hanger.range('T' + str(row_hanger_no)).value
        print(f'hanger_blocks: {hanger_blocks}')
        
        print('------- assigning page ------------')
        # GET ALL THE BLOCKS FROM THE LOADED CSV FILE
        unique_blocks = self.x_unique_blocks
        wiring_space = self.x_space_loaded
        ship_no = self.x_ship_no

        if wiring_space == 'acc':
            str_ship_dwg_no = f'{ship_no}-430500W'
            space = 'ACCOMMODATION SPACE'
        elif wiring_space == 'er':
            str_ship_dwg_no = f'{ship_no}-430510W'
            space = 'ENGINE ROOM SPACE'
        elif wiring_space == 'stg':
            str_ship_dwg_no = f'{ship_no}-430520W'
            space = 'STEERING GEAR ROOM SPACE'
        elif wiring_space == 'bos':
            str_ship_dwg_no = f'{ship_no}-430520W'
            space = 'BOSUN STORE'
        else:
            pass

        print('------- assigning page ------------')

        # SORT THE BLOCKS ACCORDING TO STANDARD
        predef_blocks = _settings_items['blocks'][wiring_space]

        sorted_blocks = [x for x in predef_blocks if x in unique_blocks]

        for block in sorted_blocks:
            
            if block in tray_blocks.keys():
                # ASSIGN VALUES TO SAVED RANGE
                print(page_ctr)

                cell_page = tray_blocks[block]['page']
                cell_dwg_no = tray_blocks[block]['dwg_no']
                cell_space = tray_blocks[block]['space']

                wb_dst_sht_tray.range(cell_page).value = f'{page_ctr}'
                wb_dst_sht_tray.range(cell_dwg_no).value = str_ship_dwg_no
                wb_dst_sht_tray.range(cell_space).value = space

                page_ctr += 1

            if block in hanger_blocks.keys():
                # ASSIGN VALUES TO SAVED RANGE
                print(page_ctr)

                cell_page = hanger_blocks[block]['page']
                cell_dwg_no = hanger_blocks[block]['dwg_no']
                cell_space = hanger_blocks[block]['space']

                wb_dst_sht_hanger.range(cell_page).value = f'{page_ctr}'
                wb_dst_sht_hanger.range(cell_dwg_no).value = str_ship_dwg_no
                wb_dst_sht_hanger.range(cell_space).value = space

                page_ctr += 1

        # create text file from the output
        f = open("data/loaded_file_data.txt", "w")
        # print(df_tray_cleaned.head())
        print(ship_no, file=f)
        print(wiring_space, file=f)
        print(sorted_blocks, file=f)
        f.close()


# class Tray_Hanger_Page:

#     def __init__(self) -> None:
        
#         #initialize for tray page
#         tray_cell_block = 'N' #3
#         tray_increment = 48
#         tray

#     def tray_page(self):
#         pass

#     def hanger_page(self):
#         pass


        

        