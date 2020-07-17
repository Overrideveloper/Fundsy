import { InvestmentRes } from './investment';

export interface CustomerInvestmentCreateReq {
    customer_id: number;
    title: string;
    amount: number;
    investment_id: number;
}

export interface CustomerInvestmentRes {
    id: number;
    title: string;
    amount: number;
    appreciation: number;
    created_at: string;
    investment_id: number;
    investment: InvestmentRes;
}

export interface CustomerInvestmentResOmitInvestment {
    id: number;
    title: string;
    amount: number;
    created_at: string;
}

export interface CustomerInvestmentWithdrawReq {
    id: number;
    amount: number;
}
