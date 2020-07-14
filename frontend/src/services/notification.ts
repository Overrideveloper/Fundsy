import miniToastr from 'mini-toastr';
import swal from 'sweetalert';
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
    success: { title: '', message: '', type: 'success' },
    info: { title: '', message: '', type: 'info' },
    warn: { title: '', message: '', type: 'warn' },
    error: { title: '', message: '', type: 'error' },
};

export function prompt(icon: 'info' | 'warning' = 'warning', title: string, text: string, danger?: boolean) {
    return swal({ title, text, icon, buttons: [true, true], dangerMode: danger}).then(willAct => Promise.resolve(willAct));
}
