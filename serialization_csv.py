import csv
import os
from people import Student, Instructor, Course

def save_to_csv(students, instructors, courses, filename_prefix="school_data"):
    """
    Saves all the school data to CSV files.
    """
    # Save Students
    with open(f"{filename_prefix}_students.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Age", "Email"])
        for student in students:
            # Note: Accessing protected member _email for saving
            writer.writerow([student.id, student.name, student.age, student._email])

    # Save Instructors
    with open(f"{filename_prefix}_instructors.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Age", "Email"])
        for instructor in instructors:
            writer.writerow([instructor.id, instructor.name, instructor.age, instructor._email])

    # Save Courses
    with open(f"{filename_prefix}_courses.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "InstructorID"])
        for course in courses:
            instructor_id = course.instructor.id if course.instructor else None
            writer.writerow([course.id, course.name, instructor_id])
    
    # Save Registrations (for the many-to-many relationship)
    with open(f"{filename_prefix}_registrations.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["StudentID", "CourseID"])
        for student in students:
            for course in student.reg_courses:
                writer.writerow([student.id, course.id])


def load_from_csv(filename_prefix="school_data"):
    """
    Loads school data from CSV files and recreates objects and relationships.
    """
    # Load People (Students and Instructors)
    students = {}
    try:
        with open(f"{filename_prefix}_students.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students[row["ID"]] = Student(row["Name"], int(row["Age"]), row["Email"], row["ID"])
    except FileNotFoundError:
        pass

    instructors = {}
    try:
        with open(f"{filename_prefix}_instructors.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instructors[row["ID"]] = Instructor(row["Name"], int(row["Age"]), row["Email"], row["ID"])
    except FileNotFoundError:
        pass

    # Load Courses
    courses = {}
    try:
        with open(f"{filename_prefix}_courses.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instructor = instructors.get(row["InstructorID"])
                courses[row["ID"]] = Course(row["ID"], row["Name"], instructor)
    except FileNotFoundError:
        pass

    # Load Registrations and build relationships
    try:
        with open(f"{filename_prefix}_registrations.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                student = students.get(row["StudentID"])
                course = courses.get(row["CourseID"])
                if student and course:
                    student.register_course(course)
                    course.add_student(student)  # Add students to courses as well
    except FileNotFoundError:
        pass
    
    return list(students.values()), list(instructors.values()), list(courses.values())