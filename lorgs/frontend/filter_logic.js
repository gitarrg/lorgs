

const FILTERS = {}



FILTERS.is_fight_visible = function(fight, filters) {


}


FILTERS.is_player_visible = function(player = {}, filters = {}) {

    // console.log("player_visible", player, filters)
    if (filters["role"][player.role] === false ) { return false}
    if (filters["class"][player.class] === false ) { return false}
    if (filters["spec"][player.spec] === false ) { return false}
    if (filters["covenant"][player.covenant] === false ) { return false}
    // if (player.role !== "heal") { return false }
    return true
}


export default FILTERS
