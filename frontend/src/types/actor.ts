import type Cast from "./cast";
import type Death from "./death";


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

    deaths: Death[]

    pinned?: boolean

    // spec ranking
    rank?: number
}
