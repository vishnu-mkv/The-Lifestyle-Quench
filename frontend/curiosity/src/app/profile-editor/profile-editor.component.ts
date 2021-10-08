import {Component, OnInit, ViewChild} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {Observable} from "rxjs";
import {Profile, updateProfile} from "../interfaces";
import {MatIconModule} from '@angular/material/icon';
import {PopupService} from "../popup";
import {EditInputBaseComponent} from "../edit-input-base/edit-input-base.component";
import {Router} from "@angular/router";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-profile-editor',
    templateUrl: './profile-editor.component.html',
    styleUrls: ['./profile-editor.component.scss'],
})
export class ProfileEditorComponent implements OnInit {

    @ViewChild('fName')
    fName!: EditInputBaseComponent;

    @ViewChild('lName')
    lName!: EditInputBaseComponent;

    profile: Observable<Profile>;
    updateInstance!: updateProfile;
    edit = {
        "profile_pic": false,
        "first_name": false,
        "last_name": false
    }
    firstName: any;
    lastName: any;

    constructor(public auth: AuthService, public popup: PopupService,
                private router: Router, private messages: MessageService) {
        this.profile = auth.getProfile();
        auth.getProfile().subscribe(
            data => {
                this.updateInstance = {
                    first_name: data.user.first_name,
                    last_name: data.user.last_name,
                    profile_pic: data.profile_pic
                };
                this.firstName = {
                    label: 'First Name',
                    id: 'fName',
                    value: this.updateInstance.first_name,
                    edit: this.updateInstance.first_name,
                    onEdit: false,
                };
                this.lastName = {
                    label: 'Last Name',
                    id: 'lName',
                    value: this.updateInstance.last_name,
                    edit: this.updateInstance.last_name,
                    onEdit: false,
                };

            }
        )
    }

    ngOnInit(): void {
    }

    updateProfile() {
        this.fName.save();
        this.lName.save();
        this.auth.updateProfile(this.firstName.value, this.lastName.value, this.updateInstance?.profile_pic).subscribe(
            data => {
                this.auth.fetchProfile();
                this.messages.showMessage("Profile updated.", "success");
                this.router.navigate(['profile']);
            },
            err => {
                this.messages.showMessage("Profile update failed.", "error");
                console.log(err);
            }
        );
    }

    imageUploaded(url: string) {
        this.edit.profile_pic = false;
        this.updateInstance.profile_pic = url;
        this.popup.close("profile-pic-upload");
    }
}
