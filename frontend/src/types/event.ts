
/** Generic Event used for things like DeathEvents, Resurctions
 * and maybe other nieche features in the future */
export default interface Event {

    /** timestamp */
    ts: number

    /** spell info */
    spell_id?: number
    spell_icon?: string
    spell_name?: string

    /** source player info */
    source_id?: number
    source_name?: number
    source_class?: number
}
