import {Component, OnInit} from '@angular/core';
import {AuthService} from '../services/auth.service'
import {Observable} from "rxjs";

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

    isAuthenticated: Observable<boolean>;
    loginError = false;
    error_msg: string[] = []

    constructor(public auth: AuthService) {
        this.isAuthenticated = this.auth.isLoggedIn();
    }

    ngOnInit(): void {
    }

    login(email: string, password: string) {
        this.auth.login(email, password).subscribe({
            error: err => {
                this.loginError = true;
                this.error_msg = err.error.non_field_errors;
                console.log(this.error_msg)
            }
        });
    }

    onSubmit(loginForm: any) {
        if (loginForm.valid) {
            this.login(loginForm.value.email, loginForm.value.password);
        }
    }
}
