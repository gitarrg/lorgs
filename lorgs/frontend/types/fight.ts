import Actor from "./actor";
import BossActor from "./boss_actor";


interface Fight {


    fight_id: number
    report_id: string
    report_url: string

    duration: number

    boss: BossActor
    players: Actor[]

    pinned?: boolean

}


export default Fight


