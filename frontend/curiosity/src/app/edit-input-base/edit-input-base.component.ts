import {Component, Input, OnInit} from '@angular/core';
import {InputEdit} from "../interfaces";

@Component({
    selector: 'app-edit-input-base',
    templateUrl: './edit-input-base.component.html',
    styleUrls: ['./edit-input-base.component.scss']
})
export class EditInputBaseComponent implements OnInit {

    @Input() props: InputEdit = {label: "", id: "", value: "", onEdit: false};

    original: string;
    edit: string = "";

    constructor() {
        this.original = this.props.value;
    }

    ngOnInit(): void {
        if (!this.props) {
            return;
        }
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
