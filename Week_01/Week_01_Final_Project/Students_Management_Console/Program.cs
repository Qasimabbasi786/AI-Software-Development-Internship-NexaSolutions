using System;

namespace STUDENT_MANAGEMENT_CONSOLE
{
    class Program
    {
        static StudentManager manager = new StudentManager();

        static void Main(string[] args)
        {
            int choice = 0;

            do
            {
                Console.ForegroundColor = ConsoleColor.DarkCyan;
                Console.WriteLine("\n=========================================");
                Console.WriteLine("   STUDENT PORTAL & MANAGEMENT SYSTEM");
                Console.WriteLine("=========================================");
                Console.ResetColor();
                Console.WriteLine(" 1. Add New Student");
                Console.WriteLine(" 2. View All Students (Table View)");
                Console.WriteLine(" 3. Update Student Record");
                Console.WriteLine(" 4. Delete Student");
                Console.WriteLine(" 5. Search Student (Name/Dept)");
                Console.WriteLine(" 6. Sort Students by Performance");
                Console.WriteLine(" 7. View Analytics Dashboard (New!)");
                Console.WriteLine(" 8. Exit");

                try
                {
                    Console.Write("\nSelect an option (1-8): ");
                    choice = Convert.ToInt32(Console.ReadLine());

                    switch (choice)
                    {
                        case 1: AddStudent(); break;
                        case 2: manager.ViewStudents(); break;
                        case 3: UpdateStudent(); break;
                        case 4: DeleteStudent(); break;
                        case 5: SearchStudent(); break;
                        case 6: manager.SortByMarks(); break;
                        case 7: manager.ShowAnalytics(); break;
                        case 8: Console.WriteLine("Closing portal... Goodbye!"); break;
                        default: Console.WriteLine("Invalid option! Choose between 1-8."); break;
                    }
                }
                catch (FormatException)
                {
                    Console.WriteLine("Invalid input! Please enter a valid number.");
                }

            } while (choice != 8);
        }

        static void AddStudent()
        {
            try
            {
                Console.Write("Enter Student ID: ");
                int id = Convert.ToInt32(Console.ReadLine());

                Console.Write("Enter Full Name: ");
                string name = Console.ReadLine();

                Console.Write("Enter Department: ");
                string department = Console.ReadLine();

                Console.Write("Enter Marks (0-100): ");
                double marks = Convert.ToDouble(Console.ReadLine());

                manager.AddStudent(new Student(id, name, department, marks));
            }
            catch (FormatException)
            {
                Console.WriteLine("Formatting Error! Please check numerical inputs.");
            }
        }

        static void UpdateStudent()
        {
            try
            {
                Console.Write("Enter ID of student to update: ");
                int id = Convert.ToInt32(Console.ReadLine());

                Console.Write("Enter New Name: ");
                string name = Console.ReadLine();

                Console.Write("Enter New Department: ");
                string department = Console.ReadLine();

                Console.Write("Enter New Marks: ");
                double marks = Convert.ToDouble(Console.ReadLine());

                manager.UpdateStudent(id, name, department, marks);
            }
            catch (FormatException)
            {
                Console.WriteLine("Invalid input format.");
            }
        }

        static void DeleteStudent()
        {
            try
            {
                Console.Write("Enter Student ID to delete: ");
                int id = Convert.ToInt32(Console.ReadLine());
                manager.DeleteStudent(id);
            }
            catch (FormatException)
            {
                Console.WriteLine("Please enter a valid numeric ID.");
            }
        }

        static void SearchStudent()
        {
            Console.Write("Enter Name or Department to search: ");
            string keyword = Console.ReadLine();
            manager.SearchStudent(keyword);
        }
    }
}