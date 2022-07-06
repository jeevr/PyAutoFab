import os
import shutil
import time

class FileManager:
    def __init__(self) -> None:
        self.output_folder_name = '_thfl_output_files'

    def copy_raw_input_data(self, raw_input_original_file_path):
        file_name = raw_input_original_file_path.split('/')[-1]
        shutil.copyfile(raw_input_original_file_path, os.path.join(self._get_current_app_parent_directory(), 'data', self.output_folder_name, file_name))
        time.sleep(0.2)

    def _clear_files_in_output_folder(self): 
        app_parent_dir = self._get_current_app_parent_directory() # sample: D:\jeevr_apps\PyAutoFab
        output_folder_path = os.path.join(app_parent_dir, 'data', self.output_folder_name)
        print(output_folder_path)
        for f in os.listdir(output_folder_path):
            os.remove(os.path.join(output_folder_path, f))

    def _get_current_app_parent_directory(self):
        return os.getcwd()


# if __name__ == '__main__':
#     fm = FileManager()
#     print(fm._clear_files_in_output_folder())
    