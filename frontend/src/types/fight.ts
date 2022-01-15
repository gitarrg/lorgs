import type Actor from "./actor";


export default interface Fight {


    fight_id: number
    report_id: string
    report_url: string

    duration: number

    boss?: Actor
    players: Actor[]

    pinned?: boolean

    /** boss percent at the end of the fight */
    percent?: number

    kill?: boolean

    /** unix timestamp of the pull */
    time?: number
}

