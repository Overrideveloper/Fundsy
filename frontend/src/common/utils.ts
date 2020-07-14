const DAY = 86400, WEEK = 604800, MONTH = 2592000, YEAR = 31104000;

type durationType = ('days' | 'weeks' | 'months' | 'years');

export const durationTypes: durationType[] = ['days', 'weeks', 'months', 'years'];

export function getSecondsFromDuration(type: durationType, amount: number) {
    let seconds = 0;

    switch (type) {
      case 'days':
        seconds = DAY * amount;
        break;
      case 'weeks':
        seconds = WEEK * amount;
        break;
      case 'months':
        seconds = MONTH * amount;
        break;
      case 'years':
        seconds = YEAR * amount;
        break;
      default:
        break;
    }

    return seconds;
}

export function getDurationFromSeconds(seconds: number): { amount: number, type: durationType } {
    const duration: { amount: number, type: durationType } = { amount: 0, type: 'days' };

    if (Number.isInteger(seconds / YEAR) === true) {
        duration.amount = (seconds / YEAR);
        duration.type = 'years';
    } else if (Number.isInteger(seconds / MONTH) === true) {
        duration.amount = (seconds / MONTH);
        duration.type = 'months';
    } else if (Number.isInteger(seconds / WEEK) === true) {
        duration.amount = (seconds / WEEK);
        duration.type = 'weeks';
    } else if (Number.isInteger(seconds / DAY) === true) {
        duration.amount = (seconds / DAY);
        duration.type = 'days';
    }

    return duration;
}

export const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

export function getDateStringFromDateTime(datetime: string) {
  const date = new Date(datetime);
  return `${date.getDate()} ${MONTHS[date.getMonth()]}, ${date.getFullYear()}`;
}