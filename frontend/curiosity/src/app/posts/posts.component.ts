import {Component, OnInit} from '@angular/core';
import {postList, PostsService} from "../services/posts.service";
import {postSummary} from "../interfaces"
import {paginationConfig} from "../pagination/pagination.component";
import {MessageService} from "../services/message.service";
import {NgForm} from "@angular/forms";

@Component({
    selector: 'app-posts',
    templateUrl: './posts.component.html',
    styleUrls: ['./posts.component.scss']
})
export class PostsComponent implements OnInit {

    posts: postSummary[] = []
    config: paginationConfig = {count: 0, current: 0, resultSetSize: 1};
    searchTerm = '';

    constructor(private postsService: PostsService, private messages: MessageService) {
        this.fetchPosts();
    }

    fetchPosts() {
        this.postsService.getPostList().subscribe(
            data => this.setPostData(data),
            err => {
                this.messages.showMessage("Couldn't fetch posts", "error");
                console.log(err);
            }
        )
    }

    setPostData(data: postList, page = 1) {
        this.posts = data.results;
        this.config.count = data.count;
        this.config.resultSetSize = 5;
        this.config.current = page;
    }

    ngOnInit(): void {
    }

    paginate(val: number) {

        if (this.searchTerm) return this.fetchSearchPosts(val);

        if (val === this.config.current) return;
        this.postsService.getPostList(val).subscribe(
            data => this.setPostData(data, val),
            err => {
                this.messages.showMessage("Couldn't fetch posts", "error");
                console.log(err);
            }
        );
    }

    searchPosts(searchForm: NgForm) {
        this.searchTerm = searchForm.value.search;
        if (this.searchTerm !== '') {
            this.fetchSearchPosts();
        } else this.fetchPosts();
    }

    fetchSearchPosts(pageNumber = 1) {
        this.postsService.search(this.searchTerm, pageNumber).subscribe(
            data => this.setPostData(data),
            err => console.log(err)
        );
    }
}
