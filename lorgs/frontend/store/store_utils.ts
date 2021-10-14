/**
 * Some shared utils used in multiple slices
 */
import type { SpellDict } from "../types/spell"

/**
 * Group spells by spell_type
 * @returns {object} spell_type: spell_ids[]
 */
export function group_spells_by_type(spells: SpellDict) {

    const spells_by_type: { [key: string] : number[] } = {}

    Object.values(spells).forEach(spell => {
        const spell_type = spell.spell_type
        spells_by_type[spell_type] = spells_by_type[spell_type] || []
        spells_by_type[spell_type].push(spell.spell_id)
    })
    return spells_by_type
}

