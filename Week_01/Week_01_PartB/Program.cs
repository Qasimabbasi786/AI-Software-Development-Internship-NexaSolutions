using System;

namespace Week1_PartB_Exercises
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Week 1 - Part B  ===");
            
            Student s1 = new Student();
            s1.Name = "Muhammad Qasim";
            s1.Age = 23;
            s1.Grade = 85;
            s1.StudentId = "0092";
            s1.PrintDetails();
            
            Console.WriteLine("Try creating a Person, Student, and Teacher object!");
        }
    }
}
