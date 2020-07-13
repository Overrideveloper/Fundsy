export function saveToLS<T = any>(key: string, value: T) {
    localStorage.setItem(key, JSON.stringify(value));
}

export function getFromLS<T = any>(key: string) {
    const strValue = localStorage.getItem(key);
    return strValue ? JSON.parse(strValue) as T : null;
}

export function removeFromLS(key: string) {
    localStorage.removeItem(key);
}
