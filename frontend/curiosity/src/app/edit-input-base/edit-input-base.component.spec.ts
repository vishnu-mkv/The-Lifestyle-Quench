import {ComponentFixture, TestBed} from '@angular/core/testing';

import {EditInputBaseComponent} from './edit-input-base.component';

describe('EditInputBaseComponent', () => {
    let component: EditInputBaseComponent;
    let fixture: ComponentFixture<EditInputBaseComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [EditInputBaseComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(EditInputBaseComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
