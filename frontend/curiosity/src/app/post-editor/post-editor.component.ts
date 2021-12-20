import {Component, OnInit, ViewChild, ViewEncapsulation} from '@angular/core';
import Quill from "quill";
import {PopupService} from "../popup";
import {post} from "../interfaces";
import {PostsService} from "../services/posts.service";
import {NgForm} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthService} from "../services/auth.service";
import {MessageService} from "../services/message.service";
import {interval} from "rxjs";

@Component({
    selector: 'app-post-editor',
    templateUrl: './post-editor.component.html',
    styleUrls: ['./post-editor.component.scss', '../post.scss'],
    encapsulation: ViewEncapsulation.None
})
export class PostEditorComponent implements OnInit {

    quill: Quill | any;
    titlePlaceholder = "A nice title would be good.";
    summaryPlaceholder = "A summary about the post."

    postInstance: post = {
        id: 0,
        title: '',
        summary: '',
        content: '',
        thumbnail: '',
        slug: '',
        last_edited: (new Date()).toISOString(),
        status: 'D',
        writer: 'author',
        writer_id: '',
        writer_profile_pic: ''
    }
    create = true;
    postCopy = this.postInstance;
    @ViewChild('form', {static: true}) form!: NgForm;

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
                    'color': ['#3cd73c', '#FFFFFF', '#50c878', '#0f6e32',
                        '#fbf5f3', '#ef7d7d', '#aba9a9', '#145873']
                }]
            ],
            handlers: {
                image: this.imageHandler.bind(this)
            }
        }
    };
    preview = false;
    autoSave = false;
    autoSaver = interval(10000).subscribe(() => {
        if (this.autoSave && !this.preview) this.save(true);
    });
    saving = false;

    constructor(public popup: PopupService, public posts: PostsService,
                private route: ActivatedRoute, private auth: AuthService,
                private router: Router, private messages: MessageService) {
        auth.fetchWriterProfile();
    }

    ngOnInit(): void {

        this.route.paramMap.subscribe(
            data => {
                let slug = data.get('id');
                if (slug && slug !== 'new') {
                    this.create = false
                    this.posts.getPost(slug).subscribe(
                        data => {
                            this.postInstance = data;
                            this.postCopy = Object.assign({}, data);
                            if (data.status == 'P') {
                                this.messages.showMessage('The post has already been published. Edit not allowed. Contact administrator.', 'error');
                                this.router.navigate(['./profile'])
                            }
                            this.auth.getWriterProfile().subscribe(
                                data => {
                                    if (this.postInstance.writer_id !== data.writer_name) {
                                        this.auth.getProfile().subscribe(
                                            data => {
                                                if (!data.user.staff && !data.user.admin) {
                                                    this.messages.showMessage('403 - unauthorized', 'error');
                                                    this.router.navigate(['/login']);
                                                }
                                            }
                                        )
                                    }
                                }
                            )
                        }
                    )
                } else {
                    this.auth.getProfile().subscribe(
                        data => {
                            this.postInstance.writer_profile_pic = data.profile_pic;
                            this.postInstance.writer = data.user.first_name + ' ' + data.user.last_name;
                        }
                    )
                }
            }
        );
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

    saveChanges(postForm: NgForm) {
        if (postForm.invalid) this.messages.showMessage('Create failed. Check if all fields are filled', 'error');
        else this.save();
    }

    save(passive = false) {
        this.saving = true;
        this.posts.savePost(this.create, {
            title: this.postInstance.title, summary: this.postInstance.summary,
            content: this.postInstance.content, thumbnail: this.postInstance.thumbnail, slug: this.postInstance.slug
        }, this.postInstance.slug).subscribe(
            data => {
                this.reloadIfSlugChange(this.postInstance.slug, data.slug);
                this.create = false;
                if (!passive) {
                    this.postInstance = data;
                    this.messages.showMessage(this.create ? "Post created." : "Changes saved", 'success');
                }
            },
            err => {
                for (let field in err.error) {
                    this.messages.showMessage(`${field} - ${err.error[field]}`, 'error');
                }
            },
            () => this.saving = false
        )
    }

    reloadIfSlugChange(oldSLug: string, newSlug: string) {
        if (oldSLug !== newSlug) {
            this.messages.showMessage("URL Changed. Reloading...", "info");
            this.router.navigate(['/posts', newSlug, 'edit']);
        }
    }

    submitPost() {
        this.posts.submitPost(this.postInstance.slug).subscribe(
            data => {
                if (data.status == 'S') {
                    this.postInstance.status = 'S';
                    this.messages.showMessage('Post submitted successfully.', 'info');
                }
            },
            () => this.messages.showMessage("Something went wrong. Couldn't submit post", 'error')
        )
    }

    deletePost() {
        this.posts.deletePost(this.postInstance.slug).subscribe(
            data => {
                if (data.delete) {
                    this.messages.showMessage(data.message, 'success');
                    this.router.navigate(['/']);
                }
            }
        )
    }

    reset() {
        this.postInstance = Object.assign({}, this.postCopy);
        this.messages.showMessage("Resetting", "info");
        this.save();
    }
}
