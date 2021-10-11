

const FILTERS = {}


FILTERS.is_fight_visible = function(fight, filters) {

    if (fight.pinned) { return true }

    let fight_duration = fight.duration / 1000  // ms to s
    if (filters.killtime.min && filters.killtime.min > fight_duration) { return false }
    if (filters.killtime.max && filters.killtime.max < fight_duration) { return false }

    return true
}


FILTERS.is_player_visible = function(player = {}, filters = {}) {

    if (player.pinned) { return true }

    if (filters["role"][player.role] === false ) { return false}
    if (filters["class"][player.class] === false ) { return false}
    if (filters["spec"][player.spec] === false ) { return false}
    if (filters["covenant"][player.covenant] === false ) { return false}
    return true
}


export default FILTERS
