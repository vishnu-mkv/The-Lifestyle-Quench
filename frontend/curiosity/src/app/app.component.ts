import {Component} from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";
import {NavService} from "./services/nav.service";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'curiosity';

    constructor(private router: Router, private nav: NavService) {

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
