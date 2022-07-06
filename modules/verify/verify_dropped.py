

class DroppedFile:
    def __init__(self, file_path):
        self.file_path = file_path[0]
        self.file_name = ''
        self.file_ext = ''
        self.is_valid = True
        self.ship = ''
        self.space = ''
        self.returned_error = []

        try:
            self._get_details()
            self._check_validity()
            self._dump_to_file()
        except:
            self.returned_error.append('INVALID FILE FORMAT')

    def _get_details(self):
        print(self.file_path)
        file_name = (self.file_path).split('/')[-1] # sample return: SC407_CW_ER.txt
        self.file_name = file_name.split('.')[0].upper() # sample return: SC407_CW_ER
        self.file_ext = file_name.split('.')[1].upper() # sample return: txt

        self.ship = (self.file_name).split('_')[0] # sample return: [SC407, CW, ER] - > SC407
        self.space = (self.file_name).split('_')[2] # sample return: [SC407, CW, ER] - > ER

    def _check_validity(self):

        if self.file_ext != 'TXT':
            (self.returned_error).append('INVALID FILE TYPE')
    
        if (self.ship).find('SC') == -1:
            (self.returned_error).append('INVALID FILE NAME')

        if self.space not in ['ER', 'ACC', 'BOSN', 'STG']:
            (self.returned_error).append('INVALID CW SPACE')

    def _dump_to_file(self):
        _file = open('data/_verification_data/input_file_data.txt', 'w')
        print(self.ship, file=_file)
        print(self.space, file=_file)
        _file.close()