import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { BehaviorSubject } from 'rxjs';
import { Transaction } from '@/types/transaction';

export const transactionCache = new BehaviorSubject<Transaction[] | null>(null);
export const transactionTotal = new BehaviorSubject<number>(0);

function cacheTransactions(transactions: Transaction[]) {
    let cache: Transaction[] = transactionCache.getValue() || [];
    cache = [...cache, ...transactions];

    transactionCache.next(Array.from(new Set(cache.map(c => c.id))).map(id => <Transaction> cache.find(c => c.id === id)));
}

export function getCustomerTransactions<T = Transaction[] | PaginatedData<Transaction>>(customerId: number, cache: boolean, query?: PaginationQuery) {
    const baseURL = `/customer/${customerId}/transaction`;
    const url = query ? `${baseURL}?page=${query.page}&per_page=${query.per_page}` : baseURL;

    return http.get<Response<T>>(url).then(({ data }) => {
        let transactions: Transaction[] = [];

        if (query) {
            const res = <PaginatedData<Transaction>> (data.data as any);
            transactions = res.data;

            if (cache) {
                transactionTotal.next(res.total);
            }
        } else {
            transactions = <Transaction[]> (data.data as any);
        }

        if (cache) {
            cacheTransactions(transactions);
        }

        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}
