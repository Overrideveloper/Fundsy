export type NotificationType = 'success' | 'error' | 'warn' | 'info';

export type ToastTypes = Record<NotificationType, NotificationType>;

export interface ToastProps { 
    title: string;
    message: string;
    type: NotificationType;
    timeout: number;
    cb: any;
};

export interface Notification<T> {
    title: string;
    message: string;
    type: T;
};

export type NamedNotifications = Record<NotificationType, Notification<NotificationType>>;
