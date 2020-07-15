const CURRENCY_HTML_SYMBOL = '&#8358';

export function currencyFilter(value: number) {
    if (!value || !Number.isFinite(value)) {
        return '';
    }
    
    let amount = value.toLocaleString('en', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
    
    if (amount.charAt(amount.indexOf('.') + 1) === '0' && amount.charAt(amount.indexOf('.') + 2) === '0') {
        amount = amount.slice(0, amount.indexOf('.'));
    }

    const tempElement = document.createElement('span');
    tempElement.innerHTML = `${CURRENCY_HTML_SYMBOL} ${amount}`;
    return tempElement.innerText;
}
