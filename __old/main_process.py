from tray_hanger_raw import Tray, Hanger, CreateExcelOutput
from file_organizer import Template_data
from transform_raw_to_format import RawToExcelStandardFormat
from file_organizer import OutputResource
from material_list import *

import pymsgbox as pymsgbox

# modules for tracing errors and printingit
import traceback
import sys



class main():
    def __init__(self, csv_input_file):
        
        self.csv_input_file = csv_input_file
        self.csv_input_file_name = csv_input_file.split('/')[-1]
        
        self.output_folder_path = ''

        self.is_error = False
        

    def run_main_process(self):


        
        #input file for both tray and hanger
        input_file_name = self.csv_input_file_name



        ###################################################
        #create an object of class Tray
        # tray = Tray(input_file_name)

        # #get tray dataframe
        # df_tray = tray.get_tray_dataframe()

        # #create an object of class Hanger
        # hanger = Hanger(input_file_name)

        # #get the dataframe from hanger
        # df_hanger = hanger.get_hanger_dataframe()

        # #create the output object
        # output_to_excel = CreateExcelOutput('temp_output_data')

        # #output the tray and hanger in a single excel file
        # output_to_excel.output_to_excel_in_one_file([df_tray, df_hanger], ['for_tray', 'for_hanger'])


        # #copy template file to output folder
        # file_temp_copy = Template_data()
        # file_temp_copy.copy_template_file()

        # #transform raw output to standard template
        # transform_raw = RawToExcelStandardFormat()
        # transform_raw.transform_raw_to_standard(df_tray, df_hanger)

        # #create output folder for the related files

        # output_file = OutputResource(self.csv_input_file)

        # output_file.create_output_folder()
        # self.output_folder_path = output_file.complete_folder_path

        # output_file.copy_resources()

        if self.is_error == False:

            try:
                #create an object of class Tray
                tray = Tray(input_file_name)

                #get tray dataframe
                df_tray = tray.get_tray_dataframe()
            except Exception as e:
                pymsgbox.alert(text='There is an error [TRAY PROCESS].', title='ERROR!!!', button='OK')

                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True


        if self.is_error == False:
            try:
                #create an object of class Hanger
                hanger = Hanger(input_file_name)

                #get the dataframe from hanger
                df_hanger = hanger.get_hanger_dataframe()
            except:
                pymsgbox.alert(text='There is an error [HANGER PROCESS].', title='ERROR!!!', button='OK')

                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True


        if self.is_error == False:
            try:
                #create the output object
                output_to_excel = CreateExcelOutput('temp_output_data')

                #output the tray and hanger in a single excel file
                output_to_excel.output_to_excel_in_one_file([df_tray, df_hanger], ['for_tray', 'for_hanger'])
            except:
                pymsgbox.alert(text='There is an error [CREATING EXCEL OUTPUT FOR TEMP DATA].', title='ERROR!!!', button='OK')

                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True




        if self.is_error == False:
            try:
                #copy template file to output folder
                file_temp_copy = Template_data()
                file_temp_copy.copy_template_file()

            except:
                    pymsgbox.alert(text='There is an error [SETTING-UP TEMPLATE EXCEL FILE].', title='ERROR!!!', button='OK')
                    
                    print("---> printing Error <---")
                    print(traceback.format_exc())
                    print(e)

                    self.is_error = True


        if self.is_error == False:
            try:
        
                #transform raw output to standard template
                transform_raw = RawToExcelStandardFormat()
                transform_raw.transform_raw_to_standard(df_tray, df_hanger)

            except:
                pymsgbox.alert(text='There is an error [TRANSFORMING DATA INTO STANDARD FORMAT].', title='ERROR!!!', button='OK')
                
                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True


        # CREATE A MATERIAL LIST
        if self.is_error == False:
            try:
                
                mat_list = Material_List_Module()
                mat_list.run_module()

            except:
                pymsgbox.alert(text='There is an error [CREATING MATERIAL LIST].', title='ERROR!!!', button='OK')
                
                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True





        if self.is_error == False:
            try:

                #create output folder for the related files
                output_file = OutputResource(self.csv_input_file)

                output_file.create_output_folder()
                self.output_folder_path = output_file.complete_folder_path
        
                output_file.copy_resources()
            except:
                pymsgbox.alert(text='There is an error [COMPILING OUTPUT DATA].', title='ERROR!!!', button='OK')
                
                print("---> printing Error <---")
                print(traceback.format_exc())
                print(e)

                self.is_error = True



# if __name__ == '__main__':

#     app_run = main(r'D:/jeevr_apps/cway_thfl_automation - new/data/_csv_input/SC405_CW_ACC.txt')
#     app_run.run_main_process()