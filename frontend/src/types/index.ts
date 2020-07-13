export interface SidebarRoute {
    to: string;
    name: string;
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
