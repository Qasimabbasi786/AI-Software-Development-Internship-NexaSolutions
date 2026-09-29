using System;

namespace Week1_PartB_Exercises
{
    // TODO: Practice 1 - Create a Person class with Name and Age properties.
    public class Person
    {
        public string Name { get; set; } 
        public int Age { get; set; }

        public void PrintDetails(){
            Console.WriteLine($"Name: {Name}, Age: {Age}");
        }
    }
}
