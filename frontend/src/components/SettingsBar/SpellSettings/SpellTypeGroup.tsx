import { get_boss } from "../../../store/bosses";
import { get_class } from "../../../store/classes";
import { get_spec } from "../../../store/specs";
import { get_spells_for_type, get_used_spells } from "../../../store/spells";
import { useAppSelector } from "../../../store/store_hooks";
import type Boss from "../../../types/boss";
import type Class from "../../../types/class";
import type Spec from "../../../types/spec";
import ButtonGroup from "../shared/ButtonGroup";
import SpellButton from "./SpellButton";
import RaidCDButton from "./RaidCDButton";


export type SpellTypeGroupProps = {
    spell_type: string
}


function get_spell_type(spell_type: string): Spec|Boss|Class {
    const spec = useAppSelector(state => get_spec(state, spell_type));
    const boss = useAppSelector(state => get_boss(state, spell_type));
    const wow_class = useAppSelector(state => get_class(state, spell_type));

    return spec || boss || wow_class;
}



function create_spell_button(name_slug: string, spec: Spec|Boss|Class, spell_id: number) {

    const key = `${name_slug}/${spell_id}`

    if (spec.full_name_slug && spec.full_name_slug === "other-raid") {
        return <RaidCDButton key={key} spell_id={spell_id} />
    }
    return <SpellButton key={key} spell_id={spell_id} spec={spec} />

}


export function SpellTypeGroup({ spell_type }: SpellTypeGroupProps) {

    // the spell type can be a Spec, Boss or Class

    const type = get_spell_type(spell_type)

    const type_spells = useAppSelector(state => get_spells_for_type(state, spell_type));
    const used_spells = useAppSelector(get_used_spells)
    const used_type_spells = type_spells.filter(spell_id => used_spells.includes(spell_id))

    if (!type) {
        console.warn("unknown type:", type)
        return null;
    }
    if (used_type_spells.length === 0) {
        return null;
    }

    const name_slug = type.class?.name_slug || type.full_name_slug || type.name_slug
    const className=`wow-${name_slug}`


    return (
        <ButtonGroup name={type.name} side="left" className={className}>
            {used_type_spells.map(spell_id => create_spell_button(name_slug, type, spell_id))}

        </ButtonGroup>
    );
}
