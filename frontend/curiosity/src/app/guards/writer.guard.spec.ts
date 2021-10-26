import {TestBed} from '@angular/core/testing';

import {WriterGuard} from './writer.guard';

describe('WriterGuard', () => {
    let guard: WriterGuard;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        guard = TestBed.inject(WriterGuard);
    });

    it('should be created', () => {
        expect(guard).toBeTruthy();
    });
});
