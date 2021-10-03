import {Component, OnInit} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {post, Profile} from "../interfaces";
import {Observable} from "rxjs";
import {MatIconModule} from '@angular/material/icon';
import {PostsService} from "../services/posts.service";
import {MessageService} from "../services/message.service";
import {PopupService} from "../popup";

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

    profile: Observable<Profile>;
    isWriter: boolean = false;
    posts: post[] = [];
    deleteId = "";

    constructor(private auth: AuthService, private postService: PostsService,
                private messages: MessageService, public popupService: PopupService) {
        this.profile = auth.getProfile();
        auth.getProfile().subscribe(
            data => {
                this.isWriter = data.user.writer;
                if (this.isWriter) {
                    this.loadWriterPosts();
                }
            }
        )
    }

    ngOnInit(): void {
    }

    loadWriterPosts() {
        this.postService.getWriterPosts().subscribe(
            data => {
                this.posts = data;
            },
            err => this.messages.showMessage(err.error.message, "error")
        )
    }

    shortenString(str: string, n: number) {
        if (str.length <= n) return str;
        return str.substr(0, n) + '...';
    }

    deleteSubmission(post: post) {
        this.postService.unSubmit(post.slug).subscribe(
            data => {
                post.status = data.status;
                this.messages.showMessage(data.message!, "info");
            },
            err => this.messages.showMessage(err.error.message, "error")
        )
    }

    submitPost(post: post) {
        this.postService.submitPost(post.slug).subscribe(
            data => {
                post.status = data.status;
                this.messages.showMessage(data.message!, "success");
            },
            err => this.messages.showMessage(err.error.message, "error")
        )
    }

    deletePost() {
        this.popupService.close('confirm-delete');
        this.postService.deletePost(this.deleteId).subscribe(
            data => {
                if (data.delete) {
                    this.posts = this.posts.filter(x => x.slug !== this.deleteId);
                    this.messages.showMessage(data.message, "success")
                }
            },
            err => this.messages.showMessage(err.error.message, "error")
        )
    }

    openConfirmation(post: post) {
        this.deleteId = post.slug;
        this.popupService.open('confirm-delete');
    }
}
