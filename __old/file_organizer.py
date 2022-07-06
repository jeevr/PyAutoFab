import time
import os
import shutil
import pathlib


class Template_data:

    def __init__(self):
        self.template_file_path = 'data/_template/THFL.xls'
        self.destination_path = 'data/_output/THFL.xls'

        self.material_list_path = 'data/_template/MATLIST.xlsx'
        self.matlist_dest_path = 'data/_output/MATLIST.xlsx'

        self.input_path = 'data/_csv_input'
        self.output_path = 'data/_output'


    def copy_template_file(self):
        print('\n')
        print('function:    --copy_template_file--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --copy_template_file--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################


        #check if there is existing template file in the output folder
        self.check_template_file_at_destination_path = pathlib.Path(self.destination_path)

        if self.check_template_file_at_destination_path.exists():
            print('file exists')

            #delete file
            os.remove(self.destination_path)
            os.remove(self.matlist_dest_path)

            #wait for the file to be deleted
            time.sleep(1)

            #check again if the file is already deleted
            if self.check_template_file_at_destination_path.exists():
                while self.check_template_file_at_destination_path.exists():
                    print('deleting file')
                    time.sleep(1)

                    if self.check_template_file_at_destination_path.exists():
                        print('file deleted... at while loop')
                        break
            else:
                print('file already deleted')
                pass
        else:
            print('no file yet exists')


        #check if template file exist on source folder
        self.check_template_file = pathlib.Path(self.template_file_path)

        if self.check_template_file.exists():

            #copy file
            shutil.copy(self.template_file_path, self.destination_path)
            shutil.copy(self.material_list_path, self.matlist_dest_path)


            #wait for a while
            time.sleep(1)

            #check if the file is already copied to the destination path
            while not self.check_template_file_at_destination_path.exists():
                print('copying file...')
                time.sleep(1)

                if self.check_template_file_at_destination_path.exists():
                    print('file copied... at while loop')
                    break
            
            print('file copied')

        else:
            print('template file does not exists')
            
            time.sleep(2)
            
            #exit the program, or inform the user
            print('program exiting...')
            exit()


    





class OutputResource:

    def __init__(self, csv_input_file):
        
        self.csv_input_file = csv_input_file
        self.csv_input_file_name = self.csv_input_file.split('/')[-1]

        self.output_folder_name = 'THFL_Output'
        self.complete_folder_path = ''

        self.input_path = 'data/_csv_input/'
        self.output_path = 'data/_output/'


        #get the parent folder path
        self.csv_input_parent_path = self.csv_input_file.split('/')
        #remove the last item from the list
        self.csv_input_parent_path.pop()
        #re-construct the parent folder path
        my_separator = '\\'
        self.csv_input_parent_path = my_separator.join(self.csv_input_parent_path)
        
        print(f'csv_input_parent_path::: {self.csv_input_parent_path}')


    def create_output_folder(self):
        print('\n')
        print('function:    --create_output_folder--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --create_output_folder--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################



        #get time stamp
        curr_time = self.get_current_timestamp()
        folder_name = self.output_folder_name

        #create the complete path
        self.complete_folder_path = str(self.csv_input_parent_path) + "\\[" + str(folder_name) + ']_' + str(curr_time)

        print(f'comple_folder_path is: {self.complete_folder_path}')


        #create the folder
        os.makedirs(self.complete_folder_path)


    def get_current_timestamp(self):
        print('\n')
        print('function:    --get_current_timestamp--')


        #get time stamp to create suffix for folder
        #sample: THFL_Output_[Nov-12-2022 09.44]
        # dateTimeObj = datetime.now()
        secondsSinceEpoch = time.time()
        timeObj = time.localtime(secondsSinceEpoch)
        # print('Current TimeStamp is : %d-%d-%d %d:%d:%d' % (timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))

        suffix_name_timestamp = '%d-%d-%d_%d.%d.%d' % (timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)
        print(suffix_name_timestamp)

        return suffix_name_timestamp
        
        
    def copy_resources(self):
        print('\n')
        print('function:    --copy_resources--')


        # CREATE/OPEN TEXT FILE FOR LOGGER
        ###########################################################################
        f = open("data/_output_temp_data/process_logger.txt", "a")
        print('****************************************************', file=f)
        print('MAIN FUNCTION: --copy_resources--', file=f)
        print('****************************************************', file=f)
        f.close()
        ###########################################################################


        #copy the input file
        shutil.copy(self.csv_input_file, str(self.complete_folder_path + '/'))


        # fetch all files
        # ref link: https://pynative.com/python-copy-files-and-directories/
        for file_name in os.listdir(self.output_path):
            # construct full file path
            source = self.output_path + file_name
            destination = str(self.complete_folder_path + '/') + file_name
            # copy only files
            if os.path.isfile(source):
                shutil.copy(source, destination)
                print('copied', file_name)

        
    def copy_filedropped_to_input_folder(self):
        print('\n')
        print('function:    --copy_filedropped_to_input_folder--')

        
        #copy the input file
        shutil.copy(self.csv_input_file, str(self.input_path + self.csv_input_file_name))

