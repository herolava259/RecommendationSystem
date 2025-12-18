export type AlertType = 'success' | 'error' | 'info' | 'warning';

export interface ToastInfo {
    body: string;
    type: AlertType;
}