import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class MessageService {

    messages: Message[] = [];
    messageSource = new BehaviorSubject<Message[]>(this.messages);

    constructor() {
    }

    showMessage(message: string, type: string) {
        let obj = new Message(message, type);
        this.messages.push(obj);
        setTimeout(() => {
            let index = this.messages.indexOf(obj);
            if (index !== -1) {
                this.messages.splice(index, 1);
            }
        }, 3000)
        this.messageSource.next(this.messages);
    }

    getMessages() {
        return this.messageSource.asObservable();
    }
}

export class Message {
    public text: string;
    public classType: string;

    constructor(message: string, classType: string) {
        this.text = message;
        this.classType = classType;
    }
}
