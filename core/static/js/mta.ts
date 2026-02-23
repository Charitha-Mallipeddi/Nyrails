const TIME_ZONE = 'America/New_York';
export const format = {
  time_duration: (ms: number) => {
    if (ms < 0) ms = -ms;
    const time = {
      day: Math.floor(ms / 86400000),
      hour: Math.floor(ms / 3600000) % 24,
      min: Math.floor(ms / 60000) % 60,
      sec: Math.floor(ms / 1000) % 60,
      ms: Math.floor(ms) % 1000
    };
    return Object.entries(time)
      .filter(val => val[1] !== 0)
      .map(([key, val]) => `${val} ${key}${val !== 1 ? '(s)' : ''}`)
      .join(', ');
  },
  usd: new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }),
  int_usd: (value: number) => format.usd.format(value / 100),
  date_time: new Intl.DateTimeFormat('en-US', {
    dateStyle: "short",
    timeStyle: "medium",
    timeZone: TIME_ZONE,
  })
}
export const datatable = {
  renderer: {
    date_time: (data: string | Date, type: string, row: any, meta: any) => {
      if (type === 'display') {
        const date = new Date(data);
        if (isNaN(date.getTime())) {
          return data;
        }
        return format.date_time.format(date);
      }
      return data;
    },
    usd: (data: number, type: string, row: any, meta: any) => {
      if (type === 'display') {
        return format.usd.format(data);
      }
      return data;
    }
  },
  test: true
}
