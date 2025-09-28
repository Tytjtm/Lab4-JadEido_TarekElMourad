import sys
from tkinterGUI import SchoolGUI
from pyqtGUI import SchoolManagementPyQt
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    """
    Main program entry point.
    
    Gives the user a choice between Tkinter and PyQt5 interfaces.
    I added this choice because I wanted to try both GUI frameworks.
    """
    # Ask user which GUI to use
    print("Choose GUI framework:")
    print("1. Tkinter")
    print("2. PyQt5")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        app = SchoolGUI()
        app.run()
    elif choice == "2":
        app = QApplication(sys.argv)
        window = SchoolManagementPyQt()
        window.show()
        sys.exit(app.exec_())
    else:
        print("Invalid choice. Using Tkinter by default.")
        app = SchoolGUI()
        app.run()