
import pandas as pd
import xlwings as xw


class TrayBracket_Mat:
    def __init__(self):
    # def __init__(self, size, bkt_type, width, height, block):

        # self.size = size
        # self.type = bkt_type
        # self.width = width
        # self.height = height
        # self.block = block
        
        self.steel_type = '' # 30X30X5T or 40X40X5T

        
    def identify(self, df_supports): # identify if the bracket is angle bar or flat bar
        
        # _process_tray_support
        processed_tray_support = self._process_tray_support(df_supports)
        print('processed_tray_support', processed_tray_support)
        processed_tray_support.to_excel('data/_output_temp_mat_list/processed_tray_support.xlsx')

        support_with_material_assigned = self._assign_bracket_material(processed_tray_support)
        print('processed_tray_support', support_with_material_assigned)
        support_with_material_assigned.to_excel('data/_output_temp_mat_list/support_with_material_assigned.xlsx')
        

        return support_with_material_assigned

    def _process_tray_support(self, df_tray):
        df_support = df_tray[['BLOCK', 'bracket_TYPE', 'bracket_WIDTH', 'bracket_HEIGHT', 'COUNT']]
        df_support = df_support.dropna()
        print('df_support\n', df_support)

        # separate support legs
        df_support['bracket_a'] = df_support.apply(lambda x: self._separate_bracket_supports(x['bracket_HEIGHT'], 'leg_a'), axis=1)
        df_support['bracket_b'] = df_support.apply(lambda x: self._separate_bracket_supports(x['bracket_HEIGHT'], 'leg_b'), axis=1)
       
        print('df_support\n', df_support)
        return df_support

    def _separate_bracket_supports(self, bracket_height, leg_set):
        if '/' in str(bracket_height):
            a, b = bracket_height.split('/')
        else:
            a, b = bracket_height, bracket_height
        
        if leg_set == 'leg_a':
            return a
        else:
            return b

    def _assign_bracket_material(self, processed_support):
        processed_support.to_excel('data/_output_temp_mat_list/processed_supportx.xlsx')
        # get the material of the bracket
        processed_support['MATERIAL'] = processed_support.apply(lambda x: self._identify_material(x['bracket_TYPE'], 
                                                                                                  x['bracket_WIDTH'], 
                                                                                                  x['bracket_a'], 
                                                                                                  x['bracket_b']), axis=1)
        processed_support.to_excel('data/_output_temp_mat_list/processed_supporty.xlsx')
        # separate both legs support
        return self._transform(processed_support)


    def _identify_material(self, support_type, width, height_a, height_b):
        height = max(int(height_a), int(height_b))
        if support_type in ['E2', 'U2']:
            if width >= 500:
                return '40x40x5t'
            else:
                return '30x30x5t'
        else:
            if height <= 1000:
                return '30x30x5t'
            else:
                return '40x40x5t'
        
        

    def _transform(self, support_data):

        support_a = support_data[['BLOCK', 'bracket_TYPE', 'bracket_WIDTH', 'bracket_a', 'MATERIAL', 'COUNT']]
        support_a.columns = ['BLOCK', 'TYPE', 'WIDTH', 'LENGTH', 'MATERIAL', 'COUNT'] # rename headers
        print("suppport_a", support_a)

        support_b = support_data[['BLOCK', 'bracket_TYPE', 'bracket_WIDTH', 'bracket_b', 'MATERIAL', 'COUNT']]
        support_b.columns = ['BLOCK', 'TYPE', 'WIDTH', 'LENGTH', 'MATERIAL', 'COUNT'] # rename headers
        print("suppport_a", support_a)

        # merge dataframes
        supports = pd.concat([support_a, support_b], ignore_index=True)
        
        print("supports\n", supports)
        print("data types", supports.dtypes)
        # supports['LENGTH'] = support['LENGTH'].astype(int)
        supports.to_excel('data/_output_temp_mat_list/supports.xlsx')
        return supports

class Hanger_Mat:
    def __init__(self):
        pass

    def identify(self, df_hanger):
        print("df_hanger_raw", df_hanger)
        df_1 = df_hanger.copy()
        df_2 = df_hanger.copy()

        # identify type steel material for hanger leg
        support_processed = self._process_support(df_1)
        support_processed.to_excel('data/_output_temp_mat_list/hanger_leg_processed_support.xlsx')
        support_cleaned = self._extract_supports(support_processed)
        support_cleaned.to_excel('data/_output_temp_mat_list/hanger_support_cleaned.xlsx')

        # identify type steel material for runner bars
        runnerbar_processed = self._process_runnerbar(df_2)
        runnerbar_processed.to_excel('data/_output_temp_mat_list/runnerbar_processed.xlsx')

        # merge
        complete_hanger_material = self._combine(support_cleaned, runnerbar_processed)
        complete_hanger_material.to_excel('data/_output_temp_mat_list/complete_hanger_material.xlsx')

        return complete_hanger_material
       

    def _extract_supports(self, support):
        # create new dataframe with supports only
        # BLOCKNAME, HANGER_SIZE, h_height_a, h_height_b

        support_a = support[['BLOCK', 'HANGER_SIZE', 'h_height_a', 'MATERIAL', 'COUNT_RB']]
        support_a.columns = ['BLOCK', 'HANGER_SIZE', 'LENGTH', 'MATERIAL', 'COUNT_RB'] # rename headers
        print("suppport_a", support_a)

        support_b = support[['BLOCK', 'HANGER_SIZE', 'h_height_b', 'MATERIAL', 'COUNT_RB']]
        support_b.columns = ['BLOCK', 'HANGER_SIZE', 'LENGTH', 'MATERIAL', 'COUNT_RB'] # rename headers
        print("suppport_b", support_b)

        
        # merge dataframes
        supports = pd.concat([support_a, support_b], ignore_index=True)
        
        # rename columnheader
        supports.columns = ['BLOCK', 'HANGER_SIZE', 'LENGTH', 'MATERIAL', 'COUNT']


        print("supports", supports)
        print("data types", supports.dtypes)
        # supports['LENGTH'] = support['LENGTH'].astype(int)
        return supports


    def _process_support(self, df_support):
        supports_processed = df_support
        supports_processed['MATERIAL'] = supports_processed.apply(lambda x: self._assign_material(x['HANGER_SIZE'],
                                                                                                  x['hang_TYPE'],
                                                                                                  x['h_height_a'], 
                                                                                                  x['h_height_b']), axis=1)
        
        supports_processed['COUNT_RB'] = supports_processed.apply(lambda x: self._get_count(x['hang_TYPE'],
                                                                                         x['HANGER_LENGTH'],
                                                                                         x['COUNT']), axis=1)
        
        print('supports_processed', supports_processed)
        return supports_processed

    def _get_count(self, hang_type, hang_length, count):
        if hang_length != None:
            if int(hang_length) > 1500:
                return count + 1
            else:
                return count + 2
        else:
            return count


    def _assign_material(self, hang_width, hang_type, hanger_height_a, hanger_height_b):
        hang_width = int(hang_width[:3])
        hanger_height_a = int(hanger_height_a)
        hanger_height_b = int(hanger_height_b)
        hang_height = max(hanger_height_a, hanger_height_b)
        print(hang_width, hanger_height_a, hanger_height_b)

        material_type = ''

        # GET THE MAX HEIGHT FROM BOTH LEGS
        hang_height = max(hanger_height_a, hanger_height_b)

        if hang_type in ['S1', 'S3']:
            if hang_height < 400 and hang_width < 600:
                material_type = '32x4.5t' # flat bar
            else:
                material_type = '30x30x5t' # angle bar

        elif hang_type in ['S2', 'S4']:
            material_type = '30x30x5t' # angle bar

        elif hang_type in ['H1', 'H3']:
            # CHECK RUNNER BAR LENGTH
            if hang_height <= 400 and hang_width <= 600:
                material_type = '32x4.5t' # flat bar
            else:
                material_type = '30x30x5t' # angle bar

        elif hang_type in ['H2', 'H4']:
            # CHECK RUNNER BAR LENGTH
            material_type = '30x30x5t' # angle bar

        elif hang_type in ['X1', 'X2']:
            material_type = '30x30x5t' # angle bar

        elif hang_type in ['V1', 'V2']:
            material_type = '30x30x5t' # angle bar

        elif hang_width > 600 or hang_height >= 1000:
            material_type ="40x40x5t" # angle bar

        return material_type


    def _process_runnerbar(self, df_hanger):
        # hangers with runner bars: H1, H2, H3, H4
        with_runnerbars = df_hanger[(df_hanger['hang_TYPE']).isin(['H1', 'H2', 'H3', 'H4'])]
        with_runnerbars = with_runnerbars[['BLOCK', 'hang_TYPE', 'HANGER_LENGTH', 'COUNT']]
        with_runnerbars.to_excel('data/_output_temp_mat_list/with_runnerbars0.xlsx')

        # adjust hanger runnerbar length, +50mm
        with_runnerbars['HANGER_LENGTH'] = with_runnerbars['HANGER_LENGTH'].apply(lambda x: int(x) + 50)

        with_runnerbars['MATERIAL'] = '32x4.5t'

        with_runnerbars['COUNT_temp'] = with_runnerbars.apply(lambda x: self._count(x['hang_TYPE']), axis=1)
        with_runnerbars.to_excel('data/_output_temp_mat_list/with_runnerbars1.xlsx')

        # recompute runnerbar count
        with_runnerbars['COUNT_X'] = with_runnerbars['COUNT'].astype(int) * with_runnerbars['COUNT_temp'].astype(int)
        with_runnerbars.to_excel('data/_output_temp_mat_list/with_runnerbars2.xlsx')

        with_runnerbars = with_runnerbars[['BLOCK', 'hang_TYPE', 'HANGER_LENGTH', 'MATERIAL', 'COUNT_X']]
        with_runnerbars.columns = ['BLOCK', 'HANGER_TYPE', 'LENGTH', 'MATERIAL', 'COUNT'] # rename headers


        print('with_runnerbars', with_runnerbars)

        return with_runnerbars


    def _count(self, hanger_type):
        if hanger_type in ['H1', 'H3']:
            return 2
        elif hanger_type in ['H2', 'H4']:
            return 4
        else:
            return 0
    
    def _combine(self, hanger_support, hanger_runnerbar):
        combined = pd.concat([hanger_support, hanger_runnerbar], ignore_index=True)
        print('combined hanger support\n', combined)
        combined.to_excel('data/_output_temp_mat_list/combined.xlsx')
        return combined

    def _identify_steel_material(self):
        pass   


class ExcelMatList:

    def __init__(self):
        pass
    
    def aggregate_supports(self, df_support_tray, df_support_hanger):
        
        # retain needed columns
        df_tray_supp = df_support_tray[['BLOCK', 'MATERIAL', 'LENGTH', 'COUNT']]
        df_hanger_supp = df_support_hanger[['BLOCK', 'MATERIAL', 'LENGTH', 'COUNT']]

        # combine dataframes
        material_data = pd.concat([df_tray_supp, df_hanger_supp], ignore_index=True)
        material_data['COUNT'] = material_data['COUNT'].astype(int)
        material_data['LENGTH'] = material_data['LENGTH'].astype(int)
        print('combined material_data\n', material_data)

        material_data.to_excel('data/_output_temp_mat_list/material_data.xlsx')
        unik = material_data.nunique()
        print(unik)


        # transformed_data = self._transform_data(material_data)
        # transformed_data.to_excel('data/_output_temp_mat_list/transformed_data.xlsx')

        return material_data
    
    # def _load_data_to_template(self):
    #     print("_load_data_to_template function")
    #     mat_data = pd.read_excel('data/_output_temp_mat_list/material_data.xlsx')
    #     mat_data_1 = mat_data.drop(columns=['Unnamed: 0'], axis=1)
    #     print(mat_data_1)

    #     # get unique blocks
    #     _blocks = self._read_data_from_text_file()
    #     print(_blocks)

    
    def _get_unique_mat_sizes(self, df, material):
        dfx = df[df['MATERIAL']==material]
        print(dfx)
        print(dfx['LENGTH'].unique())
        mat_size = list(dfx['LENGTH'].unique())
        mat_size.sort(reverse=True)
        return mat_size


    def _count_material_length_per_block(self, df, material, material_length, block):
        dfy = df[(df['MATERIAL']==material) & (df['LENGTH']==material_length) & (df['BLOCK']==block)]
        print(dfy)
        mat_count = dfy['COUNT'].sum()
        print(mat_count)

        if mat_count == 0:
            return ''
        else:
            return mat_count

    # def _transform_data(self, data):
    #     transformed_data = pd.pivot_table(data, index=['MATERIAL', 'LENGTH'], columns=['BLOCK'], aggfunc=[np.sum]).sort_values(by=['MATERIAL', 'LENGTH'], ascending=False)
    #     transformed_data = transformed_data.reindex(self._get_blocks_from_range(), axis=1)
    #     transformed_data.swaplevel()
    #     print('transformed data\n', transformed_data)
    #     return transformed_data

    # def _get_blocks_from_range(self):
    #     # cell_row = 3 # along row 3
    #     # last_column = wb_dest.cells(cell_row, wb_dest.cells.last_cell.column).end('left').column
    #     # block_target_range = wb_dest.range((3,3),(3,last_column)).value # returns list from material list
    #     sorted_blocks = self._read_data_from_text_file()
    #     # sorted_blocks = self._sort_blocks_columns(block_target_range, all_blocks)
    #     return sorted_blocks

    def _read_data_from_text_file(self):
        f = open("data/loaded_file_data.txt", "r")
        ship = f.readline()
        space = f.readline()
        blocks = f.readline()
        f.close()

        blocks = blocks.replace('[', '')
        blocks = blocks.replace(']', '')
        blocks = blocks.replace("'", '')
        blox = blocks.split(',')

        new_blocks = []
        for block in blox:
            # print(block.strip())
            new_blocks.append(block.strip())

        return new_blocks
    
    def _sort_blocks_columns(self, list_of_blocks, extracted_blocks):
        sorted_blocks = [x for x in extracted_blocks if x in list_of_blocks]
        return sorted_blocks


class RawData:
    data_file_path = r'data/_output/temp_output_data.xlsx'

    def __init__(self) -> None:
        pass

    def get_dataframe(self):
        # READ DATA FROM EXCEL FILE
        
        # OPEN DATA
        with xw.App(visible=False) as app:
            raw_data = xw.Book(self.data_file_path, update_links=False) # OPEN EXCEL FILE

            sht_tray = raw_data.sheets['for_tray']
            sht_hanger = raw_data.sheets['for_hanger']

            df_raw_tray = sht_tray.range('A1').options(pd.DataFrame, header=1, index=False, expand='table').value 
            print(df_raw_tray.head())

            df_raw_hanger = sht_hanger.range('A1').options(pd.DataFrame, header=1, index=False, expand='table').value 
            print(df_raw_hanger.head())

            raw_data.close()

            return df_raw_tray, df_raw_hanger


class Material_List_Module:
    def __init__(self) -> None:
        pass

    def run_module(self):


# if __name__ == '__main__':
    
        # this script starts here
    
        file_mat_list = 'data/_output/MATLIST.xlsx'

        # GET RAW DATA
        RawDataX = RawData()
        df_raw_tray, df_raw_hanger = RawDataX.get_dataframe() # IN LIST TRAY, HANGER
        df_raw_tray.to_excel('data/_output_temp_mat_list/1_df_raw_tray.xlsx')
        df_raw_hanger.to_excel('data/_output_temp_mat_list/1_df_raw_hanger.xlsx')

        # PROCESS RAW DATA
        Hanger = Hanger_Mat()
        df_hanger_materials = Hanger.identify(df_raw_hanger)

        Tray = TrayBracket_Mat()
        df_tray_materials = Tray.identify(df_raw_tray)

        # PROCESS FOR STANDARD OUTPUT
        MatList = ExcelMatList()
        material_list_data = MatList.aggregate_supports(df_tray_materials, df_hanger_materials)
        
        # dfx = material_list_data.reset_index(level='LENGTH')
        # print(dfx.to_excel('dfx.xlsx'))

        # OPEN MATERIAL LIST EXCEL FILE
        with xw.App(visible=False) as app:

            wb_mat_list = xw.Book(file_mat_list, update_links=False) # OPEN EXCEL FILE
            
            # wb_mat_list_template = xw.Book('data/_output_temp_mat_list/transformed_data.xlsx', update_links=False) # OPEN EXCEL FILE
            wb_dest = wb_mat_list.sheets['Cway Support']

            # paste blocks, range: F7 -> Y7
            blocks = MatList._read_data_from_text_file()
            print(blocks)
            wb_dest.range('F7:Y7').value = blocks

            # paste 32x4.5t flatbars, range E9 -> E59
            sizes = MatList._get_unique_mat_sizes(material_list_data, '32x4.5t')
            print(sizes)
            row_val = 9
            for size in sizes:
                wb_dest.range('E' + str(row_val)).value = size
                wb_dest.range('C' + str(row_val)).value = '32 x 4.5t'

                # block_val = wb_dest.cells(7, 6).value # equivalent to RANGE(F7)
                col_val = 6
                while(wb_dest.cells(7, col_val).value != None): # equivalent to RANGE(F7)
                    print(wb_dest.cells(7, col_val).value)
                    mat_count = MatList._count_material_length_per_block(material_list_data, '32x4.5t', size, wb_dest.cells(7, col_val).value)
                    wb_dest.cells(row_val, col_val).value = mat_count
                    
                    col_val += 1
                    
                row_val += 1

            # paste 30x30x5t angle bars, range E60 -> E119
            sizes = MatList._get_unique_mat_sizes(material_list_data, '30x30x5t')
            print(sizes)
            row_val = 60
            for size in sizes:
                wb_dest.range('E' + str(row_val)).value = size
                wb_dest.range('C' + str(row_val)).value = '30 x 30 x 5t'

                col_val = 6
                while(wb_dest.cells(7, col_val).value != None): # equivalent to RANGE(F7)
                    mat_count = MatList._count_material_length_per_block(material_list_data, '30x30x5t', size, wb_dest.cells(7, col_val).value)
                    wb_dest.cells(row_val, col_val).value = mat_count
                    
                    col_val += 1
                    
                row_val += 1

            # paste 40x40x5t angle bars, range E121 -> E135
            sizes = MatList._get_unique_mat_sizes(material_list_data, '40x40x5t')
            print(sizes)
            row_val = 121
            for size in sizes:
                wb_dest.range('E' + str(row_val)).value = size
                wb_dest.range('C' + str(row_val)).value = '40 x 40 x 5t'

                col_val = 6
                while(wb_dest.cells(7, col_val).value != None): # equivalent to RANGE(F7)
                    mat_count = MatList._count_material_length_per_block(material_list_data, '40x40x5t', size, wb_dest.cells(7, col_val).value)
                    wb_dest.cells(row_val, col_val).value = mat_count
                    
                    col_val += 1

                row_val += 1

            wb_mat_list.save(file_mat_list)
            wb_mat_list.close()
