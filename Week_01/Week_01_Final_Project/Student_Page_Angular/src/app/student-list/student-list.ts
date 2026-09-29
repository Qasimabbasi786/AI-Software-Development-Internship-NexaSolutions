import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-student-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './student-list.html',
  styleUrl: './student-list.css'
})
export class StudentList {
  @Input() searchText: string = '';
  @Output() studentSelect = new EventEmitter<any>();

  students = [
    { id: 1, name: 'Muhamamd Qasim', department: 'Computer Science', marks: 88, grade: 'A+' },
    { id: 2, name: 'Minahil', department: 'Artificial Intelligence', marks: 85, grade: 'A' },
    { id: 3, name: 'Asma', department: 'Computer Science', marks: 90, grade: 'A+' },
    { id: 4, name: 'Anoosha', department: 'Artificial Intelligence', marks: 82, grade: 'A-' },
    { id: 5, name: 'Azmat', department: 'Cyber Security', marks: 79, grade: 'B+' }
  ];

  get filteredStudents() {
    return this.students.filter(student =>
      student.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
      student.department.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  selectStudent(student: any) {
    this.studentSelect.emit(student);
  }
}