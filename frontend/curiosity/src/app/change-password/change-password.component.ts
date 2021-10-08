import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {NgForm} from "@angular/forms";
import {MessageService} from "../services/message.service";
import {Router} from "@angular/router";

@Component({
    selector: 'app-change-password',
    templateUrl: './change-password.component.html',
    styleUrls: ['./change-password.component.scss']
})
export class ChangePasswordComponent implements OnInit {

    email = "";
    errorMsg: string[] = [];

    constructor(private auth: AuthService, private messageService: MessageService,
                private router: Router) {
        this.auth.getProfile().subscribe(
            data => this.email = data.user.email
        );
    }

    ngOnInit(): void {
    }

    changePassword(changeForm: NgForm) {
        this.errorMsg = [];
        if (changeForm.invalid) return;
        if (changeForm.value.cPassword !== changeForm.value.password) {
            this.errorMsg = ["Passwords do not match"];
            return;
        }
        this.auth.changePassword(this.email, changeForm.value.oldPassword, changeForm.value.password).subscribe(
            data => {
                if (data.success) {
                    this.messageService.showMessage(data.message, "success");
                    this.router.navigateByUrl('/profile');
                }
            },
            err => {
                for (let field in err.error) {
                    this.errorMsg.push(...err.error[field]);
                }
            }
        )
    }
}
