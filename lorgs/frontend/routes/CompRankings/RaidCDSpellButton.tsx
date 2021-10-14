/* Custom Spell Button to inject some additional logic */

import SpellButton from '../../components/SettingsBar/SpellSettings/SpellButton'
import { get_spec_for_spell_id } from '../../store/specs'
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { set_filter } from '../../store/ui'

export default function RaidCDSpellButton({spell_id} : { spell_id: number}) {

    const dispatch = useAppDispatch()
    const spec = useAppSelector(state => get_spec_for_spell_id(state, spell_id))
    if (!spec) { return null}

    function onClick(value: boolean) {
        dispatch(set_filter({
            group: "class",
            name: spec?.class.name_slug,
            value: value
        }))
    }

    return <SpellButton spec={spec} spell_id={spell_id} onClick={onClick} />
}



