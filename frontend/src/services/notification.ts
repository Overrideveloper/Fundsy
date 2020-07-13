import miniToastr from 'mini-toastr';
import { ToastTypes, ToastProps, NamedNotifications } from '@/types/notification';

const toastTypes: ToastTypes = {
    success: 'success',
    error: 'error',
    info: 'info',
    warn: 'warn'
};

miniToastr.init({ types: toastTypes });

function toast({ title, message, type, timeout, cb }: ToastProps) {
    return miniToastr[type](message, title, timeout, cb);
}

export const notificationOptions: { [key: string]: (props: ToastProps) => any } = {
    success: toast,
    error: toast,
    info: toast,
    warn: toast,
}

export const NOTIFICATIONS: NamedNotifications = {
    success: { title: 'Success!', message: '', type: 'success' },
    info: { title: 'Information', message: '', type: 'info' },
    warn: { title: 'Warning!', message: '', type: 'warn' },
    error: { title: 'Error!', message: '', type: 'error' },
};
