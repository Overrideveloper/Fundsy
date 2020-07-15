import { formAmountToCurrency } from '@/common/utils';

export function currencyFilter(value: number) {
    return formAmountToCurrency(value);
}
