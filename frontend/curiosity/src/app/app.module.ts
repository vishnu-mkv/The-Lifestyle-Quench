import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HomeComponent} from './home/home.component';
import {NavbarComponent} from './navbar/navbar.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {HttpClientModule} from '@angular/common/http'
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {TokenInterceptor} from './auth.interceptor';
import {AuthService} from './auth.service';
import {Router} from '@angular/router';
import {FormsModule} from "@angular/forms";

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        NavbarComponent,
        LoginComponent,
        RegisterComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useFactory: function (auth: AuthService, router: Router) {
                return new TokenInterceptor(auth, router);
            },
            deps: [AuthService, Router],
            multi: true
        }
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
