from file_formatter import file_formatter
from tabulate import tabulate


class absolute_loader(file_formatter):

    def __init__(self, file_name, memory_given=None):
        super().__init__(file_name)
        if memory_given == None:
            self.memory = self.generate_memory()
            self.memory = self.memory_plotter(self.memory)
        else:
            self.memory = self.memory_plotter(memory_given)

    def generate_memory(self, no_of_rows=22):
        memory = [['000000', '0', '1', '2', '3', '4', '5', '6', '7',
                   '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']]
        current_location = '000000'
        nulls = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null',
                 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        for i in range(1, no_of_rows):
            memory.append([current_location] + nulls)
            current_location = self.zero_filler(
                hex(int(current_location, 16) + 16))

        return memory

    def give_memory(starting_address, no_of_rows=80):
        memory = [['000000', '0', '1', '2', '3', '4', '5', '6', '7',
                   '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']]
        current_location = public_zero_filler(starting_address)
        nulls = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null',
                 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        for i in range(1, no_of_rows):
            memory.append([current_location] + nulls)
            current_location = public_zero_filler(
                hex((int(current_location, 16) + 16)))
        return memory

    def return_memory(self):
        return self.memory

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
        return memory

    def split_object_codes(self, object_codes):
        splitted_object_codes = []
        for i in range(0, len(object_codes), 2):
            splitted_object_codes.append(object_codes[i] + object_codes[i+1])
        return splitted_object_codes

    def print_memory_rows(self):
        print(tabulate(self.memory, headers="firstrow"))

    def zero_filler(self, value, desired_length=6):
        if "0x" in value:
            value = value[2:]
        zero_count = desired_length - len(value)
        for i in range(zero_count):
            value = "0" + value
        return value


def public_zero_filler(value, desired_length=6):
    if "0x" in value:
        value = value[2:]
    zero_count = desired_length - len(value)
    for i in range(zero_count):
        value = "0" + value
    return value


if __name__ == "__main__":
    absolute_loader("PROG3.txt")
