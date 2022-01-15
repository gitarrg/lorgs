import type { FilterValues } from "./store/ui"
import type Actor from "./types/actor"
import type Fight from "./types/fight"


function is_fight_visible(fight: Fight, filters: FilterValues) {

    if (fight.pinned) { return true }

    let fight_duration = fight.duration / 1000  // ms to s
    if (filters.killtime.min && filters.killtime.min > fight_duration) { return false }
    if (filters.killtime.max && filters.killtime.max < fight_duration) { return false }

    const has_boss = fight.boss && is_player_visible(fight.boss, filters)
    return has_boss || fight.players.some(player => is_player_visible(player, filters))
}


function is_player_visible(player: Actor , filters: FilterValues) {

    if (player.pinned) { return true }

    if (filters["role"][player.role] === false ) { return false}
    if (filters["class"][player.class] === false ) { return false}
    if (filters["spec"][player.spec] === false ) { return false}
    if (filters["covenant"][player.covenant ?? ""] === false ) { return false}

    const casts = player.casts
    return casts.length > 0
}


const FILTERS = {
    is_fight_visible,
    is_player_visible,
}

export default FILTERS
