import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class NavService {

    showNavSubject = new BehaviorSubject(false);
    showDropdownSubject = new BehaviorSubject(false);

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

    getShowDropdown() {
        return this.showDropdownSubject.asObservable();
    }

    showDropdown(val: boolean) {
        this.showDropdownSubject.next(val);
    }

    toggleDropdown() {
        let next = !this.showDropdownSubject.getValue();
        this.showDropdownSubject.next(next);
    }
}
