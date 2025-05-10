from abc import ABC, abstractmethod
import platform, os

def clear_console():
    os.system('cls' if platform.system()=="Windows" else 'clear')

class Menu(ABC):
    UNITS={
        "TB": pow(1024, 4),
        "GB": pow(1024, 3),
        "MB": pow(1024, 2),
        "KB": 1024,
        "B": 1
    }

    FILE_TYPES={
        "png": "PNG File",
        "jpeg": "JPEG File",
        "pdf": "PDF File",
        "docx": "Word Document",
        "mp4": "MP4 Video",
        "mp3": "MP3 Audio",
        "txt": "Text Document",
    }

    def __init__(self, name, parent=None, type="", size=0, unit=""):
        self._files=[]
        self._file_name=name
        self._parent=parent # Subject for Removal
        self._file_type=type
        self._file_size=size
        self._file_unit=unit

    def validate_input(self, input_type, message: str, condition: tuple=None):
        """
        Validates user input based on the specified type and conditions.
        Args:
            input_type (str/int): The type of input expected ('int' for number, 'str' for string).
            message (str): The message to display to the user.
            condition (tuple): A tuple containing the condition type ('include' or 'exclude') and a list of valid values.
        """
        try:
            user_input=input(message).strip()
                
            if user_input.lower()=="exit":
                return None

            if input_type==int:
                if user_input.isdigit():
                    user_input=int(user_input)
                else:
                    raise ValueError("Input must be an integer.")

            if type(condition)!=tuple and condition != None and not condition[1]:
                input("Error: Empty Selection.")
                return
            if condition:
                if condition[0]=="include" and user_input not in condition[1]:
                    raise ValueError("Input is not in one of the options.")
                elif condition[0]=="exclude" and user_input in condition[1]:
                    raise ValueError("Existing name found, please input a different name.")
                elif condition[0]=="greater" and user_input <= condition[1]:
                    raise ValueError(f"Inputs less than or equal to {condition[1]} is not allowed.")

            return user_input

        except ValueError as e:
            print(f"\nError: {e}")
            return self.validate_input(input_type, message, condition)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files=value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name=value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent=value

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type=value

    @property
    def file_size(self):
        return self._file_size

    @file_size.setter
    def file_size(self, value):
        self._file_size=value

    @property
    def file_unit(self):
        return self._file_unit

    @file_unit.setter
    def file_unit(self, value):
        self._file_unit=value

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def create_file(self, name, type, size, unit):
        pass

    @abstractmethod
    def create_folder(self, name):
        pass

    @abstractmethod
    def delete_file(self, name):
        pass

class SSD(Menu):
    def __init__(self, name, parent=None, type="", size=0, unit=""):
        super().__init__(name, parent, type, size, unit)

    def show(self, selected=0):
        if self.files:
            headers=["Name", "Type", "Size"]
            maximum=[len(i) for i in headers]
            for i in self.files:
                maximum[0]=max(maximum[0], len(i.file_name))
                maximum[1]=max(maximum[1], len(i.file_type))
                maximum[2]=max(maximum[2], len(str(i.file_size)))
            maximum=[i + 4 for i in maximum]

            print(f"{headers[0]:<{maximum[0]-1}}|{headers[1]:<{maximum[1]-1}}|{headers[2]:<{maximum[2]}}|")
            for i,file in enumerate(self.files):
                if i==selected:
                    print("\033[48;2;88;84;84m", end="")
                print(f"{file.file_name:<{maximum[0]}}{file.file_type:<{maximum[1]}}", end="")
                if file.file_size > 0:
                    print_size=str(file.file_size) + " " + file.file_unit
                else:
                    print_size=""
                print(f"{print_size:<{maximum[2]}}")
                print("\033[0m", end="")
        else:
            print("Empty Folder")

    def create_file(self, name, type, size, unit):
        self.files.append(SSD(name, None, type, size, unit))

    def create_folder(self, name):
        self.files.append(SSD(name, self, "File folder", 0, ""))

    def delete_file(self, name):
        for i, file in enumerate(self.files):
            if file.file_name==name:
                self.files.pop(i)
                return

import msvcrt
def open_menu(device):
    key=""
    index=0
    while True:
        clear_console()
        device.show(index)
        print("\nActions (Enter \"exit\" to cancel action):")
        print("1. Create File")
        print("2. Create Folder")
        print("3. Delete File/Folder")
        print("0. Back\n")
        print("Select an Action: ", end="")
        
        choice=""
        if device.files:
            key=msvcrt.getch()
            if key==b'\x00' or key==b'\xe0':
                key=msvcrt.getch()
                if key==b'H' and index > 0:
                    index-=1
                elif key==b'P' and index < len(device.files)-1:
                    index+=1
            elif key==b'\r' and device.files[index].file_type=="File folder":
                open_menu(device.files[index])
            else:
                print(key.decode(), end="")
                choice=key.decode()+input()
                
                if choice.isdigit() and int(choice) in range(4):
                    choice=int(choice)
                else:
                    continue
        else:
            choice=input()
            choice=int(choice) if choice.isdigit() and int(choice) in range(4) else ""
        
        if choice==1:
            name=device.validate_input(str, "Input file name: ", ("exclude", [i.file_name for i in device.files]))
            type=device.validate_input(str, f"Input file type ({', '.join(device.FILE_TYPES.keys())}): ", ("include", device.FILE_TYPES))
            size=device.validate_input(int, "Input file size: ", ("greater",0))
            unit=device.validate_input(str, f"Input file unit ({', '.join(device.UNITS.keys()).title()}): ", ("include", device.UNITS.keys()))
            device.create_file(name, type, size, unit)
        elif choice==2:
            name=device.validate_input(str, "Input folder name: ", ("exclude", [i.file_name for i in device.files]))
            device.create_folder(name)
        elif choice==3:
            name=device.validate_input(str, "Input file name: ", ("include", [i.file_name for i in device.files]))
            device.delete_file(name)
        elif choice==0:
            return 

def initialize():
    root=SSD("C")
    root.create_file("test", "png", 100000000, "MB")
    root.create_file("test1", "jpeg", 20, "KB")
    root.create_file("test2", "pdf", 30, "GB")
    root.create_file("test3", "docx", 40, "TB")
    root.create_folder("pictures")
    return root

open_menu(initialize())

"""
added input validation for open file, create folder, and delete file
cleaned up show function
edited validate_input function to handle specific conditions
revamped the menu system to include easy navigation
"""