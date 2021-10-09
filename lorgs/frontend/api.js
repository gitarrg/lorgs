// Not the actual api... but all the connections to it and some post processing


const PRINT_REQUEST_TIMES = true


const API = {}
export default API


async function fetch_data(url, params={}) {


    if (Object.keys(params).length) {
        let search = new URLSearchParams(params)
        if (search) {
            url = url + "?" + search
        }
    }

    const console_key = `request: ${url}`

    if (PRINT_REQUEST_TIMES) {console.time(console_key)}
    let response = await fetch(url);
    if (PRINT_REQUEST_TIMES) {console.timeEnd(console_key)}

    if (response.status != 200) {
        return {}
    }
    return await response.json()
}


////////////////////////////////////////////////////////////////////////////////


API.load_roles = async function() {
    let roles = await fetch_data("/api/roles")
    roles = roles.roles // take array from dict
    roles.sort((a, b) => (a.id > b.id) ? 1 : -1  )
    return roles;
}


API.load_specs = async function({include_spells = false} = {}) {
    const specs = await fetch_data("/api/specs", { include_spells: include_spells });
    return specs.specs || []
}


API.load_spec = async function(spec_slug) {
    return await fetch_data(`/api/specs/${spec_slug}`);
}


API.load_multiple_specs = async function(specs=[]) {
    let calls = specs.map(spec => API.load_spec(spec))
    let data = await Promise.all(calls)
    return data
}


API.load_bosses = async function() {
    const zone_info = await fetch_data(`/api/bosses`);
    return zone_info.bosses || []
}


API.load_boss = async function(boss_slug) {
    return await fetch_data(`/api/boss/${boss_slug}`);
}


////////////////////////////////////////////////////////////////////////////////
//
//                  SPELLS
//
////////////////////////////////////////////////////////////////////////////////

API.load_spells = async function(groups = []) {

    let params = new URLSearchParams(groups.map(g => ["group", g]))
    let url ="/api/spells?" + params

    return await fetch_data(url);
}




////////////////////////////////////////////////////////////////////////////////
//
//                  PAGE RELATED
//
////////////////////////////////////////////////////////////////////////////////

/* Returns a list of fights */
API.load_spec_rankings = async function(spec_slug, boss_slug) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=100`;
    const fight_data = await fetch_data(url);

    // post process
    return fight_data.fights.map((fight, i) => {
        fight.players.forEach(player => {
            player.rank = i+1  // insert ranking data
        })
        return fight
    })
}


////////////////////////////////////////////////////////////////////////////////
//
//                  Post Processing
//
////////////////////////////////////////////////////////////////////////////////

function filter_unused_spells(spells = [], fights = []) {

    if (!spells) { return []}
    if (!fights) { return []}

    let used_spells = new Set()
    fights.forEach(fight => {

        if (fight.boss && fight.boss.casts) {
            fight.boss.casts.forEach(cast => {
                used_spells.add(cast.id)
            })
        }

        (fight.players || []).forEach(player => {
            (player.casts || []).forEach(cast => {
                used_spells.add(cast.id)
            })
        })
    })

    spells.forEach(spell => spell.was_used = used_spells.has(spell.spell_id))
    return spells.filter(spell => spell.was_used)
}


API.process_fetched_data = function(state) {

    // backref the spec on each spell
    Object.values(state.specs).forEach(spec => {
        spec.spells.forEach(spell => {
            spell.spec = spec
        })
    })

    // build flat list of spells
    state.spells = [] 
    state.spells = [...state.boss.spells]
    Object.values(state.specs).forEach(spec => {
        state.spells = [...state.spells, ...(spec.spells || [])]
    })

    // filter out duplicates (eg.: class spells that occur on multiple specs)
    state.spells = [...new Map(state.spells.map(spell => [spell["spell_id"], spell])).values()];

    // apply some filtering
    state.spells = filter_unused_spells(state.spells, state.fights)

    // additional loading
    process_spells(state.boss.spells)
    state.specs.forEach(spec => process_spells(spec.spells))

    return state
}
