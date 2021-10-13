import {ComponentFixture, TestBed} from '@angular/core/testing';

import {WriterApplicationHistoryComponent} from './writer-application-history.component';

describe('WriterApplicationHistoryComponent', () => {
    let component: WriterApplicationHistoryComponent;
    let fixture: ComponentFixture<WriterApplicationHistoryComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [WriterApplicationHistoryComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(WriterApplicationHistoryComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
