import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QFormLayout, QLineEdit, QSpinBox, QHBoxLayout, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from people import Student, Instructor, Course
from serialization_csv import save_to_csv, load_from_csv
import database
import csv


class SchoolManagementPyQt(QMainWindow):
    """
    PyQt5 version of the school management GUI.
    
    I made this as an alternative to the Tkinter version because PyQt5 looks
    more modern. The functionality is basically the same but uses Qt widgets.
    
    :ivar students: List of Student objects
    :vartype students: list
    :ivar instructors: List of Instructor objects
    :vartype instructors: list
    :ivar courses: List of Course objects
    :vartype courses: list
    :ivar tabs: Main tab widget container
    :vartype tabs: QTabWidget
    """
    
    def __init__(self):
        """
        Initialize the PyQt5 main window.
        
        Sets up the window properties and initializes data storage.
        """
        super().__init__()
        self.setWindowTitle("School Management System - PyQt5")
        self.setGeometry(100, 100, 1000, 700)
        
        # Data storage
        self.students = []
        self.instructors = []
        self.courses = []
        
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the central widget and tab structure for the PyQt5 interface.
        """
        main_widg = QWidget()
        self.setCentralWidget(main_widg)
        
        layout = QVBoxLayout()
        main_widg.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_registration_tab()
        self.create_view_tab()
        self.create_file_tab()
    
    def create_student_tab(self):
        """
        Create the student management tab for PyQt5.
        
        Similar to the Tkinter version but using Qt widgets and layouts.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Add Student")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.student_name = QLineEdit()
        self.student_age = QSpinBox()
        self.student_age.setMaximum(120)
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        
        form_layout.addRow("Name:", self.student_name)
        form_layout.addRow("Age:", self.student_age)
        form_layout.addRow("Email:", self.student_email)
        form_layout.addRow("Student ID:", self.student_id)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Student")
        add_btn.clicked.connect(self.add_student)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_student_form)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Students")
    
    def create_instructor_tab(self):
        """Create the instructor management tab for PyQt5."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Add Instructor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.instructor_name = QLineEdit()
        self.instructor_age = QSpinBox()
        self.instructor_age.setMaximum(120)
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        
        form_layout.addRow("Name:", self.instructor_name)
        form_layout.addRow("Age:", self.instructor_age)
        form_layout.addRow("Email:", self.instructor_email)
        form_layout.addRow("Instructor ID:", self.instructor_id)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Instructor")
        add_btn.clicked.connect(self.add_instructor)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_instructor_form)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Instructors")
    
    def create_course_tab(self):
        """Create the course management tab for PyQt5."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Add Course")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        self.course_instructor = QComboBox()
        
        form_layout.addRow("Course ID:", self.course_id)
        form_layout.addRow("Course Name:", self.course_name)
        form_layout.addRow("Instructor:", self.course_instructor)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Course")
        add_btn.clicked.connect(self.add_course)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_course_form)
        refresh_btn = QPushButton("Refresh Instructors")
        refresh_btn.clicked.connect(self.refresh_instructor_list)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Courses")
    
    def create_registration_tab(self):
        """Create the registration tab for PyQt5."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Student Registration")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.reg_student = QComboBox()
        self.reg_course = QComboBox()
        
        form_layout.addRow("Select Student:", self.reg_student)
        form_layout.addRow("Select Course:", self.reg_course)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register_student)
        refresh_btn = QPushButton("Refresh Lists")
        refresh_btn.clicked.connect(self.refresh_registration_lists)
        
        button_layout.addWidget(register_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Registration")
    
    def create_view_tab(self):
        """Create the data viewing tab for PyQt5."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("View All Records")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_records)
        search_layout.addWidget(search_btn)
        
        show_all_btn = QPushButton("Show All")
        show_all_btn.clicked.connect(self.show_all_records)
        search_layout.addWidget(show_all_btn)
        
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Info'])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Delete button
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_record)
        layout.addWidget(delete_btn)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "View Records")
    
    def create_file_tab(self):
        """Create the file operations tab for PyQt5."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("File Operations")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Buttons
        save_btn = QPushButton("Save to CSV")
        save_btn.clicked.connect(self.save_data)
        layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load from CSV")
        load_btn.clicked.connect(self.load_data)
        layout.addWidget(load_btn)
        
        export_students_btn = QPushButton("Export Students CSV")
        export_students_btn.clicked.connect(lambda: self.export_csv('students'))
        layout.addWidget(export_students_btn)
        
        export_instructors_btn = QPushButton("Export Instructors CSV")
        export_instructors_btn.clicked.connect(lambda: self.export_csv('instructors'))
        layout.addWidget(export_instructors_btn)
        
        export_courses_btn = QPushButton("Export Courses CSV")
        export_courses_btn.clicked.connect(lambda: self.export_csv('courses'))
        layout.addWidget(export_courses_btn)
        
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "File Operations")
    
    # PyQt5 Event handlers - similar functionality to Tkinter version
    def add_student(self):
        """
        Add a new student through the PyQt5 interface.
        
        Gets data from Qt widgets and creates a Student object. PyQt5 widgets
        work a bit differently than Tkinter but the logic is the same.
        
        :raises ValueError: When student data validation fails
        """
        try:
            name = self.student_name.text().strip()
            age = self.student_age.value()
            email = self.student_email.text().strip()
            student_id = self.student_id.text().strip()
            
            if not all([name, email, student_id]):
                QMessageBox.warning(self, "Error", "All fields are required")
                return
            
            student = Student(name, age, email, student_id)
            self.students.append(student)
            QMessageBox.information(self, "Success", "Student added successfully")
            self.clear_student_form()
            self.show_all_records()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def add_instructor(self):
        """Add a new instructor through PyQt5 interface."""
        try:
            name = self.instructor_name.text().strip()
            age = self.instructor_age.value()
            email = self.instructor_email.text().strip()
            instructor_id = self.instructor_id.text().strip()
            
            if not all([name, email, instructor_id]):
                QMessageBox.warning(self, "Error", "All fields are required")
                return
            
            instructor = Instructor(name, age, email, instructor_id)
            self.instructors.append(instructor)
            QMessageBox.information(self, "Success", "Instructor added successfully")
            self.clear_instructor_form()
            self.refresh_instructor_list()
            self.show_all_records()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def add_course(self):
        """Add a new course through PyQt5 interface."""
        try:
            course_id = self.course_id.text().strip()
            course_name = self.course_name.text().strip()
            instructor_selection = self.course_instructor.currentText()
            
            if not all([course_id, course_name]):
                QMessageBox.warning(self, "Error", "Course ID and Name are required")
                return
            
            instructor = None
            if instructor_selection:
                # Find instructor by ID
                for inst in self.instructors:
                    if inst.id in instructor_selection:
                        instructor = inst
                        break
            
            course = Course(course_id, course_name, instructor)
            self.courses.append(course)
            if instructor:
                instructor.assign_course(course)
            
            QMessageBox.information(self, "Success", "Course added successfully")
            self.clear_course_form()
            self.show_all_records()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def register_student(self):
        """Register a student for a course through PyQt5 interface."""
        try:
            student_selection = self.reg_student.currentText()
            course_selection = self.reg_course.currentText()
            
            if not student_selection or not course_selection:
                QMessageBox.warning(self, "Error", "Select both student and course")
                return
            
            # Find student and course
            student = None
            course = None
            
            for s in self.students:
                if s.id in student_selection:
                    student = s
                    break
            
            for c in self.courses:
                if c.id in course_selection:
                    course = c
                    break
            
            if student and course:
                student.register_course(course)
                course.add_student(student)
                QMessageBox.information(self, "Success", "Student registered successfully")
                self.show_all_records()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def show_all_records(self):
        """
        Display all records in the PyQt5 table widget.
        
        Similar to the Tkinter version but uses QTableWidget instead of Treeview.
        """
        # Clear table
        self.table.setRowCount(0)
        
        row = 0
        # Add students
        for student in self.students:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Student"))
            self.table.setItem(row, 1, QTableWidgetItem(student.id))
            self.table.setItem(row, 2, QTableWidgetItem(student.name))
            self.table.setItem(row, 3, QTableWidgetItem(f"{len(student.reg_courses)} courses"))
            row += 1
        
        # Add instructors
        for instructor in self.instructors:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Instructor"))
            self.table.setItem(row, 1, QTableWidgetItem(instructor.id))
            self.table.setItem(row, 2, QTableWidgetItem(instructor.name))
            self.table.setItem(row, 3, QTableWidgetItem(f"{len(instructor.ass_courses)} courses"))
            row += 1
        
        # Add courses
        for course in self.courses:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Course"))
            self.table.setItem(row, 1, QTableWidgetItem(course.id))
            self.table.setItem(row, 2, QTableWidgetItem(course.name))
            instructor_name = course.instructor.name if course.instructor else "No instructor"
            self.table.setItem(row, 3, QTableWidgetItem(instructor_name))
            row += 1
    
    def search_records(self):
        """Search records in PyQt5 interface."""
        search_term = self.search_input.text().lower()
        if not search_term:
            self.show_all_records()
            return
        
        # Clear table
        self.table.setRowCount(0)
        row = 0
        
        # Search students
        for student in self.students:
            if search_term in student.name.lower() or search_term in student.id.lower():
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem("Student"))
                self.table.setItem(row, 1, QTableWidgetItem(student.id))
                self.table.setItem(row, 2, QTableWidgetItem(student.name))
                self.table.setItem(row, 3, QTableWidgetItem(f"{len(student.reg_courses)} courses"))
                row += 1
        
        # Search instructors
        for instructor in self.instructors:
            if search_term in instructor.name.lower() or search_term in instructor.id.lower():
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem("Instructor"))
                self.table.setItem(row, 1, QTableWidgetItem(instructor.id))
                self.table.setItem(row, 2, QTableWidgetItem(instructor.name))
                self.table.setItem(row, 3, QTableWidgetItem(f"{len(instructor.ass_courses)} courses"))
                row += 1
        
        # Search courses
        for course in self.courses:
            if search_term in course.name.lower() or search_term in course.id.lower():
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem("Course"))
                self.table.setItem(row, 1, QTableWidgetItem(course.id))
                self.table.setItem(row, 2, QTableWidgetItem(course.name))
                instructor_name = course.instructor.name if course.instructor else "No instructor"
                self.table.setItem(row, 3, QTableWidgetItem(instructor_name))
                row += 1
    
    def delete_record(self):
        """Delete selected record from PyQt5 interface."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Select a record to delete")
            return
        
        record_type = self.table.item(current_row, 0).text()
        record_id = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Delete {record_type} {record_id}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                if record_type == 'Student':
                    self.students = [s for s in self.students if s.id != record_id]
                elif record_type == 'Instructor':
                    self.instructors = [i for i in self.instructors if i.id != record_id]
                elif record_type == 'Course':
                    self.courses = [c for c in self.courses if c.id != record_id]
                
                self.show_all_records()
                self.refresh_instructor_list()
                self.refresh_registration_lists()
                QMessageBox.information(self, "Success", "Record deleted")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def save_data(self):
        """Save data using PyQt5 interface."""
        try:
            save_to_csv(self.students, self.instructors, self.courses)
            QMessageBox.information(self, "Success", "Data saved to CSV files")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {e}")
    
    def load_data(self):
        """Load data using PyQt5 interface."""
        try:
            self.students, self.instructors, self.courses = load_from_csv()
            self.show_all_records()
            self.refresh_instructor_list()
            self.refresh_registration_lists()
            QMessageBox.information(self, "Success", "Data loaded from CSV files")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
    
    def export_csv(self, data_type):
        """
        Export specific data type to CSV file.
        
        Opens a file dialog and exports the selected data type to a CSV file.
        This is extra functionality I added beyond the basic requirements.
        
        :param data_type: Type of data to export ('students', 'instructors', or 'courses')
        :type data_type: str
        """
        filename, _ = QFileDialog.getSaveFileName(self, f"Export {data_type}", "", "CSV Files (*.csv)")
        if filename:
            try:
                if data_type == 'students':
                    with open(filename, "w", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["ID", "Name", "Age", "Email", "Courses"])
                        for student in self.students:
                            courses = ', '.join([c.name for c in student.reg_courses])
                            writer.writerow([student.id, student.name, student.age, student._email, courses])
                elif data_type == 'instructors':
                    with open(filename, "w", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["ID", "Name", "Age", "Email", "Courses"])
                        for instructor in self.instructors:
                            courses = ', '.join([c.name for c in instructor.ass_courses])
                            writer.writerow([instructor.id, instructor.name, instructor.age, instructor._email, courses])
                elif data_type == 'courses':
                    with open(filename, "w", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["ID", "Name", "Instructor", "Students"])
                        for course in self.courses:
                            instructor_name = course.instructor.name if course.instructor else "None"
                            students = ', '.join([s.name for s in course.enrolled_students])
                            writer.writerow([course.id, course.name, instructor_name, students])
                
                QMessageBox.information(self, "Success", f"{data_type.title()} exported successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export {data_type}: {e}")
    
    # PyQt5 utility methods - mostly form clearing and dropdown updating
    def clear_student_form(self):
        """Clear all student form fields in PyQt5."""
        self.student_name.clear()
        self.student_age.setValue(0)
        self.student_email.clear()
        self.student_id.clear()
    
    def clear_instructor_form(self):
        """Clear all instructor form fields in PyQt5."""
        self.instructor_name.clear()
        self.instructor_age.setValue(0)
        self.instructor_email.clear()
        self.instructor_id.clear()
    
    def clear_course_form(self):
        """Clear all course form fields in PyQt5."""
        self.course_id.clear()
        self.course_name.clear()
        self.course_instructor.setCurrentText("")
    
    def refresh_instructor_list(self):
        """Refresh the instructor dropdown in PyQt5."""
        self.course_instructor.clear()
        self.course_instructor.addItem("")  # Empty option
        for instructor in self.instructors:
            self.course_instructor.addItem(f"{instructor.id} - {instructor.name}")
    
    def refresh_registration_lists(self):
        """Refresh both registration dropdowns in PyQt5."""
        # Students
        self.reg_student.clear()
        for student in self.students:
            self.reg_student.addItem(f"{student.id} - {student.name}")
        
        # Courses
        self.reg_course.clear()
        for course in self.courses:
            self.reg_course.addItem(f"{course.id} - {course.name}")

