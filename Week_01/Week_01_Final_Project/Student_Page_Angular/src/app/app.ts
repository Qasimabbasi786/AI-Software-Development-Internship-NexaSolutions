import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { StudentList } from './student-list/student-list';
import { StudentDetails } from './student-details/student-details';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, StudentList, StudentDetails],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  searchText: string = '';
  selectedStudent: any = null;

  onStudentSelect(student: any) {
    this.selectedStudent = student;
  }
}