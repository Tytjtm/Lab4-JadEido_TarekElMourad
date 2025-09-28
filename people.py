import re

class Person:
    """
    Base class for all people in the school system.
    """
    def __init__(self, name, age, email):
        """
        Constructor that sets up a person with basic info.
        """
        # Validating Age Here:
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")

        # Validating Email Here:
        email_val = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        if not re.match(email_val, email):
            raise ValueError("Invalid email format.")
        
        self.name = name  # Public
        self.age = age    # Public
        self._email = email  # Private (using underscore convention)

    def introduce(self):
        """
        Prints a simple introduction message.
        """
        print("Hello, my name is " + self.name + " and I am " + str(self.age) + " years old")


class Student(Person):
    """
    Student class that inherits from Person.
    """
    def __init__(self, name, age, email, std_id):
        """
        Creates a new student object.
        """
        super().__init__(name, age, email)
        self.id = std_id
        self.reg_courses = []  # List to store Course objects

    def register_course(self, course):
        """
        Adds a course to the student's registration list.
        """
        (self.reg_courses).append(course)


class Instructor(Person):
    """
    Instructor class, also inherits from Person.
    """
    def __init__(self, name, age, email, ins_id):
        """
        Creates a new instructor object.
        """
        super().__init__(name, age, email)
        self.id = ins_id
        self.ass_courses = []  # List to store assigned Course objects

    def assign_course(self, course):
        """
        Assigns a course to this instructor.
        """
        (self.ass_courses).append(course)


class Course:
    """
    Course class to represent individual courses.
    """
    def __init__(self, crs_id, crs_name, inst):
        """
        Creates a new course object.
        """
        self.id = crs_id
        self.name = crs_name
        self.instructor = inst
        self.enrolled_students = []  # List to store Student objects

    def add_student(self, student):
        """
        Enrolls a student in this course.
        """
        (self.enrolled_students).append(student)