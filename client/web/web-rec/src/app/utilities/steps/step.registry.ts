import { Injectable } from "@angular/core";
import { StepDefinition } from "./core/step.state";



@Injectable({providedIn: 'root'})
export class StepRegistry {

  private registry = new Map<string, StepDefinition[]>();

  public register(workflowId: string, steps: StepDefinition[]) {
    this.registry.set(workflowId, steps);
  }

  public getSteps(workflowId: string): StepDefinition[] {
    return this.registry.get(workflowId) || [];
  }

}
