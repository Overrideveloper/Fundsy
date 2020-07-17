export interface AppreciationLogRes {
    old_amount: number;
    new_amount: number;
    created_at: string;
}

export interface AppreciationLogResWeekly extends AppreciationLogRes {
    week: number;
    year: number;
}

export interface AppreciationLogResMonthly extends AppreciationLogRes {
    month: number;
    year: number;
}

export interface AppreciationLogResQuarterly extends AppreciationLogRes {
    quarter: number;
    year: number;
}

export enum AppreciationLogType {
    WEEKLY = "weekly",
    MONTHLY = "monthly",
    QUARTERLY = "quarterly"
}