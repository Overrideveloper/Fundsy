import { formatAmountToCurrency } from '@/common/utils';

export function currencyFilter(value: number) {
    return formatAmountToCurrency(value);
}
