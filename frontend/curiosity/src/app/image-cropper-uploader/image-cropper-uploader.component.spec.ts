import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageCropperUploaderComponent} from './image-cropper-uploader.component';

describe('ProfileImageCropperComponent', () => {
    let component: ImageCropperUploaderComponent;
    let fixture: ComponentFixture<ImageCropperUploaderComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ImageCropperUploaderComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ImageCropperUploaderComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
