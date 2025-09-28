import tkinter as tk
from tkinter import ttk, messagebox
from people import Student, Instructor, Course
import database 
from serialization_csv import save_to_csv, load_from_csv

class SchoolGUI:
    """
    Tkinter-based GUI for the school management system.
    
    This was my first attempt at making a GUI and it shows. The code is a bit messy
    but it works! I used tabs to organize different functionalities.
    
    :ivar root: Main Tkinter window
    :vartype root: tk.Tk
    :ivar students_list: List of all students 
    :vartype students_list: list
    :ivar instructors_list: List of all instructors
    :vartype instructors_list: list  
    :ivar courses_list: List of all courses
    :vartype courses_list: list
    """
    
    def __init__(self):
        """
        Initialize the Tkinter GUI.
        
        Sets up the main window and creates empty lists for data storage.
        Also calls setup_gui to build all the interface elements.
        """
        self.root = tk.Tk()
        self.root.title("My School System")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        
        # my data lists
        self.students_list = []
        self.instructors_list = []
        self.courses_list = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """
        Set up all the GUI components.
        
        Creates the main notebook widget with tabs for different functions.
        Each tab handles a specific part of the system.
        """
        # main tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # student tab
        student_frame = ttk.Frame(notebook)
        notebook.add(student_frame, text="Students")
        self.make_student_tab(student_frame)
        
        # instructor tab
        instructor_frame = ttk.Frame(notebook)
        notebook.add(instructor_frame, text="Instructors") 
        self.make_instructor_tab(instructor_frame)
        
        # course tab
        course_frame = ttk.Frame(notebook)
        notebook.add(course_frame, text="Courses")
        self.make_course_tab(course_frame)
        
        # registration tab - this was confusing
        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text="Register")
        self.make_reg_tab(reg_frame)
        
        # view everything tab
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="View All")
        self.make_view_tab(view_frame)
        
        # save tab
        save_frame = ttk.Frame(notebook)
        notebook.add(save_frame, text="Save Data")
        self.make_save_tab(save_frame)
    
    def make_student_tab(self, parent):
        """
        Creates the student management tab.
        
        Has form fields for entering student info and buttons for actions.
        Uses grid layout for the form which took me a while to get right.
        
        :param parent: Parent widget to attach this tab to
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="Add Student", font=('Times', 18)).pack(pady=20)
        
        # entry fields
        form = tk.Frame(parent)
        form.pack(pady=20)
        
        tk.Label(form, text="Name:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Age:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')  
        self.age_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Email:", font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.email_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Student ID:", font=('Arial', 11)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.student_id_entry = tk.Entry(form, width=30, font=('Arial', 11))  
        self.student_id_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=30)
        
        add_btn = tk.Button(btn_frame, text="Add Student", command=self.add_student, 
                           bg='green', fg='white', font=('Arial', 12), width=12)
        add_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_student, 
                             bg='red', fg='white', font=('Arial', 12), width=12)
        clear_btn.pack(side='left', padx=10)
    
    def make_instructor_tab(self, parent):
        """
        Creates the instructor management tab.
        
        Similar to the student tab but for instructors. Copy-pasted most of it
        and just changed the variable names.
        
        :param parent: Parent widget for this tab
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="Add Instructor", font=('Times', 18)).pack(pady=20)
        
        # form stuff
        form = tk.Frame(parent)
        form.pack(pady=20)
        
        tk.Label(form, text="Name:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.inst_name_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.inst_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Age:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.inst_age_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.inst_age_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Email:", font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.inst_email_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.inst_email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Instructor ID:", font=('Arial', 11)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.inst_id_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.inst_id_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=30)
        
        add_btn = tk.Button(btn_frame, text="Add Instructor", command=self.add_instructor, 
                           bg='blue', fg='white', font=('Arial', 12), width=14)
        add_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_instructor, 
                             bg='red', fg='white', font=('Arial', 12), width=12)
        clear_btn.pack(side='left', padx=10)
    
    def make_course_tab(self, parent):
        """
        Creates the course management tab.
        
        This one has a dropdown (combobox) for selecting instructors which 
        made it more complicated than the other tabs.
        
        :param parent: Parent widget for this tab
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="Add Course", font=('Times', 18)).pack(pady=20)
        
        form = tk.Frame(parent)
        form.pack(pady=20)
        
        tk.Label(form, text="Course ID:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.course_id_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.course_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Course Name:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.course_name_entry = tk.Entry(form, width=30, font=('Arial', 11))
        self.course_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form, text="Instructor:", font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.instructor_combo = ttk.Combobox(form, width=27, font=('Arial', 11))
        self.instructor_combo.grid(row=2, column=1, padx=10, pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=30)
        
        add_btn = tk.Button(btn_frame, text="Add Course", command=self.add_course, 
                           bg='orange', fg='white', font=('Arial', 12), width=12)
        add_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_course, 
                             bg='red', fg='white', font=('Arial', 12), width=12)
        clear_btn.pack(side='left', padx=10)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.update_instructor_combo, 
                               bg='gray', fg='white', font=('Arial', 12), width=12)
        refresh_btn.pack(side='left', padx=10)
    
    def make_reg_tab(self, parent):
        """
        Creates the student registration tab.
        
        This tab lets you register students for courses. Uses two dropdowns
        which need to be kept in sync with the data.
        
        :param parent: Parent widget for this tab
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="Register Student for Course", font=('Times', 18)).pack(pady=20)
        
        form = tk.Frame(parent)
        form.pack(pady=20)
        
        tk.Label(form, text="Select Student:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=15, sticky='w')
        self.student_combo = ttk.Combobox(form, width=35, font=('Arial', 11))
        self.student_combo.grid(row=0, column=1, padx=10, pady=15)
        
        tk.Label(form, text="Select Course:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=15, sticky='w')
        self.course_combo = ttk.Combobox(form, width=35, font=('Arial', 11))
        self.course_combo.grid(row=1, column=1, padx=10, pady=15)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=30)
        
        reg_btn = tk.Button(btn_frame, text="Register Student", command=self.register_student, 
                           bg='green', fg='white', font=('Arial', 12), width=15)
        reg_btn.pack(side='left', padx=10)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh Lists", command=self.update_reg_combos, 
                               bg='gray', fg='white', font=('Arial', 12), width=15)
        refresh_btn.pack(side='left', padx=10)
    
    def make_view_tab(self, parent):
        """
        Creates the view/search tab.
        
        This tab shows all data in a table and has search functionality.
        The treeview widget was new to me and took some figuring out.
        
        :param parent: Parent widget for this tab
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="View All Data", font=('Times', 18)).pack(pady=15)
        
        # search stuff
        search_frame = tk.Frame(parent)
        search_frame.pack(pady=15)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 11)).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=25, font=('Arial', 11))
        self.search_entry.pack(side='left', padx=5)
        
        search_btn = tk.Button(search_frame, text="Search", command=self.search_data, 
                              bg='lightblue', font=('Arial', 11))
        search_btn.pack(side='left', padx=5)
        
        show_btn = tk.Button(search_frame, text="Show All", command=self.show_all_data, 
                            bg='lightgreen', font=('Arial', 11))
        show_btn.pack(side='left', padx=5)
        
        # table for displaying data
        columns = ('Type', 'ID', 'Name', 'Info')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=16)
        
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column('Type', width=80)
        self.tree.column('ID', width=100)
        self.tree.column('Name', width=150)
        self.tree.column('Info', width=250)
        
        self.tree.pack(fill='both', expand=True, padx=15, pady=15)
        
        # delete button
        delete_btn = tk.Button(parent, text="Delete Selected", command=self.delete_selected, 
                              bg='red', fg='white', font=('Arial', 11))
        delete_btn.pack(pady=10)
    
    def make_save_tab(self, parent):
        """
        Creates the save/load data tab.
        
        Simple tab with just a save button for now. Was planning to add 
        load functionality but ran out of time.
        
        :param parent: Parent widget for this tab
        :type parent: ttk.Frame
        """
        tk.Label(parent, text="Save & Load Data", font=('Times', 18)).pack(pady=30)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=50)
        
        save_btn = tk.Button(btn_frame, text="Save to CSV", command=self.save_to_csv, 
                            bg='purple', fg='white', font=('Arial', 14), width=15)
        save_btn.pack(pady=20)
        
        # TODO: add load function later if I have time
    
    # Functions for adding stuff to the system
    def add_student(self):
        """
        Add a new student to the system.
        
        Gets data from the form fields, validates it, creates a Student object,
        and adds it to the list. Shows success/error messages.
        
        :raises ValueError: When student data validation fails
        """
        try:
            name = self.name_entry.get()
            age = int(self.age_entry.get())
            email = self.email_entry.get()
            student_id = self.student_id_entry.get()
            
            if name == "" or email == "" or student_id == "":
                messagebox.showerror("Error", "Please fill all fields!")
                return
                
            new_student = Student(name, age, email, student_id)
            self.students_list.append(new_student)
            
            messagebox.showinfo("Success", f"Student {name} added!")
            self.clear_student()
            self.show_all_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong: " + str(e))
    
    def add_instructor(self):
        """
        Add a new instructor to the system.
        
        Similar to add_student but for instructors. Also updates the 
        instructor dropdown after adding.
        
        :raises ValueError: When instructor data validation fails
        """
        try:
            name = self.inst_name_entry.get()
            age = int(self.inst_age_entry.get()) 
            email = self.inst_email_entry.get()
            instructor_id = self.inst_id_entry.get()
            
            if not name or not email or not instructor_id:
                messagebox.showerror("Error", "Fill all fields please!")
                return
                
            new_instructor = Instructor(name, age, email, instructor_id)
            self.instructors_list.append(new_instructor)
            
            messagebox.showinfo("Success", f"Instructor {name} added!")
            self.clear_instructor()
            self.update_instructor_combo()
            self.show_all_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except:
            messagebox.showerror("Error", "Something went wrong!")
    
    def add_course(self):
        """
        Add a new course to the system.
        
        Gets course info and tries to match the selected instructor.
        This part was tricky because of the dropdown selection parsing.
        
        :raises Exception: When course creation fails
        """
        try:
            course_id = self.course_id_entry.get()
            course_name = self.course_name_entry.get()  
            instructor_selection = self.instructor_combo.get()
            
            if not course_id or not course_name:
                messagebox.showerror("Error", "Need course ID and name!")
                return
            
            # find instructor - this part was tricky
            instructor = None
            if instructor_selection:
                for inst in self.instructors_list:
                    if inst.id in instructor_selection:
                        instructor = inst
                        break
            
            new_course = Course(course_id, course_name, instructor)
            self.courses_list.append(new_course)
            
            if instructor:
                instructor.assign_course(new_course)
            
            messagebox.showinfo("Success", f"Course {course_name} added!")
            self.clear_course()
            self.show_all_data()
            
        except Exception as e:
            messagebox.showerror("Error", "Error adding course: " + str(e))
    
    def register_student(self):
        """
        Register a student for a course.
        
        Parses the dropdown selections to find the right student and course objects,
        then creates the registration relationship. This was the most confusing part.
        
        :raises Exception: When registration fails or objects can't be found
        """
        try:
            student_selection = self.student_combo.get()
            course_selection = self.course_combo.get()
            
            if not student_selection or not course_selection:
                messagebox.showerror("Error", "Select both student and course!")
                return
            
            # find student and course - this part was tricky
            student = None
            course = None
            
            for s in self.students_list:
                if s.id in student_selection:
                    student = s
                    break
                    
            for c in self.courses_list:
                if c.id in course_selection:
                    course = c
                    break
            
            if student and course:
                student.register_course(course)
                course.add_student(student)
                messagebox.showinfo("Success", f"{student.name} registered for {course.name}!")
                self.show_all_data()
            else:
                messagebox.showerror("Error", "Couldn't find student or course")
                
        except Exception as e:
            messagebox.showerror("Error", "Registration failed: " + str(e))
    
    def show_all_data(self):
        """
        Display all data in the treeview table.
        
        Clears the table and rebuilds it with current data. Shows students,
        instructors, and courses with summary info for each.
        """
        # clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # add students
        for student in self.students_list:
            num_courses = len(student.reg_courses)
            self.tree.insert('', 'end', values=('Student', student.id, student.name, f'{num_courses} courses enrolled'))
        
        # add instructors  
        for instructor in self.instructors_list:
            num_courses = len(instructor.ass_courses)
            self.tree.insert('', 'end', values=('Instructor', instructor.id, instructor.name, f'{num_courses} courses teaching'))
        
        # add courses
        for course in self.courses_list:
            inst_name = course.instructor.name if course.instructor else "No instructor"
            num_students = len(course.enrolled_students)
            info = f"Instructor: {inst_name}, Students: {num_students}"
            self.tree.insert('', 'end', values=('Course', course.id, course.name, info))
    
    def search_data(self):
        """
        Search through all data based on user input.
        
        Looks for matches in names and IDs across students, instructors, and courses.
        Case-insensitive search which I thought was important.
        """
        search_text = self.search_entry.get().lower()
        if not search_text:
            self.show_all_data()
            return
        
        # clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # search students
        for student in self.students_list:
            if search_text in student.name.lower() or search_text in student.id.lower():
                num_courses = len(student.reg_courses)
                self.tree.insert('', 'end', values=('Student', student.id, student.name, f'{num_courses} courses'))
        
        # search instructors
        for instructor in self.instructors_list:
            if search_text in instructor.name.lower() or search_text in instructor.id.lower():
                num_courses = len(instructor.ass_courses)
                self.tree.insert('', 'end', values=('Instructor', instructor.id, instructor.name, f'{num_courses} courses'))
        
        # search courses
        for course in self.courses_list:
            if search_text in course.name.lower() or search_text in course.id.lower():
                inst_name = course.instructor.name if course.instructor else "None"
                self.tree.insert('', 'end', values=('Course', course.id, course.name, f'Instructor: {inst_name}'))
    
    def delete_selected(self):
        """
        Delete the selected item from the system.
        
        Gets the selected row from the table, confirms deletion, then removes
        the item from the appropriate list. Updates dropdowns after deletion.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select something to delete")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        item_type = values[0]
        item_id = values[1]
        item_name = values[2]
        
        # confirm deletion
        if messagebox.askyesno("Confirm", f"Delete {item_type} '{item_name}'?"):
            try:
                if item_type == 'Student':
                    # remove from list
                    self.students_list = [s for s in self.students_list if s.id != item_id]
                elif item_type == 'Instructor':
                    self.instructors_list = [i for i in self.instructors_list if i.id != item_id]
                elif item_type == 'Course':
                    self.courses_list = [c for c in self.courses_list if c.id != item_id]
                
                self.tree.delete(item)
                self.update_instructor_combo()
                self.update_reg_combos()
                messagebox.showinfo("Success", f"{item_type} deleted!")
                
            except Exception as e:
                messagebox.showerror("Error", "Failed to delete: " + str(e))
    
    def save_to_csv(self):
        """
        Save all data to CSV files.
        
        Calls the global save_to_csv function with current data.
        Shows success/error message to user.
        """
        try:
            save_to_csv(self.students_list, self.instructors_list, self.courses_list)
            messagebox.showinfo("Success", "Data saved to CSV files!")
        except Exception as e:
            messagebox.showerror("Error", "Save error: " + str(e))
    
    # Clear functions - these reset the form fields
    def clear_student(self):
        """Clear all student form fields."""
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)
    
    def clear_instructor(self):
        """Clear all instructor form fields."""
        self.inst_name_entry.delete(0, tk.END)
        self.inst_age_entry.delete(0, tk.END)
        self.inst_email_entry.delete(0, tk.END)
        self.inst_id_entry.delete(0, tk.END)
    
    def clear_course(self):
        """Clear all course form fields."""
        self.course_id_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        self.instructor_combo.set('')
    
    # Update dropdown lists - these keep the combos in sync with current data
    def update_instructor_combo(self):
        """
        Update the instructor dropdown with current instructors.
        
        Refreshes the combobox values to show all available instructors.
        """
        instructor_list = []
        for inst in self.instructors_list:
            instructor_list.append(f"{inst.id} - {inst.name}")
        self.instructor_combo['values'] = instructor_list
    
    def update_reg_combos(self):
        """
        Update both registration dropdown lists.
        
        Refreshes student and course dropdowns for the registration tab.
        """
        # update student dropdown
        student_list = []
        for s in self.students_list:
            student_list.append(f"{s.id} - {s.name}")
        self.student_combo['values'] = student_list
        
        # update course dropdown  
        course_list = []
        for c in self.courses_list:
            course_list.append(f"{c.id} - {c.name}")
        self.course_combo['values'] = course_list
    
    def run(self):
        """
        Start the GUI application.
        
        Starts the Tkinter main event loop.
        """
        self.root.mainloop()
