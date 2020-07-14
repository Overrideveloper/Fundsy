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
