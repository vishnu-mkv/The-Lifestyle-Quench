import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

export interface paginationConfig {
    current: number,
    count: number,
    resultSetSize: number
}

@Component({
    selector: 'app-pagination',
    templateUrl: './pagination.component.html',
    styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent implements OnInit {

    @Input() config: paginationConfig = {count: 0, current: 0, resultSetSize: 1};
    @Output() pageEmitter = new EventEmitter<number>();
    lastPage = 1;

    constructor() {
    }

    ngOnInit() {
    }

    getPageNumbers() {

        let pageNumbers: number[] = []

        let i = 1;
        this.lastPage = Math.ceil(this.config.count / this.config.resultSetSize);

        for (; i <= Math.min(this.lastPage, 3); i++) {
            pageNumbers.push(i);
        }

        if (i < this.config.current) pageNumbers.push(-1);

        i = Math.max(i, this.config.current);
        if (i === this.config.current) {
            pageNumbers.push(i);
            i++;
        }

        if (i + 2 < this.lastPage) pageNumbers.push(-1);

        i = Math.max(i, this.lastPage - 2);

        for (; i <= this.lastPage; i++) {
            pageNumbers.push(i);
        }

        return pageNumbers;
    }

}
