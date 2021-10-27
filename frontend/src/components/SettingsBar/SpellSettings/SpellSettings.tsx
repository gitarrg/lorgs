import { get_bosses } from "../../../store/bosses"
import { get_spell_types } from "../../../store/spells"
import { useAppSelector } from "../../../store/store_hooks"
import { SpellTypeGroup } from "./SpellTypeGroup"



export default function SpellSettings() {
    const all_spell_types = useAppSelector(get_spell_types)

    const bosses = useAppSelector(get_bosses)
    const boss_names = Object.keys(bosses)

    // ensure boss spells are listed first
    const spell_types = [
        ...boss_names,
        ...all_spell_types.filter(type => !boss_names.includes(type))
    ]

    // Render
    return (
        <>
            {spell_types.map(spell_type =>
                <SpellTypeGroup
                    key={spell_type}
                    spell_type={spell_type}
                />
            )}
        </>
    )
}
