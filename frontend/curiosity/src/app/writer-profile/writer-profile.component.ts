import { Component, OnInit } from '@angular/core';
import {postList, PostsService} from "../services/posts.service";
import {ActivatedRoute, Router} from "@angular/router";
import {postSummary, writerUserProfile} from "../interfaces";
import {paginationConfig} from "../pagination/pagination.component";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-writer-profile',
    templateUrl: './writer-profile.component.html',
    styleUrls: ['./writer-profile.component.scss']
})
export class WriterProfileComponent implements OnInit {

    profile : writerUserProfile | null = null;
    writerPosts : postSummary[] = [];
    config: paginationConfig = {count: 0, current: 0, resultSetSize: 1};

    constructor(private posts: PostsService, private route:ActivatedRoute,
                private messages: MessageService, private router: Router) {
    }

    ngOnInit(): void {
        this.route.paramMap.subscribe(
            data => {
                let id = data.get('id');
                if(id) {
                    this.posts.getWriterProfile(id).subscribe(
                        profile => {
                            this.profile = profile;
                            console.log(profile);
                        },
                        _ => {
                            this.messages.showMessage("Writer Does not exists", "error");
                            this.router.navigate(['/404'])
                        }
                    );
                    this.fetchWriterPosts(id);
                }
            }
        )
    }

    paginate(val: number) {
        if (val === this.config.current) return;
        this.posts.getPostList(val).subscribe(
            data => this.setPostData(data, val),
            _ => {
                this.messages.showMessage("Couldn't fetch writer posts", "error");
            }
        );
    }

    fetchWriterPosts(id: string, page=1) {
        this.posts.getPostsByWriter(id, page).subscribe(
            data => {
                this.setPostData(data);
            },
            err => console.log(err)
        )
    }

    setPostData(data: postList, page = 1) {
        this.writerPosts = data.results;
        this.config.count = data.count;
        this.config.resultSetSize = data.results.length;
        this.config.current = page;
    }

}
