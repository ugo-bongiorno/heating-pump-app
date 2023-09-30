import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HpToolsComponent } from './hp-tools.component';

describe('HpToolsComponent', () => {
  let component: HpToolsComponent;
  let fixture: ComponentFixture<HpToolsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HpToolsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HpToolsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
