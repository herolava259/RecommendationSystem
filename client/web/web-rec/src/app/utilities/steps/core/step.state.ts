import { Type } from "@angular/core";

export enum StepStatus {
  LOCKED = 'Locked',
  AVAILABLE = "Available",
  ACTIVE = "Active",
  COMPLETED = "Completed",
  INVALID = "Invalid",
  ERROR = "Error",
}

export enum StepLabelChangeType {
  Disabled = 'Disabled',
  Editable = 'Editable',
  Readonly = 'Readonly',
  Inprogress = 'InProgress',

}

export interface TCore {

  id: string;
}


export interface StepState<TData extends TCore> {
  id: string;
  loading: boolean;
  visited: boolean;
  enabled: boolean;
  status: StepStatus;
  cachedData?: TData;
  initialData?: TData;
}

export interface StepContext {
  workflowId: string;
  stepId: string;
  states: StepState<TCore>[];
}

export interface StepDefinition {
  id: string;
  label: string;
  route: string;

  linear?: boolean;

  canEnter?: (ctx: StepContext) => boolean | Promise<boolean>;

  canLeave?: (ctx: StepContext) => boolean | Promise<boolean>;

  resolve?: (ctx: StepContext) => Promise<TCore>;

  component?: Type<unknown>;

}


export interface StepLabelChange {
  stepOrder: number;
  label: string;
  type: StepLabelChangeType;
}

export interface WorkflowState<TData> {
  steps: StepState<TData>[];
  activeStepIndex: string | null;
}
