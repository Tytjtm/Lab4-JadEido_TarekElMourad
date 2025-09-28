from datetime import datetime
import sqlite3
import os
from people import Student, Instructor, Course

# Database operations - I added this later when I learned about SQL
# Based on the demo the professor showed us in class
def create_tables():
    """
    Create the database tables for the school system.
    
    Sets up the SQLite database with proper foreign key relationships.
    I struggled with the SQL syntax at first but eventually got it working.
    
    :raises sqlite3.Error: If there's a problem creating the database tables
    """
    db = sqlite3.connect('school.db')
    cursor = db.cursor()
    
    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STUDENTS
        (ID TEXT PRIMARY KEY,
         NAME TEXT NOT NULL,
         AGE INTEGER NOT NULL,
         EMAIL TEXT NOT NULL,
         CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)
    
    # Instructors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS INSTRUCTORS
        (ID TEXT PRIMARY KEY,
         NAME TEXT NOT NULL,
         AGE INTEGER NOT NULL,
         EMAIL TEXT NOT NULL,
         CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)
    
    # Courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COURSES
        (ID TEXT PRIMARY KEY,
         NAME TEXT NOT NULL,
         INSTRUCTOR_ID TEXT,
         CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (INSTRUCTOR_ID) REFERENCES INSTRUCTORS(ID))
    """)
    
    # Registrations table (many-to-many relationship)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS REGISTRATIONS
        (STUDENT_ID TEXT,
         COURSE_ID TEXT,
         CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
         PRIMARY KEY (STUDENT_ID, COURSE_ID),
         FOREIGN KEY (STUDENT_ID) REFERENCES STUDENTS(ID),
         FOREIGN KEY (COURSE_ID) REFERENCES COURSES(ID))
    """)
    
    db.commit()
    db.close()


def insert_student(student_id, name, age, email):
    """
    Insert a new student into the database.
    
    Adds a student record to the STUDENTS table. Handles duplicate IDs gracefully.
    
    :param student_id: Unique student identifier
    :type student_id: str
    :param name: Student's full name
    :type name: str
    :param age: Student's age in years
    :type age: int
    :param email: Student's email address
    :type email: str
    :return: True if insertion successful, False otherwise
    :rtype: bool
    :raises sqlite3.IntegrityError: If student ID already exists
    """
    try:
        db = sqlite3.connect('school.db')
        query = """
            INSERT INTO STUDENTS(ID, NAME, AGE, EMAIL)
            VALUES (?,?,?,?)
        """
        cursor = db.cursor()
        cursor.execute(query, (student_id, name, age, email))
        db.commit()
        db.close()
        print(f'Student {name} inserted successfully')
        return True
    except sqlite3.IntegrityError:
        print(f'Student with ID {student_id} already exists')
        return False
    except Exception as e:
        print(f'Error inserting student: {e}')
        return False


def get_all_students():
    """
    Get all students from the database.
    
    Returns a list of tuples containing student information.
    
    :return: List of student tuples (id, name, age, email)
    :rtype: list
    """
    db = sqlite3.connect('school.db')
    query = 'SELECT id, name, age, email FROM STUDENTS'
    cursor = db.cursor()
    students = cursor.execute(query).fetchall()
    db.close()
    return students


def delete_student(student_id):
    """
    Delete a student and their registrations.
    
    Removes the student from both STUDENTS and REGISTRATIONS tables.
    
    :param student_id: ID of student to delete
    :type student_id: str
    :return: True if deletion successful
    :rtype: bool
    """
    try:
        db = sqlite3.connect('school.db')
        cursor = db.cursor()
        
        # First delete registrations
        cursor.execute("DELETE FROM REGISTRATIONS WHERE STUDENT_ID = ?", (student_id,))
        
        # Then delete student
        cursor.execute("DELETE FROM STUDENTS WHERE ID = ?", (student_id,))
        db.commit()
        db.close()
        print(f"Student with ID {student_id} deleted successfully")
        return True
    except Exception as e:
        print(f'Error deleting student: {e}')
        return False


def update_student(student_id, updated_name, updated_age, updated_email):
    """
    Update an existing student's information.
    
    :param student_id: ID of student to update
    :type student_id: str
    :param updated_name: New name
    :type updated_name: str
    :param updated_age: New age
    :type updated_age: int
    :param updated_email: New email
    :type updated_email: str
    :return: True if update successful
    :rtype: bool
    """
    try:
        db = sqlite3.connect('school.db')
        query = "UPDATE STUDENTS SET NAME=?, AGE=?, EMAIL=? WHERE ID=?"
        cursor = db.cursor()
        cursor.execute(query, (updated_name, updated_age, updated_email, student_id))
        db.commit()
        db.close()
        print(f"Student with ID {student_id} updated successfully")
        return True
    except Exception as e:
        print(f'Error updating student: {e}')
        return False


def insert_instructor(instructor_id, name, age, email):
    """Insert a new instructor into the database."""
    try:
        db = sqlite3.connect('school.db')
        query = """
            INSERT INTO INSTRUCTORS(ID, NAME, AGE, EMAIL)
            VALUES (?,?,?,?)
        """
        cursor = db.cursor()
        cursor.execute(query, (instructor_id, name, age, email))
        db.commit()
        db.close()
        print(f'Instructor {name} inserted successfully')
        return True
    except sqlite3.IntegrityError:
        print(f'Instructor with ID {instructor_id} already exists')
        return False
    except Exception as e:
        print(f'Error inserting instructor: {e}')
        return False


def get_all_instructors():
    """Get all instructors from the database."""
    db = sqlite3.connect('school.db')
    query = 'SELECT id, name, age, email FROM INSTRUCTORS'
    cursor = db.cursor()
    instructors = cursor.execute(query).fetchall()
    db.close()
    return instructors


def delete_instructor(instructor_id):
    """Delete an instructor from the database."""
    try:
        db = sqlite3.connect('school.db')
        cursor = db.cursor()
        
        # Update courses to remove instructor
        cursor.execute("UPDATE COURSES SET INSTRUCTOR_ID=NULL WHERE INSTRUCTOR_ID = ?", (instructor_id,))
        
        # Delete instructor
        cursor.execute("DELETE FROM INSTRUCTORS WHERE ID = ?", (instructor_id,))
        db.commit()
        db.close()
        print(f"Instructor with ID {instructor_id} deleted successfully")
        return True
    except Exception as e:
        print(f'Error deleting instructor: {e}')
        return False


def update_instructor(instructor_id, updated_name, updated_age, updated_email):
    """Update an existing instructor's details."""
    try:
        db = sqlite3.connect('school.db')
        query = "UPDATE INSTRUCTORS SET NAME=?, AGE=?, EMAIL=? WHERE ID=?"
        cursor = db.cursor()
        cursor.execute(query, (updated_name, updated_age, updated_email, instructor_id))
        db.commit()
        db.close()
        print(f"Instructor with ID {instructor_id} updated successfully")
        return True
    except Exception as e:
        print(f'Error updating instructor: {e}')
        return False


def insert_course(course_id, name, instructor_id=None):
    """Insert a new course into the database."""
    try:
        db = sqlite3.connect('school.db')
        query = """
            INSERT INTO COURSES(ID, NAME, INSTRUCTOR_ID)
            VALUES (?,?,?)
        """
        cursor = db.cursor()
        cursor.execute(query, (course_id, name, instructor_id))
        db.commit()
        db.close()
        print(f'Course {name} inserted successfully')
        return True
    except sqlite3.IntegrityError:
        print(f'Course with ID {course_id} already exists')
        return False
    except Exception as e:
        print(f'Error inserting course: {e}')
        return False


def get_all_courses():
    """Get all courses with instructor information."""
    db = sqlite3.connect('school.db')
    query = '''
        SELECT c.id, c.name, c.instructor_id, i.name as instructor_name
        FROM COURSES c
        LEFT JOIN INSTRUCTORS i ON c.instructor_id = i.id
    '''
    cursor = db.cursor()
    courses = cursor.execute(query).fetchall()
    db.close()
    return courses


def delete_course(course_id):
    """Delete a course and its registrations."""
    try:
        db = sqlite3.connect('school.db')
        cursor = db.cursor()
        
        # First delete registrations
        cursor.execute("DELETE FROM REGISTRATIONS WHERE COURSE_ID = ?", (course_id,))
        
        # Then delete course
        cursor.execute("DELETE FROM COURSES WHERE ID = ?", (course_id,))
        db.commit()
        db.close()
        print(f"Course with ID {course_id} deleted successfully")
        return True
    except Exception as e:
        print(f'Error deleting course: {e}')
        return False


def update_course(course_id, updated_name, updated_instructor_id=None):
    """Update an existing course's details."""
    try:
        db = sqlite3.connect('school.db')
        query = "UPDATE COURSES SET NAME=?, INSTRUCTOR_ID=? WHERE ID=?"
        cursor = db.cursor()
        cursor.execute(query, (updated_name, updated_instructor_id, course_id))
        db.commit()
        db.close()
        print(f"Course with ID {course_id} updated successfully")
        return True
    except Exception as e:
        print(f'Error updating course: {e}')
        return False


def register_student_for_course(student_id, course_id):
    """
    Register a student for a course in the database.
    
    Creates the many-to-many relationship between students and courses.
    
    :param student_id: ID of the student
    :type student_id: str
    :param course_id: ID of the course
    :type course_id: str
    :return: True if registration successful
    :rtype: bool
    """
    try:
        db = sqlite3.connect('school.db')
        query = """
            INSERT INTO REGISTRATIONS(STUDENT_ID, COURSE_ID)
            VALUES (?,?)
        """
        cursor = db.cursor()
        cursor.execute(query, (student_id, course_id))
        db.commit()
        db.close()
        print(f'Student {student_id} registered for course {course_id}')
        return True
    except sqlite3.IntegrityError:
        print(f'Student {student_id} already registered for course {course_id}')
        return False
    except Exception as e:
        print(f'Error registering student: {e}')
        return False


def unregister_student_from_course(student_id, course_id):
    """Unregister a student from a course."""
    try:
        db = sqlite3.connect('school.db')
        query = "DELETE FROM REGISTRATIONS WHERE STUDENT_ID=? AND COURSE_ID=?"
        cursor = db.cursor()
        cursor.execute(query, (student_id, course_id))
        db.commit()
        db.close()
        print(f'Student {student_id} unregistered from course {course_id}')
        return True
    except Exception as e:
        print(f'Error unregistering student: {e}')
        return False


def get_student_courses(student_id):
    """
    Get all courses for a specific student.
    
    :param student_id: ID of the student
    :type student_id: str
    :return: List of course tuples (id, name)
    :rtype: list
    """
    db = sqlite3.connect('school.db')
    query = '''
        SELECT c.id, c.name
        FROM COURSES c
        JOIN REGISTRATIONS r ON c.id = r.course_id
        WHERE r.student_id = ?
    '''
    cursor = db.cursor()
    courses = cursor.execute(query, (student_id,)).fetchall()
    db.close()
    return courses


def get_course_students(course_id):
    """
    Get all students for a specific course.
    
    :param course_id: ID of the course
    :type course_id: str
    :return: List of student tuples (id, name)
    :rtype: list
    """
    db = sqlite3.connect('school.db')
    query = '''
        SELECT s.id, s.name
        FROM STUDENTS s
        JOIN REGISTRATIONS r ON s.id = r.student_id
        WHERE r.course_id = ?
    '''
    cursor = db.cursor()
    students = cursor.execute(query, (course_id,)).fetchall()
    db.close()
    return students


def search_students(search_term):
    """Search students by name, ID, or email."""
    db = sqlite3.connect('school.db')
    query = '''
        SELECT id, name, age, email FROM STUDENTS
        WHERE name LIKE ? OR id LIKE ? OR email LIKE ?
    '''
    cursor = db.cursor()
    students = cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')).fetchall()
    db.close()
    return students


def search_instructors(search_term):
    """Search instructors by name, ID, or email."""
    db = sqlite3.connect('school.db')
    query = '''
        SELECT id, name, age, email FROM INSTRUCTORS
        WHERE name LIKE ? OR id LIKE ? OR email LIKE ?
    '''
    cursor = db.cursor()
    instructors = cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')).fetchall()
    db.close()
    return instructors


def search_courses(search_term):
    """Search courses by name or ID."""
    db = sqlite3.connect('school.db')
    query = '''
        SELECT c.id, c.name, c.instructor_id, i.name as instructor_name
        FROM COURSES c
        LEFT JOIN INSTRUCTORS i ON c.instructor_id = i.id
        WHERE c.name LIKE ? OR c.id LIKE ?
    '''
    cursor = db.cursor()
    courses = cursor.execute(query, (f'%{search_term}%', f'%{search_term}%')).fetchall()
    db.close()
    return courses


def backup_database(backup_filename=None):
    """
    Create a backup of the database.
    
    Copies the current database to a backup file with timestamp.
    
    :param backup_filename: Custom backup filename, defaults to None
    :type backup_filename: str, optional
    :return: True if backup successful
    :rtype: bool
    """
    try:
        if not backup_filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"school_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2('school.db', backup_filename)
        print(f"Database backed up to {backup_filename}")
        return True
    except Exception as e:
        print(f"Error backing up database: {e}")
        return False


def get_database_statistics():
    """
    Get statistics about the database contents.
    
    Returns counts of students, instructors, courses, and registrations.
    
    :return: Dictionary with count statistics
    :rtype: dict
    """
    db = sqlite3.connect('school.db')
    cursor = db.cursor()
    
    # Count students
    cursor.execute('SELECT COUNT(*) FROM STUDENTS')
    student_count = cursor.fetchone()[0]
    
    # Count instructors
    cursor.execute('SELECT COUNT(*) FROM INSTRUCTORS')
    instructor_count = cursor.fetchone()[0]
    
    # Count courses
    cursor.execute('SELECT COUNT(*) FROM COURSES')
    course_count = cursor.fetchone()[0]
    
    # Count registrations
    cursor.execute('SELECT COUNT(*) FROM REGISTRATIONS')
    registration_count = cursor.fetchone()[0]
    
    db.close()
    
    return {
        'students': student_count,
        'instructors': instructor_count,
        'courses': course_count,
        'registrations': registration_count
    }

class DatabaseGUI:
    """
    Integration class for database operations with GUI.
    
    This class bridges the gap between the GUI classes and the database functions.
    I added this when I realized I needed to connect the GUI to the database.
    """
    
    def __init__(self):
        """Initialize database GUI and create tables."""
        create_tables()  # Initialize database
    
    def add_student_to_db(self, student):
        """Add a Student object to the database."""
        return insert_student(student.id, student.name, student.age, student._email)
    
    def add_instructor_to_db(self, instructor):
        """Add an Instructor object to the database."""
        return insert_instructor(instructor.id, instructor.name, instructor.age, instructor._email)
    
    def add_course_to_db(self, course):
        """Add a Course object to the database."""
        instructor_id = course.instructor.id if course.instructor else None
        return insert_course(course.id, course.name, instructor_id)
    
    def register_student_course_db(self, student, course):
        """Register a student for a course in the database."""
        return register_student_for_course(student.id, course.id)
    
    def load_all_from_db(self):
        """
        Load all data from database and return as objects.
        
        Reconstructs the object relationships from the database tables.
        This was the most complex part to get right.
        
        :return: Tuple of (students, instructors, courses) lists
        :rtype: tuple
        """
        students = []
        instructors = []
        courses = []
        
        # Load students
        for student_data in get_all_students():
            student = Student(student_data[1], student_data[2], student_data[3], student_data[0])
            students.append(student)
        
        # Load instructors
        for instructor_data in get_all_instructors():
            instructor = Instructor(instructor_data[1], instructor_data[2], instructor_data[3], instructor_data[0])
            instructors.append(instructor)
        
        # Load courses
        for course_data in get_all_courses():
            # Find instructor
            instructor = None
            if course_data[2]:  # instructor_id exists
                for inst in instructors:
                    if inst.id == course_data[2]:
                        instructor = inst
                        break
            
            course = Course(course_data[0], course_data[1], instructor)
            courses.append(course)
        
        # Load registrations
        db = sqlite3.connect('school.db')
        cursor = db.cursor()
        registrations = cursor.execute('SELECT student_id, course_id FROM REGISTRATIONS').fetchall()
        db.close()
        
        for student_id, course_id in registrations:
            # Find student and course objects
            student = next((s for s in students if s.id == student_id), None)
            course = next((c for c in courses if c.id == course_id), None)
            
            if student and course:
                student.register_course(course)
                course.add_student(student)
        
        return students, instructors, courses
