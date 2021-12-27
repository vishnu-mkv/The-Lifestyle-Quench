import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'app-card',
    templateUrl: './card.component.html',
    styleUrls: ['./card.component.scss']
})
export class CardComponent implements OnInit {

    @Input() src = "";
    @Input() title = "";
    @Input() desc = "";
    @Input() alt = "";
    @Input() link="";

    constructor() { }

    ngOnInit(): void {
    }

}
