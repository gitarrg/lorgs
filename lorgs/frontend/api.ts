// Not the actual api... but all the connections to it and some post processing


const PRINT_REQUEST_TIMES = true


export async function fetch_data(url : string, params={}) {

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
    return response.json()
}


////////////////////////////////////////////////////////////////////////////////


export async function load_spec(spec_slug) {
    return fetch_data(`/api/specs/${spec_slug}`);
}


export async function load_multiple_specs(specs=[]) {
    let calls = specs.map(spec => load_spec(spec))
    let data = await Promise.all(calls)
    return data
}

////////////////////////////////////////////////////////////////////////////////
//
//                  SPELLS
//
////////////////////////////////////////////////////////////////////////////////

export async function load_spells(groups? : string[]) {

    let params = new URLSearchParams(groups.map(g => ["group", g]))
    let url ="/api/spells?" + params

    return fetch_data(url);
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


export function process_fetched_data(state) {

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



