import type Cast from "./cast";
import type Event from "./event";


export default interface Actor {

    class: string

    covenant?: string

    name: string

    role: string

    source_id?: number

    /** spec_slug */
    spec: string

    total: number

    casts: Cast[]

    deaths: Event[]
    resurrects: Event[]

    pinned?: boolean

    // spec ranking
    rank?: number
}
