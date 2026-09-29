using System;

namespace Week1_PartB_Exercises
{
    // TODO: Practice 2 - Create Student class. Decide what should be inherited from Person.
    // TODO: Practice 3 - Implement IPrintable interface.
    public class Student : Person
    {
        public int Grade { get; set; }
        public string StudentId { get; set; }
        public void PrintDetails(){
            Console.WriteLine($"Name: {Name}, Age: {Age}, Grade: {Grade}, StudentId: {StudentId}");
        }
    }
}
