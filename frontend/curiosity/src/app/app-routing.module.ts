import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {ActivateAccountComponent} from "./activate-account/activate-account.component";
import {ProfileComponent} from "./profile/profile.component";
import {AuthGuardService} from "./services/auth-guard.service";
import {PageNotFoundComponent} from "./page-not-found/page-not-found.component";
import {ForgotPasswordComponent} from "./forgot-password/forgot-password.component";
import {ChangePasswordComponent} from "./change-password/change-password.component";
import {ProfileEditorComponent} from "./profile-editor/profile-editor.component";

const routes: Routes = [
    {
        path: 'profile/change-password',
        component: ChangePasswordComponent,
        canActivate: [AuthGuardService]
    },
    {
        path: 'profile/edit',
        component: ProfileEditorComponent,
        canActivate: [AuthGuardService]
    },
    {
        path: 'profile',
        component: ProfileComponent,
        canActivate: [AuthGuardService]
    },
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'register/activate',
        component: ActivateAccountComponent
    },
    {
        path: 'users/forgot-password',
        component: ForgotPasswordComponent
    },
    {
        path: 'register',
        component: RegisterComponent
    },
    {
        path: '',
        component: HomeComponent
    },
    {
        path: '**',
        component: PageNotFoundComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes, {onSameUrlNavigation: 'reload'})],
    exports: [RouterModule]
})
export class AppRoutingModule { }
