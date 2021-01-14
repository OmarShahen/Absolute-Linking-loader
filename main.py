
from absolute_loader import absolute_loader
from tabulate import tabulate
from linkage_loader import linkage_loader


def main():
    files = input("Enter The Linked Files In The Desired Sequence: ")
    files_list = files.split('+')
    while True:
        operations_shower(files_list)


def show_output(choice, object_record):
    print(object_record["file_name"])
    print(tabulate(absolute_loader(
        object_record["file_name"] + '.txt').return_memory(), headers="firstrow"))


def operations_shower(files_list):
    print("1. Absolute Loader.")
    print("2. Linkage Loader.")
    choice = int(input("Choose Option: "))
    if choice == 1:
        show_absolute_loader(files_list)
    elif choice == 2:
        show_linkage_loader(files_list)


def show_linkage_loader(files_list):
    starting_address = int(input("Enter The Starting Address: "))
    linkage_loader_obj = linkage_loader(files_list, starting_address)
    linkage_loader_obj.print_external_symbol()
    linkage_loader_obj.print_linkage_loader_table()


def show_absolute_loader(files_list):

    returned_memory = None
    all_objects = []
    object_record = {}
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
        print(len(all_objects)+2, '. Finished')
        choice = int(input("Select Option: "))
        if choice == len(all_objects)+1:
            file_obj.print_memory_rows()
        elif choice == len(all_objects)+2:
            operations_shower(files_list)
        else:
            show_output(choice, all_objects[choice-1])


if __name__ == "__main__":
    main()
