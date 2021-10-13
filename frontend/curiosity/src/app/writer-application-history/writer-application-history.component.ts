import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {WriterApplicationResponse} from "../interfaces";
import {PopupService} from "../popup";

@Component({
    selector: 'app-writer-application-history',
    templateUrl: './writer-application-history.component.html',
    styleUrls: ['./writer-application-history.component.scss']
})
export class WriterApplicationHistoryComponent implements OnInit {

    data: WriterApplicationResponse[] = [];
    bio = "";
    writings = "";

    constructor(private auth: AuthService, public popup: PopupService) {
        auth.getWriterApplicationHistory().subscribe(
            data => this.data = data,
            err => console.log(err)
        );
    }

    ngOnInit(): void {
    }

}
