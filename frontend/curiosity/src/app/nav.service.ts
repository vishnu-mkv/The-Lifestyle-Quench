import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class NavService {

    showNavSubject = new BehaviorSubject(false);

    constructor() {
    }

    getShowNav() {
        return this.showNavSubject.asObservable();
    }

    showNav(val: boolean) {
        this.showNavSubject.next(val);
    }

    toggleNav() {
        let next = !this.showNavSubject.getValue();
        this.showNavSubject.next(next);
    }
}
