import { AfterContentInit, Component, ContentChildren, EventEmitter, Input, OnInit, Output, QueryList } from '@angular/core';
import { StepperTabComponent } from '../stepper-tab/stepper-tab.component';

@Component({
  selector: 'app-stepper-group',
  imports: [],
  templateUrl: './stepper-group.component.html',
  styleUrl: './stepper-group.component.scss'
})
export class StepperGroupComponent implements OnInit, AfterContentInit {

  @Input() tabAcvtiveIndex = 0;

  @Output() tabActiveChange = new EventEmitter();

  @ContentChildren(StepperTabComponent)
  stepList: QueryList<StepperTabComponent> = new QueryList<StepperTabComponent>();


  ngAfterContentInit(): void {
    this.stepList.changes.subscribe(() => {
      if(this.stepList.length <= this.tabAcvtiveIndex){
        this.selectItem(0);
      }
    })
  }

  selectItem(idx: number)
  {
    this.tabAcvtiveIndex = idx;
    this.tabActiveChange.emit(idx);
  }

  ngOnInit(): void {
    throw new Error('Method not implemented.');
  }

  onNextStep(): void{
    console.log('next step');

  }




}
