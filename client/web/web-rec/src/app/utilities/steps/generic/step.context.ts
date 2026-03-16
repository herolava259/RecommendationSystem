import { Injectable } from "@angular/core";
import { StepEvent } from "./step.event";



@Injectable()
export class StepOrchestratorContext {

  public onPush<TData>(event : StepEvent<TData>): void {
    
  }
}
