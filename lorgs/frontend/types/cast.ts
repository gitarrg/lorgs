

export default interface Cast {

    /** spell id */
    id: number

    /** timestamp */
    ts: number

    /** counter, to indicate how many times the same spell was cast */
    counter?: number
}
