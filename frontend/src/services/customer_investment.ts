import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { BehaviorSubject } from 'rxjs';
import { CustomerInvestmentRes as CustomerInvestment, CustomerInvestmentCreateReq } from '@/types/customer_investment';

export const customerInvestmentCache = new BehaviorSubject<CustomerInvestment[] | null>(null);

function cacheCustomerInvestments(customerInvestments: CustomerInvestment[]) {
    let cache: CustomerInvestment[] = customerInvestmentCache.getValue() || [];
    cache = [ ...cache, ...customerInvestments ];

    customerInvestmentCache.next(Array.from(new Set(cache.map(c => c.id))).map(id => <CustomerInvestment> cache.find(c => c.id === id)));
}

function removeFromCache(id: number) {
    let cache: CustomerInvestment[] = customerInvestmentCache.getValue() || [];
    customerInvestmentCache.next(cache.filter(c => c.id !== id));
}

function replaceInCache(customerInvestment: CustomerInvestment) {
    let cache: CustomerInvestment[] = customerInvestmentCache.getValue() || [];
    const indexInCache = cache.findIndex(c => c.id === customerInvestment.id);

    if (indexInCache > -1) {
        cache.splice(indexInCache, 1, customerInvestment);
        customerInvestmentCache.next(cache);
    }
}

export function getCustomerInvestments<T = CustomerInvestment[] | PaginatedData<CustomerInvestment>>(customerId: number, query?: PaginationQuery) {
    const baseURL = `/customer/${customerId}/customer_investment`;
    const url = query ? `${baseURL}?page=${query.page}&per_page=${query.per_page}` : baseURL;

    return http.get<Response<T>>(url).then(({ data }) => {
        let customerInvestments: CustomerInvestment[] = [];

        if (query) {
            customerInvestments = (<PaginatedData<CustomerInvestment>> (data.data as any)).data;
        } else {
            customerInvestments = (<CustomerInvestment[]> (data.data as any))
        }

        cacheCustomerInvestments(customerInvestments);
        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}

export function createCustomerInvestment(req: CustomerInvestmentCreateReq) {
    return http.post<Response<CustomerInvestment>>('/customer_investment', req).then(({ data }) => {
        cacheCustomerInvestments([data.data]);
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}
