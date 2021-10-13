import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {apiURL} from "../../environments/environment";
import {BehaviorSubject, Observable, ReplaySubject} from "rxjs";
import {share, tap} from "rxjs/operators";
import {Profile, userRegistration, WriterApplicationResponse, writerProfile} from "../interfaces";
import {Router} from "@angular/router";
import {writerApplicationPending} from '../interfaces';

interface UserToken {
    token: string,
    expiresIn: number
}

interface emailAvailable {
    email: string,
    availability: boolean,
    message?: string
}

interface registerReply {
    success: boolean,
    email: string,
    errors?: any
}

interface keyActivate {
    user: string,
    status: boolean,
    message: string
}

interface activationReply {
    message: string
}

interface forgotPasswordUser {
    name: string,
    email: string
}

interface forgotPasswordSendEmail {
    success: boolean,
    message: string
}

interface forgotPasswordChange {
    success: boolean,
    email: string
}

interface changePassword {
    success: boolean,
    message: string
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    loginSubject = new BehaviorSubject<boolean>(this.isAuthenticated());
    source = this.loginSubject.asObservable();
    profileSubject = new ReplaySubject<Profile>();
    profileSource = this.profileSubject.asObservable();
    writerSubject = new ReplaySubject<writerProfile>();
    writerSource = this.writerSubject.asObservable();


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
        localStorage.setItem('writer', "");
        this.loginSubject.next(false);
        this.profileSubject.next({
            profile_pic: "",
            user: {
                first_name: "",
                last_name: "",
                writer: false,
                admin: false,
                staff: false,
                active: false,
                date_created: "",
                email: ""
            }
        });
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
        this.http.get<Profile>(apiURL + 'api/users/profile/').subscribe({
            next: data => {
                localStorage.setItem('profile', JSON.stringify(data));
                this.profileSubject.next(data as Profile);
                if (data.user.writer) this.fetchWriterProfile();
            }
        });
    }

    getProfile(): Observable<Profile> {
        return this.profileSource.pipe(share());
    }

    checkEmailAvailability(email: string) {
        return this.http.post<emailAvailable>(apiURL + 'check-availability/email/', {email});
    }

    register(user: userRegistration) {
        return this.http.post<registerReply>(apiURL + 'api/users/register/', user);
    }

    activateUser(key: string) {
        return this.http.post<keyActivate>(apiURL + 'api/users/activate/', {key});
    }

    sendActivation(email: string) {
        return this.http.post<activationReply>(apiURL + 'api/users/resend-activation/', {email});
    }

    getWriterProfile() {
        return this.writerSource.pipe(share());
    }

    private fetchWriterProfile() {
        return this.http.get<writerProfile>(apiURL + 'api/users/writer-profile/').subscribe(
            data => {
                localStorage.setItem('writer', JSON.stringify(data));
                this.writerSubject.next(data)
            },
            err => console.log(err)
        );
    }

    getForgotPasswordKeyUser(key: string) {
        return this.http.post<forgotPasswordUser>(apiURL + 'api/users/forgot-password/get-user/', {key});
    }

    sendForgotPasswordEmail(email: string) {
        return this.http.post<forgotPasswordSendEmail>(apiURL + 'api/users/forgot-password/send-email/', {email});
    }

    changePasswordWithKey(key: string, password: string) {
        return this.http.post<forgotPasswordChange>(apiURL + 'api/users/forgot-password/change-password/', {
            key,
            new_password: password
        });
    }

    changePassword(email: string, password: string, new_password: string) {
        return this.http.post<changePassword>(apiURL + 'api/users/change-password/', {email, password, new_password});
    }

    updateProfile(first_name: string, last_name: string, profile_pic: string) {
        return this.http.patch(apiURL + 'api/users/profile/', {first_name, last_name, profile_pic});
    }

    checkActiveWriterApplication() {
        return this.http.get<{ 'application': boolean }>(apiURL + 'api/users/apply/pending/');
    }

    getActiveWriterApplication() {
        return this.http.get<writerApplicationPending>(apiURL + 'api/users/apply/');
    }

    updateWriterApplication(bio: string, writings: string) {
        return this.http.patch(apiURL + 'api/users/apply/', {bio, writings});
    }

    createWriterApplication(bio: string, writings: string) {
        return this.http.post(apiURL + 'api/users/apply/', {bio, writings});
    }

    getWriterApplicationHistory() {
        return this.http.get<WriterApplicationResponse[]>(apiURL + 'api/users/apply/history/');
    }
}

