import http from './http';
import { PaginationQuery, PaginatedData } from '@/types';
import { Response } from '@/types/http';
import { BehaviorSubject } from 'rxjs';
import { InvestmentRes as Investment, InvestmentReq } from '@/types/investment';

export const investmentCache = new BehaviorSubject<Investment[] | null>(null);

function cacheInvestments(investments: Investment[]) {
    let cache: Investment[] = investmentCache.getValue() || [];
    cache = [...cache, ...investments];

    investmentCache.next(Array.from(new Set(cache.map(c => c.id))).map(id => <Investment> cache.find(c => c.id === id)));
}

export function getInvestments<T = Investment[] | PaginatedData<Investment>>(query?: PaginationQuery) {
    const url = query ? `/investment?page=${query.page}&per_page=${query.per_page}` : '/investment';

    return http.get<Response<T>>(url).then(({ data }) => {
        let investments: Investment[] = [];

        if (query) {
            investments = (<PaginatedData<Investment>> (data.data as any)).data;
        } else {
            investments = (<Investment[]> (data.data as any))
        }

        cacheInvestments(investments);
        return Promise.resolve(data.data as T);
    }).catch(err => Promise.reject(err));
}

export function createInvestment(req: InvestmentReq) {
    return http.post<Response<Investment>>('/investment', req).then(({ data }) => {
        cacheInvestments([data.data]);
        return Promise.resolve(data.data);
    }).catch(err => Promise.reject(err));
}