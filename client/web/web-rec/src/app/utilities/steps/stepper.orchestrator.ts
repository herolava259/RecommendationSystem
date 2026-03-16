import { Injectable } from "@angular/core";
import { StepContext, StepDefinition, StepState, StepStatus, TCore } from "./core/step.state";
import { BehaviorSubject } from "rxjs/internal/BehaviorSubject";
import { StepRegistry } from "./step.registry";
import { Router } from "@angular/router";



@Injectable()
export class StepperOrchestrator {

  private workflowId!: string;
  private steps!: StepDefinition[] = [];

  private _stateSubject = new BehaviorSubject<StepState<TCore>[]>([]);
  public stepState$ = this._stateSubject.asObservable();

  private activeStepSubject = new BehaviorSubject<string | null>(null);
  public currentStep$ = this.activeStepSubject.asObservable();

  constructor(
    private registry: StepRegistry,
    private router: Router
  ) {}


  init(workflowId: string) {
    this.workflowId = workflowId;
    this.steps = this.registry.getSteps(workflowId);


    const initialStates = this.steps.map((s, i) => ({
      id: s.id,
      status: i === 0 ? StepStatus.AVAILABLE : StepStatus.LOCKED,
      loading: false,
      visited: false,
    }) as StepState<TCore>);

    this._stateSubject.next(initialStates);

    this.activate(this.steps[0].id);
  }

  async activate(stepId: string) {

    const ctx = this.buildContext(stepId);

    if(! await this.canEnter(stepId, ctx))
      return;
    this.setActive(stepId);

    await this.resolveData(stepId, ctx);

    this.router.navigate([this.steps.find(s => s.id === stepId)?.route]);
  }


  buildContext(stepId: string): StepContext {

    return {
      workflowId: this.workflowId,
      stepId: stepId,
      states: this._stateSubject.getValue(),
    }
  }


}
