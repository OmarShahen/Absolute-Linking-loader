from file_formatter import file_formatter


class files_reader:

    def __init__(self, files_list):
        self.files_list = files_list
        self.fetched_files = []
        self.fetched_files = self.fetch_files()

    def fetch_files(self):
        fetched_files = []
        for i in range(len(self.files_list)):
            fetched_files.append(file_formatter(
                self.files_list[i] + '.txt').return_file_content())
        return fetched_files

    def return_fetched_files(self):
        return self.fetched_files


if __name__ == "__main__":
    files_reader(['PROG2', 'PROG3', 'PROG1'])
