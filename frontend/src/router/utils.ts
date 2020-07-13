import { currentUser } from "@/services/auth";

export const homeRedirect = () => currentUser.getValue()?.user.is_admin ? '/admin' : '/investments';
