import {Component, OnInit} from '@angular/core';
import {WriterApplicationResponse} from "../interfaces";
import {AuthService} from "../services/auth.service";
import {NgForm} from "@angular/forms";
import {MessageService} from "../services/message.service";
import {Router} from "@angular/router";

@Component({
    selector: 'app-writer-application',
    templateUrl: './writer-application.component.html',
    styleUrls: ['./writer-application.component.scss']
})
export class WriterApplicationComponent implements OnInit {

    application: WriterApplicationResponse | null = null;
    edit = false;
    originalData = {bio: "", writings: ""};
    data = {bio: "", writings: ""};

    constructor(private auth: AuthService, private message: MessageService,
                private router: Router) {
        auth.getActiveWriterApplication().subscribe(
            data => {
                if (data.application) {
                    this.edit = true;
                    this.data.bio = data.data.bio;
                    this.data.writings = data.data.writings;
                    this.originalData = Object.assign({}, this.data);
                }
            },
            err => message.showMessage("Failed to fetch application", "error")
        )
    }

    ngOnInit(): void {
    }

    updateChanges(form: NgForm) {
        if (!form.valid) return;
        this.auth.updateWriterApplication(this.data.bio, this.data.writings).subscribe(
            data => this.message.showMessage("Application updated. Wait for approval.", "success"),
            err => this.message.showMessage(err.error?.message, "error")
        )
        this.router.navigate(['profile'])
    }

    reset() {
        this.data = Object.assign({}, this.originalData);
    }

    apply(form: NgForm) {
        if (!form.valid) return;
        this.auth.createWriterApplication(this.data.bio, this.data.writings).subscribe(
            data => this.message.showMessage("Application posted. Wait for approval.", "success"),
            err => this.message.showMessage(err.error?.message, "error")
        )
        this.router.navigate(['profile'])
    }
}

