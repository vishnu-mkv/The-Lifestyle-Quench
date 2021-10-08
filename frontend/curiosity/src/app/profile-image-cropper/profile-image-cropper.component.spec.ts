import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ProfileImageCropperComponent} from './profile-image-cropper.component';

describe('ProfileImageCropperComponent', () => {
    let component: ProfileImageCropperComponent;
    let fixture: ComponentFixture<ProfileImageCropperComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ProfileImageCropperComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ProfileImageCropperComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
