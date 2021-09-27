import {Component, ElementRef, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {AuthService} from "../auth.service";
import {NavService} from "../nav.service";
import {Profile} from "../interfaces";
import {Router} from "@angular/router";

@Component({
    selector: 'app-navbar',
    templateUrl: './navbar.component.html',
    styleUrls: ['./navbar.component.scss'],
    host: {
        '(document:click)': 'closeOnOutsideClick($event)',
    },
})
export class NavbarComponent implements OnInit {

    showNav: Observable<boolean>;
    showDropdown: boolean = false;
    isLoggedIn: Observable<boolean>;
    profile: Observable<Profile>;
    name = "";
    picUrl = "";

    constructor(private router: Router, private auth: AuthService,
                private nav: NavService, private _eref: ElementRef) {
        this.showNav = nav.getShowNav();
        this.isLoggedIn = auth.isLoggedIn();
        this.profile = auth.getProfile();
        this.profile.subscribe({
            next: value => {
                this.name = value?.user.first_name;
                this.picUrl = value?.profile_pic;
            }
        });
    }

    ngOnInit(): void {
    }

    toggleMenu() {
        this.nav.toggleNav();
    }

    logout() {
        this.auth.logout();
    }

    toggleDropDown() {
        this.showDropdown = !this.showDropdown;
    }

    closeOnOutsideClick(event: any) {
        if (!this._eref.nativeElement.querySelector('#acc-view')?.contains(event.target)) // or some similar check
            this.showDropdown = false;
    }
}
