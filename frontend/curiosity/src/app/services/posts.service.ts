import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {apiURL} from "../../environments/environment";
import {Observable} from "rxjs";
import {post, postSummary, writerUserProfile} from "../interfaces";
import {AuthService} from "./auth.service";


interface postSubmit {
    status: string,
    message?: string
}


interface postDelete {
    delete: boolean,
    message: string,
    slug: string
}

export interface postList {
    results: postSummary[],
    prev: string | null,
    next: string | null,
    count: number
}

@Injectable({
    providedIn: 'root'
})
export class PostsService {

    constructor(private http: HttpClient, private auth: AuthService) {
    }

    getWriterPosts(): Observable<any> | null {
        if (this.auth.isAuthenticated()) return this.http.get<post[]>(apiURL + 'api/users/posts');
        return null;
    }

    unSubmit(slug: string) {
        return this.http.delete<postSubmit>(apiURL + `posts/${slug}/submit/`);
    }

    submitPost(slug: string) {
        return this.http.post<postSubmit>(apiURL + `posts/${slug}/submit/`, {'submit': true});
    }

    deletePost(slug: string) {
        return this.http.delete<postDelete>(apiURL + `posts/${slug}/`);
    }

    savePost(create: boolean, post: { summary: string; thumbnail: string; title: string; content: string; slug: string }, id: string = "") {
        if (create) return this.http.post<post>(apiURL + 'posts/', post);
        return this.http.put<post>(apiURL + 'posts/' + id + '/', post)
    }

    getPost(slug: string) {
        return this.http.get<post>(apiURL + 'posts/' + slug + '/');
    }

    getPostList(pageNumber = 1) {
        return this.http.get<postList>(apiURL + 'posts/?page=' + pageNumber);
    }

    search(searchTerm: string, pageNumber: number) {
        return this.http.get<postList>(apiURL + 'posts/search/' + searchTerm + '?page=' + pageNumber);
    }

    getTopPosts() {
        return this.http.get<postSummary[]>(apiURL + 'posts/top/');
    }

    sendMessage(data: { name: string, email: string, message: string }) {
        return this.http.post<{ success: boolean }>(apiURL + 'api/users/contact-us/', data);
    }

    subscribe(data: { email: string }) {
        return this.http.post<{ success: boolean }>(apiURL + 'posts/subscribe/', data);
    }

    getWriterProfile(id: string) {
        return this.http.get<writerUserProfile>(apiURL+'api/users/writer-profile/'+id+'/');
    }

    getPostsByWriter(id: string, page: number=1) {
        return this.http.get<postList>(apiURL + 'posts/writer/'+id+'?page='+page);
    }
}
