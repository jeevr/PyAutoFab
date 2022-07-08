
# from modules.transform import transform_data
from modules.transform.transform_data import RawData, Checker
from modules.file_manager.manage import FileManager

# from modules.transform.transform_data import *


class THFLProcess():
    def __init__(self):
        
        self._verified_input_file_path = 'data/_verification_data/input_file_data.txt'
        self.ship = ''
        self.space = ''
        self.input_raw_file_path = ''
        self.checker_return_errors = []

        self._get_ship_details() # get the dropped file details from text file

    def _get_ship_details(self):
        _file = open(self._verified_input_file_path, 'r')
        self.input_raw_file_path = (_file.readline()).strip()
        self.ship = (_file.readline()).strip()
        self.space = (_file.readline()).strip()
        _file.close()
        
    def execute_process(self):
        self._copy_raw_data() # copy raw data into output folder in advance
        
        self._load_and_transform() # load and transform raw data


        print('thfl process executed')

    def _copy_raw_data(self):
        manage = FileManager()
        manage.copy_raw_input_data(self.input_raw_file_path)

    def _load_and_transform(self):
        self.input_raw_file_path = 'data/_raw_data_input_copy/SC405_CW_ER.txt'
        raw = RawData(self.input_raw_file_path)
        print(raw.df_raw_tray)
        print(raw.df_raw_hanger)

        raw.df_raw_tray.to_excel('df_raw_tray.xlsx')
        raw.df_raw_hanger.to_excel('df_raw_hanger.xlsx')

        self._apply_checker(raw.df_raw_tray)

    def _apply_checker(self, df_tray):
        # apply checker
        checker = Checker()

        # check for rows with null values
        df_tray_with_nulls = checker.check_rows_with_nulls(df_tray)
        if len(df_tray_with_nulls) > 0:
            self.checker_return_errors.append('TRAY WITHH NULLS')
            df_tray_with_nulls.to_excel('df_tray_with_nulls.xlsx')
        
        df_tray_checked = checker.check_tray(df_tray)
        df_tray_checked.to_excel('df_tray_checked.xlsx')


# if __name__ == '__main__': # this code will not be executed when called from other script as a class object
    
#     process = THFLProcess()
#     print(process.input_raw_file_path)
#     print(process.ship)
#     print(process.space)