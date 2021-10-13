import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import Quill from "quill";
import {PopupService} from "../popup";
import {postEdit} from "../interfaces";
import {PostsService} from "../services/posts.service";
import {NgForm} from "@angular/forms";

@Component({
    selector: 'app-post-editor',
    templateUrl: './post-editor.component.html',
    styleUrls: ['./post-editor.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class PostEditorComponent implements OnInit {

    quill: Quill | any;
    titlePlaceholder = "How Rick Roll become so famous on social medias!";
    summaryPlaceholder = "Never gonna give you up. Never gonna let you down. Never gonna run around and desert you" +
        ". Never gonna make you cry. Never gonna say goodbye. Never gonna tell a lie and hurt you";

    postInstance: postEdit = {
        title: '',
        summary: '',
        content: '',
        thumbnail: ''
    }

    modules = {
        toolbar: {
            container: [
                [{'header': [3, 4, 5, 6, false]}],
                ['bold', 'italic', 'underline'],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                [{'align': []}],
                ['link', 'image'],
                ['clean'],
                [{
                    'color': ['#FFFFFF', '#50c878', '#0f6e32',
                        '#fbf5f3', '#ef7d7d', '#aba9a9', '#145873']
                }]
            ],
            handlers: {
                image: this.imageHandler.bind(this)
            }
        },
    };

    constructor(public popup: PopupService, private posts: PostsService) {
    }

    ngOnInit(): void {
    }

    imageHandler() {
        this.popup.open("image-upload");
    }

    getEditorInstance(event: any) {
        this.quill = event;
    }

    imageUploaded(event: string) {
        console.log(this.quill, event)
        const range = this.quill.getSelection();
        this.quill.editor.insertEmbed(range.index, 'image', event);
    }

    thumbnailUploaded(event: string) {
        this.postInstance.thumbnail = event;
    }

    createPost(postForm: NgForm) {
        console.log("Submitting");
        if (postForm.invalid) return;
        this.posts.createPost(this.postInstance).subscribe(
            data => console.log(data),
            err => console.log(err)
        )
    }
}
