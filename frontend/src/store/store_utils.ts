/**
 * Some shared utils used in multiple slices
 */
import type Spec from "../types/spec"
import type { SpellDict } from "../types/spell"
import type Spell from "../types/spell"


// spell types that will be combined with the main spec
const COMBINED_TYPES = ["raid", "external", "defensive"]


function _get_spell_group(spell: Spell, spec: Spec) {
    const spell_type = spell.spell_type

    // "other-potions" and "other-trinkets"
    if (spell_type.startsWith("other-")) { return spell_type }

    // for now, we don't split class and spec spells as it looks weird
    if (spell_type == spec.class.name_slug) { return spec.full_name_slug }

    // main group
    const main_types = [spec.full_name_slug, ...COMBINED_TYPES]
    if (main_types.includes(spell_type)) { return spec.full_name_slug }

    // fallback
    return "other-buffs";
}


/** Sort all spells the Spec can use into some logical Groups.
 *
 * Primarily this is to split the class/spec's own spells
 * from shared spells like Trinkets, Potions or external buffs like Power Infusion, Ferries and Bloodlust
 */
export function group_spells_by_type(spells: SpellDict, spec: Spec) {

    const spells_by_type: { [key: string] : number[] } = {}

    Object.values(spells).forEach(spell => {
        const spell_type = _get_spell_group(spell, spec)
        spells_by_type[spell_type] = spells_by_type[spell_type] || []
        spells_by_type[spell_type].push(spell.spell_id)
    })
    return spells_by_type
}

