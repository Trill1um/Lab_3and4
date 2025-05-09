from abc import ABC, abstractmethod
import time, platform, os

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class Menu(ABC):
    def __init__(self, name, parent=None, type="", size=None, unit=None):
        self.files={}
        self.file_name=name
        self.parent=parent
        self.file_type=type
        self.file_size=size
        self.file_unit=unit

class SSD(Menu):
    def __init__(self, name, parent=None, type="", size=0, unit=None):
        super().__init__(name, parent, type, size, unit)
    
    def show(self):
        if self.files:
            maximum=[8]*3
            for i in self.files.values():
                if len(i.file_name)>maximum[0]: maximum[0] = len(i.file_name)
                if len(i.file_type)>maximum[1]: maximum[1] = len(i.file_type)
                if len(str(i.file_size))>maximum[2]: maximum[2] = len(str(i.file_size))
            maximum[0]+=4
            maximum[1]+=4
            print(f"{"Name":{maximum[0]}}{"Type":{maximum[1]}}{"Size":{maximum[2]+2}}")
            
            for i in self.files.values():
                print(f"{i.file_name:{maximum[0]}}{i.file_type:{maximum[1]}}", end="")
                if i.file_size>0:
                    print(f"{i.file_size:{maximum[2]}}", end=" ")
                    print(f"{i.file_unit:2}")
                else: print()
        else:
            print("Empty Folder")

    def create_file(self, name, type, size, unit):
        self.files[name]=(SSD(name, None, type, size, unit))
    
    def create_folder(self, name):
        self.files[name]=(SSD(name, self,"File folder", 0, ""))
    
    def delete_file(self, name):
        self.files.pop(name)
    
    def traverse(self):
        while True:
            clear_console()
            self.show()
            files={i.file_name: i.file_type for i in self.files.values()}
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
                    if choice not in files.keys(): print("Invalide Input!")
                    else:
                        if files[choice] == "File folder":
                            self.files[choice].traverse()
            elif choice == "2":
                name=input("Input file name: ")
                type=input("Input file type: ")
                size=int(input("Input file size: "))
                unit=input("Input file unit (B, KB, MB etc.): ")
                self.create_file(name, type, size, unit)
            elif choice == "3":
                name=input("Input Folder name: ")
                self.create_folder(name)
            elif choice == "4":
                name=input("Input file name: ")
                self.delete_file(name)
            elif choice == "0":
                if self.parent:
                    self.parent.traverse()
                else: return
                
root=SSD("C")
root.create_file("test", "png", 100000000, "MB")
root.create_file("test1", "jpeg", 20, "KB")
root.create_file("test2", "pdf", 30, "GB")
root.create_file("test3", "docx", 40, "TB")
root.create_folder("pictures")
root.traverse()