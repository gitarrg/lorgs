

export default interface Cast {

    /** spell id */
    id: number

    /** timestamp */
    ts: number

    /** optional duration, only set for spells that have no constant time  */
    d?: number

    /** counter, to indicate how many times the same spell was cast */
    counter?: number
}
