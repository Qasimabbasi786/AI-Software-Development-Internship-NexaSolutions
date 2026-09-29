using System;

namespace Week1_PartB_Exercises
{
    // TODO: Practice 2 - Create Teacher class. Decide what should be inherited from Person.
    // TODO: Practice 3 - Implement IPrintable interface.
    public class Teacher : Person
    {
        public string Subject { get; set; }

        public void PrintDetails(){
            Console.WriteLine($"Name: {Name}, Age: {Age}, Subject: {Subject}");
        }
        // Add properties specific to a Teacher, like Subject
    }
}
