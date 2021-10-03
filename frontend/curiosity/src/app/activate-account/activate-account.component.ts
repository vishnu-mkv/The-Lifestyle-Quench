import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {ActivatedRoute, Router} from "@angular/router";
import {NgForm} from "@angular/forms";

@Component({
    selector: 'app-activate-account',
    templateUrl: './activate-account.component.html',
    styleUrls: ['./activate-account.component.scss']
})
export class ActivateAccountComponent implements OnInit {

    hasKey: boolean = false;
    activationSuccess = false;
    isAuthenticated: boolean;
    sendSuccess = true;
    user = "";
    seconds = 0;
    errorMessage = "";
    message = "";

    constructor(private auth: AuthService, private route: ActivatedRoute, private router: Router) {
        this.isAuthenticated = this.auth.isAuthenticated();
        route.queryParams.subscribe({
            next: params => {
                if (params?.key && !this.isAuthenticated) this.hasKey = true;
                else return;
                this.auth.activateUser(params.key).subscribe(
                    data => {
                        this.activationSuccess = data.status;
                        if (data.user) this.user = data.user;
                        this.seconds = 3;
                        let timer = setInterval(() => {
                            this.seconds--;
                            if (this.seconds == 0) {
                                clearInterval(timer);
                                this.router.navigateByUrl('/login');
                            }
                        }, 1000);
                    },
                    err => {
                        if (err.error.user) {
                            this.errorMessage = `Your account ${err.error.user} is already active.`
                        } else this.errorMessage = err.error.message;
                    }
                )
            }
        })
    }

    ngOnInit(): void {
    }

    sendActivation(activationForm: NgForm) {
        this.hasKey = false;
        if (activationForm.invalid) return;
        this.sendSuccess = true;
        this.auth.sendActivation(activationForm.value.email).subscribe(
            data => {
                this.message = data.message
            },
            err => {
                this.sendSuccess = false;
                this.errorMessage = err.error.message;
            }
        );
    }
}
