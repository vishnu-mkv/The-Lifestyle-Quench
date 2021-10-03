import {Component, OnInit} from '@angular/core';
import {Message, MessageService} from "../services/message.service";
import {Observable} from "rxjs";

@Component({
    selector: 'app-message',
    templateUrl: './message.component.html',
    styleUrls: ['./message.component.scss']
})
export class MessageComponent implements OnInit {

    messages: Observable<Message[]>

    constructor(private messageService: MessageService) {
        this.messages = messageService.getMessages();
    }

    ngOnInit(): void {
    }

}
