import { Routes } from '@angular/router';
import { StudentListComponent } from './student-list/student-list.component';
import { RegistrationFormComponent } from './registration-form/registration-form.component';

export const routes: Routes = [
  { path: '', component: StudentListComponent },
  { path: 'register', component: RegistrationFormComponent }
];
