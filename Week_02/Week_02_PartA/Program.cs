using System;
using System.Threading.Tasks;

namespace Week2_PartA_Exercises
{
    // Interface with enhanced definition
    public interface IAnimal
    {
        string Name { get; }
        string Speak();
    }

    public class Dog : IAnimal
    {
        public string Name => "German Shepherd";
        public string Speak() => "Woof! Woof!";
    }

    public class Cat : IAnimal
    {
        public string Name => "Persian Cat";
        public string Speak() => "Meow! Meow!";
    }

    class Program
    {
        static async Task Main(string[] args)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("========================================");
            Console.WriteLine("    WEEK 2 - PART A: ADVANCED C#        ");
            Console.WriteLine("========================================");
            Console.ResetColor();

            // 1. Generic Helper Method with custom styling
            Console.WriteLine("\n[1] Generic Swap Method Demonstration:");
            int num1 = 25, num2 = 50;
            Console.WriteLine($"-> Before Swap: num1 = {num1}, num2 = {num2}");
            Swap(ref num1, ref num2);
            Console.WriteLine($"-> After Swap:  num1 = {num1}, num2 = {num2}");

            string firstName = "Muhammad", lastName = "Qasim";
            Console.WriteLine($"-> Before Swap: {firstName} {lastName}");
            Swap(ref firstName, ref lastName);
            Console.WriteLine($"-> Swapped Names: {firstName} {lastName}");

            // 2. Interface Implementations
            Console.WriteLine("\n[2] Polymorphic Interface Implementations:");
            IAnimal myDog = new Dog();
            IAnimal myCat = new Cat();
            Console.WriteLine($"-> {myDog.Name} says: {myDog.Speak()}");
            Console.WriteLine($"-> {myCat.Name} says: {myCat.Speak()}");

            // 3. Async method with realistic delay & info
            Console.WriteLine("\n[3] Asynchronous Task Execution:");
            Console.WriteLine("-> Connecting to database and fetching records...");
            string responseData = await FetchDataAsync();
            Console.WriteLine($"-> Status: {responseData} (Timestamp: {DateTime.Now:T})");

            // 4. Clean Refactored Logic Execution
            Console.WriteLine("\n[4] Clean Architecture & Refactored Logic:");
            RunRefactoredLogic();
        }

        // Generic Swap Method
        public static void Swap<T>(ref T left, ref T right)
        {
            T temp = left;
            left = right;
            right = temp;
        }

        // Optimized Async Method
        public static async Task<string> FetchDataAsync()
        {
            await Task.Delay(1500); // Optimized delay
            return "Payload fetched and verified successfully!";
        }

        // Refactored Pipeline
        public static void RunRefactoredLogic()
        {
            string payload = GetSystemInput();
            ProcessSystemPayload(payload);
            FinalizeExecution();
        }

        private static string GetSystemInput()
        {
            return "Enterprise_Module_V2";
        }

        private static void ProcessSystemPayload(string input)
        {
            Console.WriteLine($"-> Processing module pipeline for: [{input}]");
        }

        private static void FinalizeExecution()
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("-> Pipeline Execution Completed Successfully!");
            Console.ResetColor();
        }
    }
}