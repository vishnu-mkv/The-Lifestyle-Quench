import {Injectable} from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class PopupService {

    private popups: any[] = [];

    constructor() {
    }

    add(popup: any) {
        this.popups.push(popup);
    }

    remove(id: string) {
        this.popups = this.popups.filter(x => x.id !== id);
    }

    open(id: string) {
        const popup = this.popups.find(x => x.id === id);
        popup.open();
    }

    close(id: string) {
        const popup = this.popups.find(x => x.id === id);
        popup.close();
    }
}
