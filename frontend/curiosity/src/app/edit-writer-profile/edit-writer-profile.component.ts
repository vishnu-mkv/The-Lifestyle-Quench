import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {writerProfile} from "../interfaces";
import {NgForm} from "@angular/forms";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-edit-writer-profile',
    templateUrl: './edit-writer-profile.component.html',
    styleUrls: ['./edit-writer-profile.component.scss']
})
export class EditWriterProfileComponent implements OnInit {

    originalData: writerProfile = {writer_name: '', bio: ''};
    data: writerProfile = {writer_name: '', bio: ''};
    idAvailable: boolean = true;
    invalidWriterName: boolean = false;

    constructor(private auth: AuthService, private messages: MessageService) {
        this.auth.getWriterProfile().subscribe(
            data => {
                this.data = data;
                Object.assign(this.originalData, data);
            },
            error => console.log(error)
        )
    }

    ngOnInit(): void {
    }

    reset() {
        Object.assign(this.data, this.originalData);
    }

    checkWriterNameAvailability(updateForm: NgForm) {
        let name = updateForm.value.writer_name;
        if (name.length < 6) return;
        if (!(/^[a-zA-z/-]{6,}$/.test(name))) {
            this.invalidWriterName = true;
            return;
        } else this.invalidWriterName = false;
        this.auth.checkWriterNameAvailability(name).subscribe(
            data => this.idAvailable = data.availability,
            err => console.log(err)
        )

    }

    updateWriterProfile(updateForm: NgForm) {
        if (updateForm.invalid || !this.idAvailable || this.invalidWriterName) return;
        this.auth.updateWriterProfile(updateForm.value, this.originalData.writer_name).subscribe(
            data => {
                this.originalData = data;
                Object.assign(this.data, data);
                this.messages.showMessage("Profile updated successfully!", 'success');
            },
            err => {
                console.log(err);
                this.messages.showMessage("Something went wrong. Couldn't update profile", 'error');
            }
        )
    }
}
