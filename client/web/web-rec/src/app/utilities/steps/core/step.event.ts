import { StepStatus } from "./step.state";



export interface StepEvent{
  id: string;
  status: StepStatus
}

export interface DispatchDataEvent<TData> {
  sourceStepId: string;
  targetStepId: string;
  data: TData;
}
