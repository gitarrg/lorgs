import type { FilterValues } from "./store/ui"
import type Actor from "./types/actor"
import type Fight from "./types/fight"


function id_filter(ids: number[], id: number) {
    if (ids.length === 0) { return true}
    return ids.includes(id)
}


function is_fight_visible(fight: Fight, filters: FilterValues) {

    if (fight.pinned) { return true }

    // filter based on IDs (if preset)
    if (Object.keys(filters.fight_ids).length !== 0) {
        if (!filters.fight_ids[fight.fight_id]) {
            return false
        }
    }

    let fight_duration = fight.duration / 1000  // ms to s
    if (filters.killtime.min && filters.killtime.min > fight_duration) { return false }
    if (filters.killtime.max && filters.killtime.max < fight_duration) { return false }

    return true
}


function is_player_visible(player: Actor , filters: FilterValues) {

    if (player.pinned) { return true }

    // filter based on IDs (if preset)
    if (Object.keys(filters.player_ids).length !== 0) {
        if (!filters.player_ids[player.source_id]) {
            return false
        }
    }

    if (filters["role"][player.role] === false ) { return false}
    if (filters["class"][player.class] === false ) { return false}
    if (filters["spec"][player.spec] === false ) { return false}
    if (filters["covenant"][player.covenant ?? ""] === false ) { return false}
    return true
}



const FILTERS = {
    is_fight_visible,
    is_player_visible,
}

export default FILTERS
