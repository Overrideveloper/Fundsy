import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { BehaviorSubject } from 'rxjs';
import { CustomerRes as Customer } from '@/types/customer';

export const customerCache = new BehaviorSubject<Customer[] | null>(null);

function cacheCustomers(customers: Customer[]) {
    let cache: Customer[] = customerCache.getValue() || [];
    cache = [...cache, ...customers];

    customerCache.next(Array.from(new Set(cache.map(c => c.id))).map(id => <Customer> cache.find(c => c.id === id)));
}

export function getFromCustomerCache(id: number) {
    let cache: Customer[] = customerCache.getValue() || [];
    return cache.find(c => c.id === id);
}

export function getCustomers<T = Customer[] | PaginatedData<Customer>>(query?: PaginationQuery) {
    const url = query ? `/customer?page=${query.page}&per_page=${query.per_page}` : '/customer';

    return http.get<Response<T>>(url).then(({ data }) => {
        let customers: Customer[] = [];

        if (query) {
            customers = (<PaginatedData<Customer>> (data.data as any)).data;
        } else {
            customers = (<Customer[]> (data.data as any))
        }

        cacheCustomers(customers);
        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}

export function getCustomer(id: number) {
    return http.get<Response<Customer>>(`/customer/${id}`).then(({ data }) => {
        cacheCustomers([data.data]);
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}
