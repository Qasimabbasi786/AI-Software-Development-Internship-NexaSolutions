using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace STUDENT_MANAGEMENT_CONSOLE
{
    public class Student
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public double Marks { get; set; }

        public string Grade => Marks switch
        {
            >= 85 => "A+",
            >= 75 => "A",
            >= 65 => "B",
            >= 50 => "C",
            _ => "F"
        };

        public Student(int id, string name, string department, double marks)
        {
            Id = id;
            Name = name;
            Department = department;
            Marks = marks;
        }
    }
}
