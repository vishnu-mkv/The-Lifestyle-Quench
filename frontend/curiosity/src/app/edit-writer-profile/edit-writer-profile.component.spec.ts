import {ComponentFixture, TestBed} from '@angular/core/testing';

import {EditWriterProfileComponent} from './edit-writer-profile.component';

describe('EditWriterProfileComponent', () => {
    let component: EditWriterProfileComponent;
    let fixture: ComponentFixture<EditWriterProfileComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [EditWriterProfileComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(EditWriterProfileComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
