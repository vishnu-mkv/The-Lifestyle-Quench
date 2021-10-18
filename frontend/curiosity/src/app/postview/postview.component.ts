import {Component, Input, OnInit} from '@angular/core';
import {PostsService} from "../services/posts.service";
import {ActivatedRoute} from "@angular/router";
import {post} from "../interfaces";
import {MessageService} from "../services/message.service";
import {DomSanitizer, SafeHtml} from "@angular/platform-browser";

@Component({
    selector: 'app-postview',
    templateUrl: './postview.component.html',
    styleUrls: ['./postview.component.scss', '../post.scss']
})
export class PostviewComponent implements OnInit {

    @Input() post: post | null = null
    //     {
    //     id: 0,
    //     title: '',
    //     slug: '',
    //     content: '',
    //     summary: '',
    //     thumbnail: '',
    //     last_edited: '',
    //     writer_id: '',
    //     writer: '',
    //     status: 'D'
    // }

    constructor(private posts: PostsService, private route: ActivatedRoute, private messages: MessageService,
                private sanitizer: DomSanitizer) {
    }


    transformHtml(htmlTextWithStyle: string): SafeHtml {
        return this.sanitizer.bypassSecurityTrustHtml(htmlTextWithStyle);
    }

    ngOnInit(): void {
        if (this.post !== null) return;
        this.route.paramMap.subscribe(
            data => {
                let id = data.get('id');
                if (id) {
                    this.posts.getPost(id).subscribe(
                        data => {
                            this.post = data;
                            console.log(data);
                        },
                        err => {
                            console.log(err);
                            this.messages.showMessage("Couldn't fetch the post", 'error');
                        }
                    )
                }
            }
        )
    }

}
