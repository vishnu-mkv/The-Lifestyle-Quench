import {Component, ElementRef, Input, OnInit, ViewEncapsulation} from '@angular/core';
import {PopupService} from "./popup.service";

@Component({
    selector: 'popup',
    templateUrl: './popup.component.html',
    styleUrls: ['./popup.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class PopupComponent implements OnInit {

    @Input() id: string = '';
    private element: any;

    constructor(private popupService: PopupService, private el: ElementRef) {
        this.element = el.nativeElement;
    }

    ngOnInit(): void {
        if (!this.id) {
            console.error("Popup must have an id");
            return;
        }

        document.body.appendChild(this.element);

        this.element.addEventListener('click', (event: any) => {
            if (event.target.className === 'popup') this.close();
        });

        this.popupService.add(this);
    }

    ngOnDestroy(): void {
        this.popupService.remove(this.id);
        this.element.remove();
    }

    open(): void {
        this.element.style.display = 'flex';
        document.body.classList.add('popup-open');
    }

    close(): void {
        this.element.style.display = 'none';
        document.body.classList.remove('popup-open');
    }
}
