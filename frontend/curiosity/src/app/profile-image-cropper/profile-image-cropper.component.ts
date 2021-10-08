import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ImageCroppedEvent} from 'ngx-image-cropper';
import {AuthService} from "../services/auth.service";
import {PopupService} from "../popup";
import {MessageService} from "../services/message.service";

@Component({
    selector: 'app-profile-image-cropper',
    templateUrl: './profile-image-cropper.component.html',
    styleUrls: ['./profile-image-cropper.component.scss']
})
export class ProfileImageCropperComponent implements OnInit {

    @Input() src = "";
    @Output() imageSetter = new EventEmitter<string>();
    imageChangedEvent: any = '';
    croppedImage: any = '';

    constructor(private auth: AuthService, public popup: PopupService, private messages: MessageService) {
    }

    ngOnInit(): void {
        console.log(this.src);
    }

    fileChangeEvent(event: any): void {
        this.imageChangedEvent = event;
    }

    imageCropped(event: ImageCroppedEvent) {
        this.croppedImage = event.base64;
    }

    imageLoaded() {
        return true;
    }

    loadImageFailed() {
        console.log("failed", this.src);
    }

    uploadImage() {
        this.auth.uploadProfileImage(this.croppedImage).subscribe(
            data => {
                this.imageSetter.emit(data.url);
                this.messages.showMessage("Image has been uploaded. Don't forget to save your changes.", "info");
            },
            error => {
                console.log(error);
                this.messages.showMessage("Image upload failed. Try again.", "error");
            }
        );
    }


}
