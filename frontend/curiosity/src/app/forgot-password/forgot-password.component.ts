import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {ActivatedRoute, Router} from "@angular/router";
import {NgForm} from "@angular/forms";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-forgot-password',
    templateUrl: './forgot-password.component.html',
    styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {

    hasKey: boolean = false;
    key = ""
    isAuthenticated: boolean;
    goodKey = false;
    user = "";
    error = "";
    emailSent = false;
    responseMessage = "";


    constructor(public auth: AuthService, private route: ActivatedRoute,
                private router: Router, private message: MessageService) {
        this.isAuthenticated = this.auth.isAuthenticated();
        route.queryParams.subscribe({
            next: params => {
                if (params?.key && !this.isAuthenticated) {
                    this.hasKey = true;
                    this.key = params.key;
                } else return;
                auth.getForgotPasswordKeyUser(params.key).subscribe(
                    data => {
                        console.log(data);
                        this.goodKey = true;
                        this.user = data.name;
                    },
                    err => {
                        message.showMessage(err.error.message, "error");
                    }
                )
                this.router.navigate([]);
            }
        })
    }

    ngOnInit(): void {
    }

    sendEmail(sendKeyForm: NgForm) {
        this.error = "";
        if (!sendKeyForm.valid) return;
        this.auth.sendForgotPasswordEmail(sendKeyForm.value.email).subscribe(
            data => {
                console.log(data);
                this.emailSent = data.success;
                this.responseMessage = data.message;
            },
            err => {
                this.error = err.error.message;
            }
        );
    }

    changePassword(changeForm: NgForm) {
        let values = changeForm.value;
        if (values.password !== values.cPassword) {
            this.error = "Passwords do not match";
            return;
        }
        this.auth.changePasswordWithKey(this.key, values.password).subscribe(
            data => {
                if (data.success) {
                    this.message.showMessage("Your password has been changed. You can login with new password", "success");
                    this.router.navigateByUrl('login');
                }
            },
            err => {
                this.error = err.error.message;
                console.log(err);
            }
        )
    }

    logout() {
        this.isAuthenticated = false;
        this.auth.logout(false);
    }
}
