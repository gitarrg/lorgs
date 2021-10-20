

// FIXME: why does this take ms?
export function toMMSS(seconds: number) {

    seconds = seconds.toFixed(0)
    let sign = ""
    if (seconds < 0) { // events that occur prepull
        seconds *= -1.0;
        sign = "-"
    }
    const str = new Date(seconds * 1000).toISOString().substr(14, 5);
    return `${sign}${str}`
}


// convert a time "1:23" to seconds
export function time_to_seconds(text: string) {

    const regex = /(?<minutes>\d+):(?<seconds>\d{2})/
    const found = text.match(regex)
    if (!found?.groups) {return}
    return parseInt(found.groups.minutes) * 60 + parseInt(found.groups.seconds)
}

/**
 * Formats a number in seconds into a time string with minutes and seconds.
 */
export function seconds_to_time(seconds: number, {padding=true}) {
    let text = new Date(seconds * 1000).toISOString().substr(14, 5);
    if(!padding && text.charAt(0) === '0') { text = text.substring(1); } // remove leading 0
    return text;
}

/**
 * Format a large number using "k" for thousands
 * @param n the number to format
 * @param digits decimal places
 * @returns string
 */
// based on: https://stackoverflow.com/a/9461657
export function kFormatter(n: number, digits=2) {

    if (n > 999) {
        return(n/1000).toFixed(digits) + "k"
    }
    return n.toFixed(0);
}

export function slug(str: string) {
    return str
        .replace(/^\s+|\s+$/g, '')   // trim
        .toLowerCase()
        .replace(/[^a-z0-9 -]/g, '') // Remove invalid chars
        .replace(/\s+/g, '-')        // Collapse whitespace and replace by -
        .replace(/-+/g, '-');        // Collapse dashes
}