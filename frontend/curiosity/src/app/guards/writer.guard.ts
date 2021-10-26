import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree} from '@angular/router';
import {Observable} from 'rxjs';
import {AuthService} from "../services/auth.service";
import {map} from "rxjs/operators";

@Injectable({
    providedIn: 'root'
})
export class WriterGuard implements CanActivate {

    constructor(private auth: AuthService) {
    }


    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

        return this.auth.profileObserver().pipe(
            map(data => {
                return data.user.writer;
            })
        );
    }

}
