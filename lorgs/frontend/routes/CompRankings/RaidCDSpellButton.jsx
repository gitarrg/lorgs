/* Custom Spell Button to inject some additional logic */

import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import SpellButton from '../../components/SettingsBar/SpellSettings/SpellButton.jsx'
import { get_spec_for_spell_id } from '../../store/specs.js'
import { set_filter } from '../../store/ui.js'

export default function RaidCDSpellButton({spell_id}) {

    const dispatch = useDispatch()
    const spec = useSelector(state => get_spec_for_spell_id(state, spell_id))

    function onClick(value) {
        dispatch(set_filter({
            group: "class",
            name: spec.class.name_slug,
            value: value
        }))
    }

    return <SpellButton spec={spec} spell_id={spell_id} onClick={onClick} />
}



