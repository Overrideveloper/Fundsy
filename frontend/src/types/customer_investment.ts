import { InvestmentRes } from './investment';

export interface CustomerInvestmentCreateReq {
    customer_id: number;
    title: string;
    amount: number;
    investment_id: string;
}

export interface CustomerInvestmentRes {
    id: number;
    title: string;
    amount: number;
    created_at: string;
    investment: InvestmentRes;
}
