

import React from 'react'
import { useInterval } from 'react-use'
import { fetch_data } from '../../api'


async function ping() {
    return fetch_data("/api/ping")
}


export default function AdminPing() {

    const inverval = 500


    useInterval(ping, inverval);

    return (
        <div>

        </div>
    )
}


