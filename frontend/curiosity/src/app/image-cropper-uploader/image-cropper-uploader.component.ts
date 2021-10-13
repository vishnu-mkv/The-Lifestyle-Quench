import {Component, EventEmitter, Input, OnInit, Output, ViewEncapsulation} from '@angular/core';
import {ImageCroppedEvent} from 'ngx-image-cropper';
import {PopupService} from "../popup";
import {MessageService} from "../services/message.service";
import {HttpClient} from "@angular/common/http";
import {apiURL} from "../../environments/environment";

interface ImageUpload {
    success: boolean,
    url: string
}

@Component({
    selector: 'app-image-cropper-uploader',
    templateUrl: './image-cropper-uploader.component.html',
    styleUrls: ['./image-cropper-uploader.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class ImageCropperUploaderComponent implements OnInit {

    @Input() url = "upload/images/";
    @Input() src = "";
    @Input() popupId = "image-upload";
    hasImage = false;
    @Input() aspectRatios: [number, number][] = [[1, 1]]
    currentActiveRatio = 0;
    @Output() imageSetter = new EventEmitter<string>();
    imageChangedEvent: any = '';
    croppedImage: any = '';
    loading = false;

    constructor(public popup: PopupService, private messages: MessageService,
                private http: HttpClient) {
    }

    ngOnInit(): void {
        if (this.src !== '') this.hasImage = true;
    }

    fileChangeEvent(event: any): void {
        this.imageChangedEvent = event;
        this.hasImage = true;
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
        this.loading = true;
        let form = new FormData();
        form.append('image', this.croppedImage);
        return this.http.post<ImageUpload>(apiURL + this.url, form).subscribe(
            data => {
                this.loading = false;
                this.imageSetter.emit(data.url);
                this.messages.showMessage("Image has been uploaded. Don't forget to save your changes.", "info");
                this.popup.close(this.popupId);
                this.src = "";
            },
            error => {
                console.log(error);
                this.messages.showMessage("Image upload failed. Try again.", "error");
                this.loading = false;
            }
        );
    }


}
