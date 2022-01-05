import CollapsableSpellGroup from './CollapsableSpellGroup'
import type Boss from "../../../types/boss"
import type Class from "../../../types/class"
import type Spec from "../../../types/spec"
import { SpellTypeGroup } from "./SpellTypeGroup"
import { get_boss } from "../../../store/bosses"
import { get_class, get_class_names } from "../../../store/classes"
import { get_occuring_bosses } from "../../../store/fights"
import { get_spec } from "../../../store/specs"
import { get_type_has_used_spells } from "../../../store/spells"
import { useAppSelector } from "../../../store/store_hooks"


function get_spell_type(spell_type: string): Spec|Boss|Class {
    const spec = useAppSelector(state => get_spec(state, spell_type));
    const boss = useAppSelector(state => get_boss(state, spell_type));
    const wow_class = useAppSelector(state => get_class(state, spell_type));

    return spec || boss || wow_class;
}


function SpellGroupSpecs({icon_name} : {icon_name : string}) {

    const type = get_spell_type(icon_name)
    const has_spells = useAppSelector(state => get_type_has_used_spells(state, icon_name))
    if (!has_spells) { return null }

    // @ts-ignore
    const groups = [icon_name, ...(type?.specs || [])]

    return (
        <CollapsableSpellGroup spec={type}>
            {groups.map(group => <SpellTypeGroup key={group} spell_type={group} />)}
        </CollapsableSpellGroup>
    )
}


function BossSpells() {
    const boss_names = useAppSelector(get_occuring_bosses)
    return <>{boss_names.map(name => <SpellGroupSpecs key={name} icon_name={name} />)}</>
}


function ClassSpells() {

    let class_names = useAppSelector(get_class_names)
    class_names = class_names.filter(name => name != "other")

    // apply filters
    const class_filters = useAppSelector(state => state.ui.filters.class)
    class_names = class_names.filter(name => class_filters[name] !== false )

    return <>{class_names.map(name => <SpellGroupSpecs key={name} icon_name={name} />)}</>
}


function OtherSpells() {
    const other = useAppSelector(state => get_class(state, "other"))
    if (!other) { return null }
    return <>{other.specs.map(name => <SpellGroupSpecs key={name} icon_name={name} />)}</>
}


export default function SpellSettings() {

    return (
        <>
            <BossSpells />
            <ClassSpells />
            <OtherSpells />
        </>
    )
}
