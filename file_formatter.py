
class file_formatter:

    def __init__(self, file_name):
        self.file = open("programs/" + file_name, "r")
        self.HTME_headers = ['H', 'D', 'R', 'T', 'M', 'E']
        self.file_dict = self.divide_HTME_record()
        self.get_H_record()
        self.PROG_name = self.extract_PROG_name()

    def divide_HTME_record(self):
        file_lines = []
        file_dict = {}

        counter = 0
        for line in self.file:
            if line[0] not in self.HTME_headers:
                file_lines[counter-1] += line
            else:
                file_lines.append(line)
            counter += 1

        T_counter = 1
        M_counter = 1

        for i in range(len(file_lines)):
            if file_lines[i][0] == 'T':
                file_dict[file_lines[i][0] +
                          str(T_counter)] = self.remove_new_line(file_lines[i])
                T_counter += 1
            elif file_lines[i][0] == 'M':
                file_dict[file_lines[i][0] +
                          str(M_counter)] = self.remove_new_line(file_lines[i])
                M_counter += 1
            else:
                file_dict[file_lines[i][0]] = self.remove_new_line(
                    file_lines[i])

        return file_dict

    def get_H_record(self):
        return self.file_dict["H"]

    def remove_new_line(self, text):
        text = text.split("\n")
        clean_text = ""
        for i in text:
            clean_text += i
        return clean_text

    def extract_PROG_name(self):
        return self.file_dict["H"].split(".")[1]

    def get_PROG_name(self):
        return self.PROG_name


if __name__ == "__main__":
    file_formatter("PROG2.txt")
