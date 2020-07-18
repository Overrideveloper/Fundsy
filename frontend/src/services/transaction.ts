import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { Transaction } from '@/types/transaction';

export function getCustomerTransactions<T = Transaction[] | PaginatedData<Transaction>>(customerId: number, query?: PaginationQuery) {
    const baseURL = `/customer/${customerId}/transaction`;
    const url = query ? `${baseURL}?page=${query.page}&per_page=${query.per_page}` : baseURL;

    return http.get<Response<T>>(url).then(({ data }) => {
        let transactions: Transaction[] = [];

        if (query) {
            transactions = (<PaginatedData<Transaction>> (data.data as any)).data;
        } else {
            transactions = <Transaction[]> (data.data as any);
        }
        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}
