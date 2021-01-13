
from absolute_loader import absolute_loader
from tabulate import tabulate


def main():
    files = input("Enter The Linked Files In The Desired Sequence: ")
    returned_memory = None
    all_objects = []
    object_record = {}
    files_list = files.split('+')

    for i in range(len(files_list)):
        object_record["file_name"] = files_list[i]
        object_record["memory"] = absolute_loader(
            files_list[i] + '.txt').return_memory()
        all_objects.append(object_record)
        object_record = {}

    while True:
        for i in range(len(all_objects)):
            print(i+1, '. ', all_objects[i]["file_name"])
        print(len(all_objects)+1, '. Final Result')
        choice = int(input("Select Option: "))
        if choice == 4:
            show_output(choice-1, all_objects[choice-2])
        else:
            show_output(choice, all_objects[choice-1])


def show_output(choice, object_record):
    print(object_record["file_name"])
    print(tabulate(object_record["memory"], headers="firstrow"))


if __name__ == "__main__":
    main()
