import {Component, Input, OnInit} from '@angular/core';
import {postSummary} from "../interfaces";

@Component({
    selector: 'app-post-item',
    templateUrl: './post-item.component.html',
    styleUrls: ['./post-item.component.scss']
})
export class PostItemComponent implements OnInit {

    @Input() post!: postSummary;
    @Input() showWriter: boolean = true;
    @Input() summaryLength = 100;

    constructor() {
    }

    ngOnInit(): void {
        if (!this.post) return;
    }

    shortenString(str: string) {
        if (str.length <= this.summaryLength) return str;
        return str.substr(0, this.summaryLength) + '...';
    }
}
