import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { BehaviorSubject } from 'rxjs';
import { CustomerInvestmentRes as CustomerInvestment, CustomerInvestmentCreateReq, CustomerInvestmentWithdrawReq } from '@/types/customer_investment';
import { AppreciationLogType } from '@/types/appreciation_log';

export const customerInvestmentCache = new BehaviorSubject<CustomerInvestment[] | null>(null);
export const customerInvestmentTotal = new BehaviorSubject<number>(0);

function cacheCustomerInvestments(customerInvestments: CustomerInvestment[]) {
    let cache: CustomerInvestment[] = customerInvestmentCache.getValue() || [];
    cache = [ ...cache, ...customerInvestments ];

    customerInvestmentCache.next(Array.from(new Set(cache.map(c => c.id))).map(id => <CustomerInvestment> cache.find(c => c.id === id)));
}

function incrementCustomerInvestmentTotal() {
    customerInvestmentTotal.next(customerInvestmentTotal.getValue() + 1);
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

export function getFromCustomerInvestmentCache(id: number) {
    const cache: CustomerInvestment[] = customerInvestmentCache.getValue() || [];
    return cache.find(c => c.id === id);
}

export function getCustomerInvestments<T = CustomerInvestment[] | PaginatedData<CustomerInvestment>>(customerId: number, query?: PaginationQuery) {
    const baseURL = `/customer/${customerId}/customer_investment`;
    const url = query ? `${baseURL}?page=${query.page}&per_page=${query.per_page}` : baseURL;

    return http.get<Response<T>>(url).then(({ data }) => {
        let customerInvestments: CustomerInvestment[] = [];

        if (query) {
            const res = <PaginatedData<CustomerInvestment>> (data.data as any);
            customerInvestments = res.data;
            customerInvestmentTotal.next(res.total);
        } else {
            customerInvestments = <CustomerInvestment[]> (data.data as any);
        }

        cacheCustomerInvestments(customerInvestments);
        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}

export function createCustomerInvestment(req: CustomerInvestmentCreateReq) {
    return http.post<Response<CustomerInvestment>>('/customer_investment', req).then(({ data }) => {
        cacheCustomerInvestments([data.data]);
        incrementCustomerInvestmentTotal();
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}

export function getCustomerInvestment(id: number) {
    return http.get<Response<CustomerInvestment>>(`/customer_investment/${id}`).then(({ data }) => {
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}

export function getWithdrawalEligibility(id: number) {
    return http.get<Response<boolean>>(`/customer_investment/${id}/withdrawal_eligibility`).then(({ data }) => {
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}

export function getMaxAmountWithdrawable(id: number) {
    return http.get<Response<number>>(`/customer_investment/${id}/max_amount_withdrawable`).then(({ data }) => {
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}

export function withdrawFromCustomerInvestment(req: CustomerInvestmentWithdrawReq) {
    return http.post<Response<CustomerInvestment>>(`/customer_investment/withdraw`, req).then(({ data }) => {
        replaceInCache(data.data);
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}

export function getAppreciationLogs<T>(id: number, type?: AppreciationLogType, query?: PaginationQuery) {
    let url = null;
    
    if (type && query) {
        url = `/customer_investment/${id}/appreciation_log?type=${type}&page=${query.page}&per_page=${query.per_page}`;
    } else if (!type && query) {
        url = `/customer_investment/${id}/appreciation_log?page=${query.page}&per_page=${query.per_page}`;
    } else if (type && !query) {
        url = `/customer_investment/${id}/appreciation_log?type=${type}`;
    } else {
        url = `/customer_investment/${id}/appreciation_log`;
    }
    
    return http.get<Response<T>>(url).then(({ data }) => {
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}
