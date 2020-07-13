export interface InvestmentRes {
    id: number;
    appreciation_amount: number;
    appreciation_duration: number;
    lock_period: number;
    withdrawal_cost: number;
    title: string;
}

export interface InvestmentReq {
    appreciation_amount: number;
    appreciation_duration: number;
    lock_period: number;
    withdrawal_cost: number;
    title: string;
}
