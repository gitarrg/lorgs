import type Boss from "./boss";


export default interface RaidZone {

    /** zone ID */
    id: number

    name: string
    name_slug: string

    /** all bosses in the zone, keyed by their full_name_slug */
    bosses: {[key: string]: Boss}
}
