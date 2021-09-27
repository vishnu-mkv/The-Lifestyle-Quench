import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {apiURL} from "../environments/environment";
import {BehaviorSubject, Observable, ReplaySubject, throwError} from "rxjs";
import {share, tap} from "rxjs/operators";
import {Profile} from "./interfaces";
import {Router} from "@angular/router";

interface UserToken {
    token: string,
    expiresIn: number
}


@Injectable({
    providedIn: 'root'
})
export class AuthService {

    loginSubject = new BehaviorSubject<boolean>(this.isAuthenticated());
    source = this.loginSubject.asObservable();
    profileSubject = new ReplaySubject<Profile>();
    profileSource = this.profileSubject.asObservable();


    constructor(private http: HttpClient, private router: Router) {
        if (this.isAuthenticated()) {
            this.profileSubject.next(JSON.parse(localStorage.getItem('profile') as string));
        }
    }


    login(email: string, password: string) {
        return this.http.post<UserToken>(apiURL + 'api/users/login/', {email, password}).pipe(
            tap(data => {
                let t = new Date();
                t.setSeconds(t.getSeconds() + data.expiresIn);
                localStorage.setItem('token', data.token);
                localStorage.setItem('expiresAt', t.toUTCString());
                this.loginSubject.next(true);
                this.fetchProfile();
                this.router.navigateByUrl('/');
            })
        );
    }

    isLoggedIn() {
        return this.source.pipe(share());
    }

    logout(redirect = true) {
        localStorage.setItem('token', "");
        localStorage.setItem('expiresAt', "");
        localStorage.setItem('profile', "");
        this.loginSubject.next(false);
        redirect && this.router.navigateByUrl("/");
    }

    isAuthenticated(): boolean {

        let token = localStorage.getItem('token');
        let expiresAt = localStorage.getItem('expiresAt');
        if (!token || !expiresAt) return false;

        let expiresDate = new Date(expiresAt);
        let now = new Date(new Date().toUTCString());
        return now <= expiresDate;
    }

    getToken() {
        return localStorage.getItem('token');
    }

    fetchProfile() {
        this.http.get<Profile>(apiURL + 'api/users/profile').subscribe({
            next: data => {
                localStorage.setItem('profile', JSON.stringify(data));
                this.profileSubject.next(data as Profile);
            }
        });
    }

    getProfile(): Observable<Profile> {
        return this.profileSource.pipe(share());
    }

}

