from files_reader import files_reader
from tabulate import tabulate
from absolute_loader import absolute_loader


class linkage_loader(files_reader):

    def __init__(self, files_list, starting_address):
        super().__init__(files_list)
        self.external_references = {}
        self.starting_address = starting_address
        self.create_symbol_table()
        self.memory = absolute_loader.give_memory(
            str(self.starting_address))
        self.memory_plotted = self.memory_plotter(self.memory)
        self.modify_memory()

    def get_T_records_with_data(self):
        all_records = []
        T_record = {}
        for file in self.fetched_files:
            for key in file:
                if "T" in key and len(key) == 2:
                    T_data = file[key].split(".")
                    T_record["number"] = key
                    T_record["starting_address"] = self.add_hexas(
                        T_data[1], file['starting_address'])
                    T_record["size"] = T_data[2]
                    T_record["object_codes"] = T_data[3]
                    all_records.append(T_record)
                    T_record = {}
        return all_records

    def print_linkage_loader_table(self):
        print(tabulate(self.memory, headers="firstrow"))

    def modify_memory(self):
        for i in range(len(self.fetched_files)):
            for key in self.fetched_files[i]:
                if 'M' in key and len(key) == 2:
                    splitted_M = self.fetched_files[i][key].split(".")
                    reference_location = self.add_hexas(
                        splitted_M[1], self.fetched_files[i]['starting_address'])
                    indexs = self.get_index(reference_location)
                    returned_elements = self.get_elements_from_memory(
                        indexs[0], indexs[1])
                    length_of_elements_to_add = None
                    outer_reference = None
                    operation_nature = None
                    if '+' in splitted_M[2]:
                        length_of_elements_to_add = splitted_M[2].split('+')[0]
                        outer_reference = splitted_M[2].split('+')[1]
                        operation_nature = '+'
                    elif '-' in splitted_M[2]:
                        length_of_elements_to_add = splitted_M[2].split('-')[0]
                        outer_reference = splitted_M[2].split('-')[1]
                        operation_nature = '-'
                    self.extract_other_references(
                        self.fetched_files[i]['starting_address'])

                    old_values = ''
                    new_values = ''
                    for element in returned_elements:
                        old_values += element

                    if operation_nature == '+':
                        new_values = self.add_hexas(
                            self.external_references[outer_reference], old_values[-int(length_of_elements_to_add):], int(length_of_elements_to_add))
                    elif operation_nature == '-':
                        new_values = self.subtract_hexas(self.external_references[outer_reference], old_values[-int(
                            length_of_elements_to_add):], int(length_of_elements_to_add))

                        new_values = self.zero_filler(
                            self.remove_X(new_values))
                    if int(length_of_elements_to_add) == 5:
                        new_values = old_values[0] + new_values
                        self.return_elements_to_memory(
                            indexs[0], indexs[1], new_values)
                    self.return_elements_to_memory(
                        indexs[0], indexs[1], new_values)

    def get_index(self, value):
        row_name = value[:len(value)-1] + '0'
        column_name = value[len(value)-1]

        all_positions = []

        index_i = None
        index_j = None

        for i in range(len(self.memory)):
            if self.memory[i][0] == row_name:
                index_i = i
                break
        for j in range(len(self.memory[0])):
            if self.memory[0][j] == column_name.upper():
                index_j = j
                break
        return index_i, index_j

    def get_elements_from_memory(self, index_i, index_j):
        if index_j == 15:
            return self.memory[index_i][index_j], self.memory[index_i][index_j+1], self.memory[index_i+1][1]
        elif index_j == 16:
            return self.memory[index_i][index_j], self.memory[index_i+1][1], self.memory[index_i+1][2]
        else:
            return self.memory[index_i][index_j], self.memory[index_i][index_j+1], self.memory[index_i][index_j+2]

    def return_elements_to_memory(self, index_i, index_j, value):
        if index_j == 15:
            self.memory[index_i][index_j] = value[:2]
            self.memory[index_i][index_j+1] = value[2:4]
            self.memory[index_i+1][1] = value[4:]
        elif index_j == 16:
            self.memory[index_i][index_j] = value[:2]
            self.memory[index_i+1][1] = value[2:4]
            self.memory[index_i+1][2] = value[4:]
        else:
            self.memory[index_i][index_j] = value[:2]
            self.memory[index_i][index_j+1] = value[2:4]
            self.memory[index_i][index_j+2] = value[4:]

    def memory_plotter(self, memory):
        for T_record in self.get_T_records_with_data():
            address_location = T_record["starting_address"]
            content_location = address_location[len(address_location)-1]
            address_location = address_location[:len(address_location)-1] + "0"

            y_location = None
            x_location = None
            # Find the location in address column
            for i in range(1, len(memory)):
                if memory[i][0] == address_location:
                    y_location = i
                    break
            # Find the location in content row
            for j in range(1, len(memory[0])):
                if memory[0][j] == content_location:
                    x_location = j
                    break

            splitted_object_codes = self.split_object_codes(
                T_record["object_codes"])

            row_length = len(memory[0])-1
            counter = 0
            done = False

            for i in range(y_location, len(memory)):
                if done == True:
                    break
                for j in range(x_location, row_length+1):
                    if len(splitted_object_codes) == counter:
                        done = True
                        break
                    memory[i][j] = splitted_object_codes[counter]
                    counter += 1
                x_location = 1
        return memory

    def split_object_codes(self, object_codes):
        splitted_object_codes = []
        for i in range(0, len(object_codes), 2):
            splitted_object_codes.append(object_codes[i] + object_codes[i+1])
        return splitted_object_codes

    def create_symbol_table(self):
        for i in range(len(self.fetched_files)):
            if i == 0:
                self.fetched_files[i]['starting_address'] = self.add_hexas(
                    self.fetched_files[i]['starting_address'], str(self.starting_address))
                self.extract_external_refernces(
                    self.fetched_files[i]['D'], self.fetched_files[i]['starting_address'])
            else:
                self.fetched_files[i]['starting_address'] = self.add_hexas(
                    self.fetched_files[i-1]['starting_address'], self.fetched_files[i-1]['prog_size'])

                self.extract_external_refernces(
                    self.fetched_files[i]['D'], self.fetched_files[i]['starting_address'])

    def extract_external_refernces(self, D_record, starting_address):
        splitted_record = D_record.split('.')
        for i in range(len(splitted_record)):
            if i % 2 != 0:
                self.external_references[self.remove_X(splitted_record[i])] = self.add_hexas(
                    splitted_record[i+1], str(starting_address))

        for i in range(len(self.fetched_files)):
            if self.fetched_files[i]['prog_name']:
                self.external_references[self.remove_X(self.fetched_files[i]['prog_name'])
                                         ] = self.fetched_files[i]['starting_address']

    def extract_other_references(self, starting_address):
        for file in self.fetched_files:
            splitted_R = file['R'].split('.')
            for i in range(len(splitted_R)):
                if self.check_number_existance(splitted_R[i]) == True:
                    reference_key = self.remove_X(splitted_R[i])
                    num_reference = splitted_R[i].split('X')[0]

                    external_references_keys = []
                    for key in self.external_references:
                        external_references_keys.append(key)
                    self.external_references[num_reference] = self.external_references[reference_key]
        self.external_references['01'] = starting_address

    def check_number_existance(self, word):
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for num in nums:
            if num in word:
                return True
        return False

    def print_external_symbol(self):
        external_symbol_table = []
        external_symbol_table.append(
            ['Control Section Name', 'Address', 'Length'])
        for i in range(len(self.fetched_files)):
            external_symbol_table.append([
                self.fetched_files[i]['prog_name'], self.fetched_files[i]['starting_address'], self.fetched_files[i]['prog_size']])
        print(tabulate(external_symbol_table, headers='firstrow'))
        print()
        for key in self.external_references:
            print(key, ' --> ', self.external_references[key])

    def remove_X(self, name):
        name = name.upper()
        splitted_name = name.split('X')
        if splitted_name[len(splitted_name)-1] == '':
            return splitted_name[len(splitted_name)-2] + 'X'
        return splitted_name[len(splitted_name)-1]

    def add_hexas(self, hex1, hex2, hexa_output_length=6):
        return self.zero_filler(hex(int(hex1, 16) + int(hex2, 16))[2:], hexa_output_length)

    def subtract_hexas(self, hex1, hex2, hexa_output_length=6):
        return self.zero_filler(hex(int(hex1, 16) - int(hex2, 16))[2:], hexa_output_length)

    def zero_filler(self, value, desired_length=6):
        if "0x" in value:
            value = value[2:]
        zero_count = desired_length - len(value)
        for i in range(zero_count):
            value = "0" + value
        return value


if __name__ == "__main__":
    linkage_loader(['PROG2', 'PROG3', 'PROG1'], 3020)
