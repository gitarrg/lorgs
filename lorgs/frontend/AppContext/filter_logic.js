



////////////////////////////////////////////////////////////////////////////////
// FILTERS
//




////////////////////////////////////////////////////////////////////////////////
// FILTERS
//

// Filters: PLAYER

function _player_visible(filters, player) {

    // exact check against false, as undefined is considered true in this case
    if ( filters[player.covenant] === false ) {
        return false
    }

    // all checks passed
    return true
}

function _apply_filter_player(filters, player) {
        player.visible = _player_visible(filters, player)
}

// Filters: FIGHT

function _fight_visible(fight, filters) {
    let fight_duration = fight.duration / 1000
    if (filters.killtime_min && filters.killtime_min > fight_duration) { return false }
    if (filters.killtime_max && filters.killtime_max < fight_duration) { return false }
    
    // all checks passed
    return true
}
    
function _apply_filter_fight(fight, filters, f) {
        
        // check the fight itself
        fight.visible = _fight_visible(fight, filters)
        if (!fight.visible) { return}
        
        fight.players.forEach(player => { _apply_filter_player(player, filters) })
        // check again, and hide fight if all players are hidden
        fight.visible =  fight.players.some(player => player.visible)
        
        if (fight.boss) {
            fight.boss.visible = f == 0; // FIXME
            fight.visible = true
        }
    }

    // Filters ALL

export function apply_filters(fights, filters) {
    fights.forEach((fight, f) => { _apply_filter_fight(fight, filters, f) })
}


export default {};

