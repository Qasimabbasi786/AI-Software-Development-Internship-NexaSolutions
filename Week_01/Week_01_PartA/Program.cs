using System;
using System.Linq;

namespace Week1_PartA_Exercises
{
    class Program
    {
        static void Main(string[] args)
        {
            bool exit = false;
            while (!exit)
            {
                Console.WriteLine("\n=== Week 1 - Part A ===");
                Console.WriteLine("1. Calculator");
                Console.WriteLine("2. Even or Odd");
                Console.WriteLine("3. FizzBuzz");
                Console.WriteLine("4. Marks to Grade");
                Console.WriteLine("5. Array Min/Max");
                Console.WriteLine("6. Exit");
                Console.Write("Select an option (1-6): ");
                
                string choice = Console.ReadLine();
                Console.WriteLine();

                switch (choice)
                {
                    case "1":
                        Calculator();
                        break;
                    case "2":
                        EvenOrOdd();
                        break;
                    case "3":
                        FizzBuzz();
                        break;
                    case "4":
                        MarksToGrade();
                        break;
                    case "5":
                        ArrayMinMax();
                        break;
                    case "6":
                        exit = true;
                        Console.WriteLine("I am going to exit from menu...!");
                        break;
                    default:
                        Console.WriteLine("Invalid option. Please enter a number between 1 to 6.");
                        break;
                }
            }
        }
        
        static void Calculator()
        {
            Console.WriteLine("--- Calculator ---");
            Console.Write("Enter first number: ");
            if (!double.TryParse(Console.ReadLine(), out double num1))
            {
                Console.WriteLine("Invalid input. Please enter a valid number.");
                return;
            }

            Console.Write("Enter second number: ");
            if (!double.TryParse(Console.ReadLine(), out double num2))
            {
                Console.WriteLine("Invalid input. Please enter a valid number.");
                return;
            }

            Console.WriteLine($"Addition: {num1 + num2}");
            Console.WriteLine($"Subtraction: {num1 - num2}");
            Console.WriteLine($"Multiplication: {num1 * num2}");
            
            if (num2 != 0)
                Console.WriteLine($"Devision: {num1 / num2}");
            else
                Console.WriteLine("Devision: Cannot divide by zero.");
        }

        static void EvenOrOdd()
        {
            Console.WriteLine("--- Even Number or Odd Number ---");
            Console.WriteLine("Enter a number");
            int input = int.Parse(Console.ReadLine());
            if (input % 2 == 0)
                Console.WriteLine($"{input} is Even Number");
            else
                Console.WriteLine($"{input} is Odd Number");
        }

        static void FizzBuzz()
        {
            Console.WriteLine("--- FizzBuzz ---");
            for (int i = 1; i <= 100; i++)
            {
                if (i % 3 == 0 && i % 5 == 0)
                    Console.WriteLine("FizzBuzz");
                else if (i % 3 == 0)
                    Console.WriteLine("Fizz");
                else if (i % 5 == 0)
                    Console.WriteLine("Buzz");
                else
                    Console.WriteLine(i);
            }
        }

        static void MarksToGrade()
        {
            Console.WriteLine("--- Marks to Grade ---");
            Console.Write("Enter your marks: ");
            int marks = int.Parse(Console.ReadLine());
            if (marks >= 85 && marks <= 100){
                Console.WriteLine("A");
            }
            else if (marks >= 80 && marks < 85){
                Console.WriteLine("A-");
            }            
            else if (marks >= 75 && marks < 80){
                Console.WriteLine("B+");
            }
            else if (marks >= 70 && marks < 75){
                Console.WriteLine("B-");
            }
            else if (marks >= 65 && marks < 70){
                Console.WriteLine("C+");
            }
            else if (marks >= 60 && marks < 65){
                Console.WriteLine("C-");
            }
            else if (marks >= 55 && marks < 60){
                Console.WriteLine("D+");
            }
            else if (marks >= 50 && marks < 55){
                Console.WriteLine("D-");
            }
            else {
                Console.WriteLine("F");
            }
        }

        static void ArrayMinMax()
        {
            Console.WriteLine("--- Array Min/Max ---");
            int[] array={2,5,4,11,78,13,5,1,9,0};
            int min = array[0];
            int max = array[0];
            for (int i=0; i<10; i++){
                if (array[i]<min)
                    min=array[i];
                if (array[i]>max)
                    max=array[i];

            }
            Console.WriteLine($"Smallest value: {min}");
            Console.WriteLine($"Largest value: {max}");
        }
    }
}
