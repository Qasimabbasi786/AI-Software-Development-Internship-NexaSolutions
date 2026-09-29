using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;



namespace STUDENT_MANAGEMENT_CONSOLE
{
    public class StudentManager
    {
        private List<Student> students = new List<Student>();

        // Add Student
        public void AddStudent(Student student)
        {
            if (students.Any(s => s.Id == student.Id))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("[Error] A student with this ID already exists!");
                Console.ResetColor();
                return;
            }

            students.Add(student);
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("[Success] Student registered successfully!");
            Console.ResetColor();
        }

        // View Students
        public void ViewStudents()
        {
            if (students.Count == 0)
            {
                Console.WriteLine("No student records available.");
                return;
            }

            Console.WriteLine("\n-------------------------------------------------------------------------");
            Console.WriteLine($"{"ID",-5} | {"Name",-18} | {"Department",-18} | {"Marks",-7} | {"Grade",-5}");
            Console.WriteLine("-------------------------------------------------------------------------");

            foreach (var s in students.OrderBy(s => s.Id))
            {
                Console.WriteLine($"{s.Id,-5} | {s.Name,-18} | {s.Department,-18} | {s.Marks,-7} | {s.Grade,-5}");
            }
            Console.WriteLine("-------------------------------------------------------------------------");
        }

        // Search Student
        public void SearchStudent(string keyword)
        {
            var result = students
                .Where(s => s.Name.Equals(keyword, StringComparison.OrdinalIgnoreCase) || 
                            s.Department.Equals(keyword, StringComparison.OrdinalIgnoreCase))
                .ToList();

            if (result.Count == 0)
            {
                Console.WriteLine("No matching students found.");
                return;
            }

            Console.WriteLine($"\n[Found {result.Count} record(s)]");
            foreach (var s in result)
            {
                Console.WriteLine($"ID: {s.Id} | Name: {s.Name} | Dept: {s.Department} | Marks: {s.Marks} | Grade: {s.Grade}");
            }
        }

        // Update Student
        public void UpdateStudent(int id, string name, string department, double marks)
        {
            var student = students.FirstOrDefault(s => s.Id == id);
            if (student == null)
            {
                Console.WriteLine("Student ID not found.");
                return;
            }

            student.Name = name;
            student.Department = department;
            student.Marks = marks;

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("[Updated] Student record modified successfully!");
            Console.ResetColor();
        }

        // Delete Student
        public void DeleteStudent(int id)
        {
            var student = students.FirstOrDefault(s => s.Id == id);
            if (student == null)
            {
                Console.WriteLine("Student ID not found.");
                return;
            }

            students.Remove(student);
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("[Deleted] Student record removed.");
            Console.ResetColor();
        }

        // Sort Students by Marks
        public void SortByMarks()
        {
            if (students.Count == 0) { Console.WriteLine("No records to sort."); return; }

            var sorted = students.OrderByDescending(s => s.Marks).ToList();
            Console.WriteLine("\n--- Students Sorted by Highest Marks ---");
            foreach (var s in sorted)
            {
                Console.WriteLine($"Name: {s.Name,-15} | Marks: {s.Marks,-5} | Grade: {s.Grade}");
            }
        }


        // Analytics Dashboard
        public void ShowAnalytics()
        {
            if (students.Count == 0)
            {
                Console.WriteLine("No data available for analytics.");
                return;
            }

            double avgMarks = students.Average(s => s.Marks);
            var topStudent = students.OrderByDescending(s => s.Marks).First();
            var lowStudent = students.OrderBy(s => s.Marks).First();

            Console.WriteLine("\n====== ACADEMIC ANALYTICS DASHBOARD ======");
            Console.WriteLine($" Total Students : {students.Count}");
            Console.WriteLine($" Average Marks  : {avgMarks:F2}");
            Console.WriteLine($" Top Performer  : {topStudent.Name} ({topStudent.Marks} Marks)");
            Console.WriteLine($" Needs Attention: {lowStudent.Name} ({lowStudent.Marks} Marks)");
            Console.WriteLine("==========================================");
        }
    }
}