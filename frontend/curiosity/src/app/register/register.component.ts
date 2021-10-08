import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {Observable} from "rxjs";

@Component({
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

    emailAvailable = true;
    registerSuccess = false;
    email = ""
    isAuthenticated: Observable<boolean>;
    errors: string[] = [];

    constructor(public auth: AuthService) {
        this.isAuthenticated = auth.isLoggedIn();
    }

    ngOnInit(): void {
    }

    checkEmail(email: any) {
        if (email.invalid) {
            this.emailAvailable = true;
            return;
        }
        this.auth.checkEmailAvailability(email.value).subscribe({
            next: data => {
                this.emailAvailable = data.availability;
                console.log(data);
            }
        })
    }

    register(form: any) {
        this.errors = [];
        if (form.invalid || !this.emailAvailable) return;
        let values = form.value;
        if (values?.password != values?.cPassword) {
            this.errors.push("Passwords do not match");
            return;
        }
        this.auth.register({
            first_name: values.fName,
            last_name: values.lName,
            email: values.email,
            password: values.password
        }).subscribe(
            data => {
                this.registerSuccess = data.success;
                this.email = data.email;
            },
            err => console.log(err)
        )
    }
}
