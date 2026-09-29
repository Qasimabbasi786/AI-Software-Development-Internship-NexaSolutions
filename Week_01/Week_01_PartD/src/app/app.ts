import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Student } from './student.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: '../styles.css'
})
export class App {
  userName = 'Muhammad Qasim';
  internshipTitle = 'AI Software Engineer Intern';

  selectedStudent: Student | null = null;

  students: Student[] = [
    { id: 1, name: 'Muhamamd Qasim', department: 'Computer Science', grade: 'A', email: 'qasim@example.com', imageUrl: 'https://images.unsplash.com/photo-1772371272141-0fbd644b65c4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fG1hbiUyMHByb2Zlc3Npb25hbCUyMEF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D' },
    { id: 2, name: 'Minahil', department: 'Artificial Intelligence', grade: 'A', email: 'minahil@example.com', imageUrl: 'https://plus.unsplash.com/premium_photo-1739786995552-0a2ccfa62ba5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d29tZW4lMjBwcm9mZXNzaW9uYWwlMjBBdmF0YXJ8ZW58MHx8MHx8fDA%3D' },
    { id: 3, name: 'Asma', department: 'Computer Science', grade: 'A-', email: 'asma@example.com', imageUrl: 'https://plus.unsplash.com/premium_photo-1739786996040-32bde1db0610?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8d29tZW4lMjBwcm9mZXNzaW9uYWwlMjBBdmF0YXJ8ZW58MHx8MHx8fDA%3D' },
    { id: 4, name: 'Anoosha', department: 'Artificial Intelligence', grade: 'A-', email: 'anoosha@example.com', imageUrl: 'https://plus.unsplash.com/premium_photo-1738822251828-2307c272d036?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fHdvbWVuJTIwcHJvZmVzc2lvbmFsJTIwQXZhdGFyfGVufDB8fDB8fHww' },
    { id: 5, name: 'Azmat', department: 'Cyber Security', grade: 'B+', email: 'azmat@example.com', imageUrl: 'https://images.unsplash.com/photo-1740252117013-4fb21771e7ca?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWFuJTIwcHJvZmVzc2lvbmFsJTIwQXZhdGFyfGVufDB8fDB8fHww' }
  ];

  selectStudent(student: Student) {
    this.selectedStudent = student;
  }
}
