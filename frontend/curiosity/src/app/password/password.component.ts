import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
    selector: 'app-password',
    templateUrl: './password.component.html',
    styleUrls: ['./password.component.scss']
})
export class PasswordComponent implements OnInit {

    @Input() submitted = false;
    password = "";
    cPassword = "";

    constructor() {
    }

    ngOnInit(): void {
    }

    getPassword(): string {
        return this.password;
    }

}
