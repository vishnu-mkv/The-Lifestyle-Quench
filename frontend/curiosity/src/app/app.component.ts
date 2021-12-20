import {Component} from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";
import {NavService} from "./services/nav.service";
import {AuthService} from "./services/auth.service";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'curiosity';

    constructor(private router: Router, private nav: NavService, private auth: AuthService) {

        if (this.auth.isAuthenticated()) {
            auth.fetchProfile();
        }

        router.events.subscribe({
            next: event => {
                if (event instanceof NavigationEnd) {
                    this.nav.showNav(false);
                    this.nav.showDropdown(false);
                }
            }
        })
    }
}
