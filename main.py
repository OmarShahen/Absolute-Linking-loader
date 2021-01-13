
from absolute_loader import absolute_loader
from tabulate import tabulate


def main():
    files = input("Enter The Linked Files In The Desired Sequence: ")
    returned_memory = None
    all_objects = []
    object_record = {}
    files_list = files.split('+')
    for i in range(len(files_list)):
        if i == 0:
            object_record["file_name"] = files_list[i]
            file_obj = absolute_loader(files_list[i] + '.txt')
            object_record["memory"] = file_obj.return_memory()
            returned_memory = file_obj.return_memory()
            all_objects.append(object_record)
            object_record = {}
        else:
            object_record["file_name"] = files_list[i]
            file_obj = absolute_loader(files_list[i] + '.txt', returned_memory)
            object_record["memory"] = file_obj.return_memory()
            returned_memory = file_obj.return_memory()
            all_objects.append(object_record)
            object_record = {}

    while True:
        for i in range(len(all_objects)):
            print(i+1, '. ', all_objects[i]["file_name"])
        print(len(all_objects)+1, '. Final Result')
        choice = int(input("Select Option: "))
        if choice == 4:
            file_obj.print_memory_rows()
        else:
            show_output(choice, all_objects[choice-1])


def show_output(choice, object_record):
    print(object_record["file_name"])
    print(tabulate(absolute_loader(
        object_record["file_name"] + '.txt').return_memory(), headers="firstrow"))


if __name__ == "__main__":
    main()
