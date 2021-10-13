import {Component, Input, OnInit} from '@angular/core';
import {editInput, InputEdit} from "../interfaces";

@Component({
    selector: 'app-edit-input-base',
    templateUrl: './edit-input-base.component.html',
    styleUrls: ['./edit-input-base.component.scss']
})
export class EditInputBaseComponent implements OnInit {

    @Input() props: InputEdit = new editInput();

    original: string = "";
    edit: string = "";

    constructor() {
    }

    ngOnInit(): void {
        if (!this.props) {
            return;
        }
        this.original = this.props.value;
    }

    reset(): void {
        this.props.value = this.original;
    }

    save(): void {
        if (this.props.onEdit) {
            this.props.onEdit = false;
            this.props.value = this.edit;
        }
    }
}
