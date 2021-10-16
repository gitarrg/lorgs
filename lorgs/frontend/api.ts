// Not the actual api... but all the connections to it and some post processing


const PRINT_REQUEST_TIMES = true


export async function fetch_data(url : string, params={}) {

    if (Object.keys(params).length) {
        let search = new URLSearchParams(params)
        if (search) {
            url = url + "?" + search
        }
    }

    if ("LORRGS_BACKEND_URL" in window) {
        // @ts-ignore
        url = window.LORRGS_BACKEND_URL + url
    }
    const console_key = `request: ${url}`

    if (PRINT_REQUEST_TIMES) {console.time(console_key)}
    let response = await fetch(url);
    if (PRINT_REQUEST_TIMES) {console.timeEnd(console_key)}

    if (response.status != 200) {
        return {}
    }
    return response.json()
}
