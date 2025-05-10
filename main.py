from abc import ABC, abstractmethod
import platform, os

#test

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    
class Menu(ABC):
    def __init__(self, name, parent=None, type="", size=None, unit=None):
        self._files=[]
        self._file_name=name
        self._parent=parent #subject for removal
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
            user_input = input(message)
            
            if input_type == int:
                if user_input.isdigit():
                    user_input = int(user_input)
                else:
                    raise ValueError
            
            if condition[0]=="include" and user_input not in condition[1]:
                raise ValueError
            if condition[0]=="exclude" and user_input in condition[1]:
                raise ValueError
            if condition[0]=="range" and user_input <= 0:
                raise ValueError
            return user_input

        except ValueError:
            print("Only enter valid inputs!!!")
            return self.validate_input(input_type, message, condition)
    
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
    def __init__(self, name, parent=None, type="", size=None, unit=None):
        super().__init__(name, parent, type, size, unit)
    
    def show(self):
        if self.files:
            maximum=[8]*3
            for i in self.files:
                if len(i.file_name)+4>maximum[0]: maximum[0] = len(i.file_name) + 4
                if len(i.file_type)+4>maximum[1]: maximum[1] = len(i.file_type) + 4 
                if len(str(i.file_size))>maximum[2]: maximum[2] = len(str(i.file_size))
    
            print(f"{"Name":{maximum[0]}}{"Type":{maximum[1]}}{"Size":{maximum[2]+2}}")
            for i in self.files:
                print(f"{i.file_name:{maximum[0]}}{i.file_type:{maximum[1]}}", end="")
                if i.file_size>0:
                    print(f"{i.file_size:{maximum[2]}}", end=" ")
                    print(f"{i.file_unit:2}")
                else: print()
        else:
            print("Empty Folder")

    def create_file(self, name, type, size, unit):
        self.files.append(SSD(name, None, type, size, unit))
    
    def create_folder(self, name):
        self.files.append(SSD(name, self,"File folder", 0, ""))
    
    def delete_file(self, name):
        for i in range(len(self.files)):
            if self.files[i].file_name == name:
                self.files.pop(i)
                return
    
def open_menu(device):
    while True:
        clear_console()
        device.show()
        files={i.file_name: i.file_type for i in device.files}
        print("\nWhich Action do you wanna do?")
        print("1. Open File")
        print("2. Create File")
        print("3. Create Folder")
        print("4. Delete File")
        print("0. Back")
        choice=input("\nEnter choice: ")
        
        if choice == "1":
            choice=input("Select a File: ")
            while True:
                if choice not in files.keys(): 
                    print("Invalide Input!")
                    choice=input("Select a File: ")
                elif files[choice] == "File folder":
                    open_menu(device.files[list(files.keys()).index(choice)])
                    break
        elif choice == "2":
            name=device.validate_input(str, "Input file name: ", ("exclude", [i.file_name for i in device.files]))
            type=device.validate_input(str, f"Input file type ({', '.join(device.FILE_TYPES.keys())}): ", ("include", device.FILE_TYPES))
            size=device.validate_input(int, "Input file size: ", ("range",))
            unit=device.validate_input(str, f"Input file unit ({', '.join(device.UNITS.keys()).title()}): ", ("include", device.UNITS.keys()))
            device.create_file(name, type, size, unit)
        elif choice == "3":
            name=input("Input Folder name: ")
            device.create_folder(name)
        elif choice == "4":
            name=input("Input file name: ")
            device.delete_file(name)
        elif choice == "0":
            return "Success"

def initialize():
    root=SSD("C")
    root.create_file("test", "png", 100000000, "MB")
    root.create_file("test1", "jpeg", 20, "KB")
    root.create_file("test2", "pdf", 30, "GB")
    root.create_file("test3", "docx", 40, "TB")
    root.create_folder("pictures")
    return root

open_menu(initialize())
