import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { get_spec_for_spell_id } from '../../../store/specs.js'
import { get_spell, set_spell_visible, get_spell_visible } from '../../../store/spells.js'


/* to avoid react rerenders when clicking the <a> tags */
function no_link(e) {
    e.preventDefault()
}


export default function SpellButton({spec, spell_id}) {


    // Hooks
    const dispatch = useDispatch()
    const spell = useSelector(state => get_spell(state, spell_id))
    spec = spec || useSelector(state => get_spec_for_spell_id(state, spell_id))
    const visible = useSelector(state => get_spell_visible(state, spell.spell_id))

    if (!spec) { return null}

    // Vars
    let wow_class = spec.class.name_slug
    const disabled = visible ? "" : "disabled"

    // onClick Callback
    function toggle_spell() {

        dispatch(set_spell_visible({
            spell_id: spell.spell_id,
            visible: !visible
        }))
    }

    // Render
    return (
        <a onClick={no_link} href="" data-wowhead={spell.tooltip_info}>
            <img
                className={`button icon-s rounded wow-border-${wow_class} ${disabled}`}
                src={spell.icon_path}
                data-spell_id={spell.spell_id}
                onClick={toggle_spell}
            />
        </a>
    )
}
