import {Injectable} from '@angular/core';
import {
    HttpRequest,
    HttpErrorResponse,
    HttpHandler,
    HttpEvent,
    HttpInterceptor
} from '@angular/common/http';
import {AuthService} from './services/auth.service';
import {Observable, of, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {Router} from '@angular/router';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

    constructor(public auth: AuthService, private router: Router) {
    }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {


        if (this.auth.isAuthenticated()) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${this.auth.getToken()}`,
                    // AccessControlAllowOrigin: 'http://127.0.0.1:4200'
                }
            });
        }

        return next.handle(request).pipe(catchError(x => this.handleAuthError(x)));
    }

    private handleAuthError(err: HttpErrorResponse): Observable<any> {
        //handle your auth error or rethrow
        if (err.status === 401 || err.status === 403) {
            //navigate /delete cookies or whatever
            // this.auth.logout();
            this.router.navigateByUrl(`/login`);
            // if you've caught / handled the error, you don't want to rethrow it unless you also want downstream consumers to have to handle it as well.
            return of(err.message); // or EMPTY may be appropriate here
        }
        return throwError(err);
    }
}
