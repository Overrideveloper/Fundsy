export interface SidebarRoute {
    to: string;
    name: string;
    icon: string;
    icon_solid?: boolean;
}

export interface PaginationQuery {
    page: number;
    per_page: number;
}

export interface PaginatedData<T> {
    data: T[];
    total: number;
    page: number;
    per_page: number;
}

export interface DatatableColumn {
    label: string;
    field: string;
    formatFn?: Function;
}

export interface DatatableButton {
    id: string;
    link?: string;
    displayText: string;
}