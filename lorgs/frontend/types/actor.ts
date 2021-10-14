
interface Cast {

    /** spell id */
    id: number

    /** timestamp */
    ts: number
}


export default interface Actor {

    class: string

    covenant?: string

    name: string

    role: string

    source_id?: number

    /** spec_slug */
    spec: string

    total: number

    pinned?: boolean

    // spec ranking
    rank?: number

    casts: Cast[]
}
