from file_formatter import file_formatter


class absolute_loader(file_formatter):

    def __init__(self, file_name):
        super().__init__(file_name)
        self.memory = self.generate_memory()
        self.memory_plotter()
        # self.print_memory()
        self.print_memory_rows()

    def generate_memory(self, no_of_rows=10):
        memory = [['000000', '0', '1', '2', '3', '4', '5', '6', '7',
                   '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']]
        current_location = '000000'
        for i in range(1, no_of_rows):
            memory.append([current_location])
            current_location = self.zero_filler(
                str(int(current_location) + 10))
        return memory

    def memory_plotter(self):
        for T_record in self.get_T_records_with_data():
            address_location = T_record["starting_address"]
            content_location = address_location[len(address_location)-1]
            address_location = address_location[:len(address_location)-1] + "0"

            y_location = None
            x_location = None
            # Find the location in address column
            for i in range(1, len(self.memory)):
                if self.memory[i][0] == address_location:
                    y_location = i
                    break
            # Find the location in content row
            for j in range(1, len(self.memory[0])):
                if self.memory[0][j] == content_location:
                    x_location = j
                    break

            splitted_object_codes = self.split_object_codes(
                T_record["object_codes"])

            row_length = len(self.memory[0])-1
            counter = 0
            done = False
            for i in range(y_location, len(self.memory)):
                if done == True:
                    break
                for j in range(x_location, row_length+1):
                    if len(splitted_object_codes) == counter:
                        done = True
                        break
                    self.memory[i].insert(j, splitted_object_codes[counter])
                    counter += 1

    def split_object_codes(self, object_codes):
        splitted_object_codes = []
        for i in range(0, len(object_codes), 2):
            splitted_object_codes.append(object_codes[i] + object_codes[i+1])
        return splitted_object_codes

    def print_memory(self):

        for row in self.memory:
            for element in row:
                print(element, end=" ")
            print()

    def print_memory_rows(self):
        for row in self.memory:
            print(row)

    def zero_filler(self, value, desired_length=6):
        if "0x" in value:
            value = value[2:]
        zero_count = desired_length - len(value)
        for i in range(zero_count):
            value = "0" + value
        return value


if __name__ == "__main__":
    absolute_loader("PROG3.txt")
