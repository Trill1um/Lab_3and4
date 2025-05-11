from abc import ABC, abstractmethod

class StorageDevice(ABC):
    def __init__(self, name, total_space_gb, used_space_gb=0):
        self._name = name
        self._total_space = total_space_gb
        self._used_space = used_space_gb
        self._files = []

    @property
    def name(self):
        return self._name
    
    @property
    def total_space(self):
        return self._total_space
    
    @property
    def used_space(self):
        return self._used_space
    
    @property
    def files(self):
        return self._files
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @total_space.setter
    def total_space(self, value):
        self._total_space = value
    
    @used_space.setter
    def used_space(self, value):
        self._used_space = value
    
    @files.setter
    def files(self, value):
        self._files = value
    
    @abstractmethod
    def save_file(self, file_name, size_gb):
        pass

    @abstractmethod
    def read_file(self, file_name):
        pass

    @abstractmethod
    def format_device(self):
        pass

    def show_storage(self):
        print(f"{self.name} Used: {self.used_space}GB / {self.total_space}GB")


class SSD(StorageDevice):
    def __init__(self, used_space_gb=0):
        super().__init__("SSD", 512, used_space_gb)

    def save_file(self, file_name, size_gb):
        if self.used_space + size_gb <= self.total_space:
            self.files.append(file_name)
            self.used_space += size_gb
            print(f"{file_name} saved to {self.name}.")
        else:
            print("Not enough space in SSD.")

    def read_file(self, file_name):
        if file_name in self.files:
            print(f"Reading {file_name} from {self.name}...")
        else:
            print(f"{file_name} not found in {self.name}.")

    def format_device(self):
        self.files.clear()
        self.used_space = 0
        print(f"{self.name} has been formatted.")


class CompactDisk(StorageDevice):
    def __init__(self, used_space_gb=0):
        super().__init__("Compact Disk", 0.7, used_space_gb)

    def save_file(self, file_name, size_gb):
        if self.used_space + size_gb <= self.total_space:
            self.files.append(file_name)
            self.used_space += size_gb
            print(f"{file_name} saved to {self.name}.")
        else:
            print("Not enough space on Compact Disk.")

    def read_file(self, file_name):
        if file_name in self.files:
            print(f"Reading {file_name} from {self.name}...")
        else:
            print(f"{file_name} not found in {self.name}.")

    def format_device(self):
        self.files.clear()
        self.used_space = 0
        print(f"{self.name} has been formatted.")


class HardDrive(StorageDevice):
    def __init__(self, used_space_gb=0):
        super().__init__("Hard Drive", 1024, used_space_gb)

    def save_file(self, file_name, size_gb):
        if self.used_space + size_gb <= self.total_space:
            self.files.append(file_name)
            self.used_space += size_gb
            print(f"{file_name} saved to {self.name}.")
        else:
            print("Not enough space on Hard Drive.")

    def read_file(self, file_name):
        if file_name in self.files:
            print(f"Reading {file_name} from {self.name}...")
        else:
            print(f"{file_name} not found in {self.name}.")

    def format_device(self):
        self.files.clear()
        self.used_space = 0
        print(f"{self.name} has been formatted.")


class FlashDrive(StorageDevice):
    def __init__(self, used_space_gb=0):
        super().__init__("Flash Drive", 64, used_space_gb)

    def save_file(self, file_name, size_gb):
        if self.used_space + size_gb <= self.total_space:
            self.files.append(file_name)
            self.used_space += size_gb
            print(f"{file_name} saved to {self.name}.")
        else:
            print("Not enough space on Flash Drive.")

    def read_file(self, file_name):
        if file_name in self.files:
            print(f"Reading {file_name} from {self.name}...")
        else:
            print(f"{file_name} not found in {self.name}.")

    def format_device(self):
        self.files.clear()
        self.used_space = 0
        print(f"{self.name} has been formatted.")


def main():
    ssd = SSD(used_space_gb=100)
    cd = CompactDisk(used_space_gb=0.1)
    hdd = HardDrive(used_space_gb=300)
    flash = FlashDrive(used_space_gb=10)

    print("\n--- SSD Test ---")
    ssd.show_storage()
    ssd.save_file("game.iso", 50)
    ssd.read_file("game.iso")
    ssd.format_device()
    ssd.show_storage()

    print("\n--- Compact Disk Test ---")
    cd.show_storage()
    cd.save_file("album.mp3", 0.2)
    cd.read_file("album.mp3")
    cd.format_device()
    cd.show_storage()

    print("\n--- Hard Drive Test ---")
    hdd.show_storage()
    hdd.save_file("movie.mp4", 200)
    hdd.read_file("movie.mp4")
    hdd.format_device()
    hdd.show_storage()

    print("\n--- Flash Drive Test ---")
    flash.show_storage()
    flash.save_file("doc.pdf", 1)
    flash.read_file("doc.pdf")
    flash.format_device()
    flash.show_storage()

if __name__ == "__main__":
    main()