import Actor from "./types/actor"
import Fight from "./types/fight"




function is_fight_visible(fight: Fight, filters = {}) {

    if (fight.pinned) { return true }

    let fight_duration = fight.duration / 1000  // ms to s
    if (filters.killtime.min && filters.killtime.min > fight_duration) { return false }
    if (filters.killtime.max && filters.killtime.max < fight_duration) { return false }

    return true
}


function is_player_visible(player: Actor , filters = {}) {

    if (player.pinned) { return true }

    if (filters["role"][player.role] === false ) { return false}
    if (filters["class"][player.class] === false ) { return false}
    if (filters["spec"][player.spec] === false ) { return false}
    if (filters["covenant"][player.covenant] === false ) { return false}
    return true
}



const FILTERS = {
    is_fight_visible,
    is_player_visible,
}

export default FILTERS
