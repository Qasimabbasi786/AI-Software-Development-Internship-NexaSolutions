import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentService } from '../student.service';
import { Student } from '../student.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-student-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './student-list.component.html',
  styleUrl: './student-list.component.css'
})
export class StudentListComponent implements OnInit {
  students$!: Observable<Student[]>;

  constructor(private studentService: StudentService) {}

  ngOnInit(): void {
    this.students$ = this.studentService.getStudents();
  }
}
