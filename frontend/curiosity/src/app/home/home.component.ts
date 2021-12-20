import {Component, OnInit} from '@angular/core';
import {PostsService} from "../services/posts.service";
import {postSummary} from "../interfaces";
import {NgForm} from "@angular/forms";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

    topPosts: postSummary[] = [];
    contact = {"email": "", "name": "", "message": ""};
    messageSent = false;
    subEmail = "";
    subscribed = false;

    constructor(private posts: PostsService, private messages: MessageService) {
        posts.getTopPosts().subscribe(
            data => {
                this.topPosts = data;
            },
            err => console.log(err)
        )
    }

    ngOnInit(): void {
    }

    sendMessage(form: NgForm) {
        if (form.invalid) return;
        this.posts.sendMessage(this.contact).subscribe(
            data => {
                this.messageSent = data.success;
                this.resetForm();
            },
            _ => this.messages.showMessage("Couldn't send the message. Something went wrong.", "error")
        );
    }

    resetForm() {
        this.contact = {"email": "", "name": "", "message": ""};
    }

    subscribe(subscribeForm: NgForm) {
        if (subscribeForm.invalid) return;
        this.posts.subscribe({email: this.subEmail}).subscribe(
            data => this.subscribed = data.success,
            _ => {
                this.messages.showMessage("Subscription Failed", "error");
            }
        )
    }
}
