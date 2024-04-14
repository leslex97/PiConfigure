import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QInputDialog, QLineEdit, QLabel, QVBoxLayout, QRadioButton ,QWidget, QFileDialog, QHBoxLayout
from operations import SystemChanger, Validator

class RpiCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Konfigurator")
        self.setGeometry(1200, 700, 1200, 700)
        self.path_finder_window()
        
       
    def welcome_view(self):
        pass
        
    def path_finder_window(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.main_window)

        boot_space = QHBoxLayout()
        self.rpi_boot_path = QLineEdit()
        self.rpi_boot_path.setPlaceholderText("Podaj lokalizacje folderu boot..")
        boot_path_button = QPushButton("Zmien")
        boot_path_button.clicked.connect(lambda:self.get_path('boot'))
        boot_space.addWidget(self.rpi_boot_path)
        boot_space.addWidget(boot_path_button)    
        
        root_space = QHBoxLayout()
        self.rpi_root_path = QLineEdit()
        self.rpi_root_path.setPlaceholderText("Podaj lokalizacje folderu root..")
        root_path_button = QPushButton("Zmien")
        root_path_button.clicked.connect(lambda:self.get_path("root"))
        root_space.addWidget(self.rpi_root_path)
        root_space.addWidget(root_path_button)
        self.rpi_root_path.changeEvent
        self.main_layout.addLayout(boot_space)       
        self.main_layout.addLayout(root_space)
        self.main_layout.addWidget(self.next_button)

        
        self.rpi_root_path.textChanged.connect(self.turn_on_button)
        
    def turn_on_button(self):
        self.next_button.setEnabled(True)
        
    def get_path(self, path):
        directory = QFileDialog.getExistingDirectory(self, "Wybierz Katalog", "/home", QFileDialog.ShowDirsOnly)
        if directory:
            if path == "boot" and Validator.validate_boot(directory):
                self.boot_directory = directory
                self.rpi_boot_path.setText(self.boot_directory)
                
            elif path == "root" and Validator.validate_root(directory):
                self.root_directory = directory
                self.rpi_root_path.setText(self.root_directory)

        else:
            print('siema')
            self.path_finder_window()
            
    def get_file_path(self, path):
        desktop_path = os.path.join(self.root_directory,'home/pi/Desktop/programy/')
        directory = QFileDialog.getOpenFileName(self, "Wybierz Plik", desktop_path)
        if directory:
            if path == 'program':
                self.program_directory = directory[0]
                print(self.program_directory)
                self.program_path.setText(self.program_directory)    
                        
    def main_window(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.system = SystemChanger(self.boot_directory, self.root_directory)
        
        os_version_label = QLabel()
        os_version_label.setText(self.system.check_system_version())
        os_version_label.setStyleSheet("""font-size: 30px;
                                       font-weight: bold;
                                       color:rgb(0,100,100);
                                       text-align: center;""")
        
        
        self.ip_field = QLineEdit()
        self.ip_field.setPlaceholderText("Adres IP")
        self.ip_field.setStyleSheet('background-color: rgb(0,0,0); color: rgb(255,255,255);')
        
        self.fstab_field = QLineEdit()
        self.fstab_field.setPlaceholderText("Numer snd (Przyklad: snd53)")
        
        self.program_field = QHBoxLayout()
        self.program_path = QLineEdit()
        self.program_path.setPlaceholderText("Sciezka programu, ktory bedzie dzialal na malinie")
        self.program_button = QPushButton("Zmien")
        self.program_button.clicked.connect(lambda:self.get_file_path("program"))
        self.program_field.addWidget(self.program_path)
        self.program_field.addWidget(self.program_button)
        
        self.send_button = QPushButton("Start")
        self.send_button.clicked.connect(self.set_properties)
        
        self.main_layout.addWidget(os_version_label)  
        self.main_layout.addWidget(self.ip_field)  
        self.main_layout.addWidget(self.fstab_field)
        self.main_layout.addLayout(self.program_field)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.send_button)
    
    def set_properties(self):
        self.system.set_snd(self.fstab_field.text())
        self.system.set_program(self.program_directory)
        self.system.change_ip(self.ip_field.text())
        self.system.change_hostname(self.ip_field.text())
        self.finish_window()
        
    def finish_window(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        print(self.program_directory, self.fstab_field.text(), self.ip_field.text())
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpiCreator()
    window.show()
    sys.exit(app.exec_()) 