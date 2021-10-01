// Not the actual api... but all the connections to it and some post processing


const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"


////////////////////////////////////////////////////////////////////////////////
//
//                  SPELLS
//
////////////////////////////////////////////////////////////////////////////////

export async function load_spells(groups) {

    let params = new URLSearchParams(groups.map(g => ["group", g]))
    let url ="/api/spells?" + params

    let response = await fetch(url);
    if (response.status != 200) {
        return []
    }
    let data = await response.json()
    return data
}


export function process_spells(spellsData) {
    let spells = Object.values(spellsData)

    spells.forEach(spell => {

        spell.icon_path = spell.icon.startsWith("/") ? spell.icon : `${ICON_ROOT}/${spell.icon}`

        // kind of shit.. but better then setting up all the callback stuff for image loading in konva
        spell.image = document.createElement("img")
        spell.image.src = spell.icon_path
    })

    return spells;
}

////////////////////////////////////////////////////////////////////////////////
//
//                  SpecRankings
//
////////////////////////////////////////////////////////////////////////////////




export default {
    load_spells,
    process_spells,
}


