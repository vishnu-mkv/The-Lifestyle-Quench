import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {AppRoutingModule} from './app-routing.module';
import {QuillModule} from "ngx-quill";
import {Router} from '@angular/router';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from '@angular/common/http'
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatIconModule} from '@angular/material/icon';
import {HashLocationStrategy, LocationStrategy, PathLocationStrategy} from '@angular/common';

import {AppComponent} from './app.component';
import {HomeComponent} from './home/home.component';
import {NavbarComponent} from './navbar/navbar.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {TokenInterceptor} from './auth.interceptor';
import {AuthService} from './services/auth.service';
import {ActivateAccountComponent} from './activate-account/activate-account.component';
import {ProfileComponent} from './profile/profile.component';
import {PageNotFoundComponent} from './page-not-found/page-not-found.component';
import {MessageComponent} from './message/message.component';
import {PopupModule, PopupService} from "./popup";
import {ForgotPasswordComponent} from "./forgot-password/forgot-password.component";
import {ChangePasswordComponent} from './change-password/change-password.component';
import {ImageCropperModule} from "ngx-image-cropper";
import {ProfileEditorComponent} from './profile-editor/profile-editor.component';
import {EditInputBaseComponent} from './edit-input-base/edit-input-base.component';
import {ImageCropperUploaderComponent} from './image-cropper-uploader/image-cropper-uploader.component';
import {WriterApplicationComponent} from './writer-application/writer-application.component';
import {WriterApplicationHistoryComponent} from './writer-application-history/writer-application-history.component';
import {PostEditorComponent} from './post-editor/post-editor.component';
import {TextFieldModule} from "@angular/cdk/text-field";
import {PostviewComponent} from './postview/postview.component';
import {PostsComponent} from './posts/posts.component';
import {PostItemComponent} from './post-item/post-item.component';
import {PaginationComponent} from './pagination/pagination.component';
import {EditWriterProfileComponent} from './edit-writer-profile/edit-writer-profile.component';

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        NavbarComponent,
        LoginComponent,
        RegisterComponent,
        ActivateAccountComponent,
        ProfileComponent,
        PageNotFoundComponent,
        MessageComponent,
        ForgotPasswordComponent,
        ChangePasswordComponent,
        ProfileEditorComponent,
        EditInputBaseComponent,
        ImageCropperUploaderComponent,
        WriterApplicationComponent,
        WriterApplicationHistoryComponent,
        PostEditorComponent,
        PostviewComponent,
        PostsComponent,
        PostItemComponent,
        PaginationComponent,
        EditWriterProfileComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule,
        BrowserAnimationsModule,
        MatIconModule,
        PopupModule,
        ImageCropperModule,
        QuillModule.forRoot(),
        TextFieldModule
    ],
    providers: [
        PopupService,
        {
            provide: HTTP_INTERCEPTORS,
            useFactory: function (auth: AuthService, router: Router) {
                return new TokenInterceptor(auth, router);
            },
            deps: [AuthService, Router],
            multi: true
        },
        {provide: LocationStrategy, useClass: PathLocationStrategy}
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
