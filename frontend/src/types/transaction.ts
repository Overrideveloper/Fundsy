import { CustomerInvestmentResOmitInvestment } from './customer_investment';

export enum TransactionType {
    CREDIT = "CREDIT",
    WITHDRAWAL = "WITHDRAWAL"
}

export interface Transaction {
    id: number;
    amount: number;
    description: string;
    type: TransactionType;
    customer_investment_id: number;
    customer_id: number;
    customer_investment: CustomerInvestmentResOmitInvestment;
    created_at: string;
}
