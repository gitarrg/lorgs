import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { get_spell, set_spell_visible, get_spell_visible } from '../../../store/spells.js'
import { ButtonGroupContext } from '../shared/ButtonGroup.jsx'


/* to avoid react rerenders when clicking the <a> tags */
function no_link(e) {
    e.preventDefault()
}


export default function SpellButton({spec, spell_id, onClick}) {

    // Hooks
    const dispatch = useDispatch()
    const spell = useSelector(state => get_spell(state, spell_id))
    const visible = useSelector(state => get_spell_visible(state, spell.spell_id))
    const [{group_active, group_source}, set_group_active] = React.useContext(ButtonGroupContext)

    if (!spec) { return null}

    // Vars
    let wow_class = spec.class.name_slug || spec.class // if its an object or string
    const disabled = visible ? "" : "disabled"

    // onClick Callback
    function toggle_spell() {
        const new_value = !visible

        // Toggle the spell itself
        dispatch(set_spell_visible({
            spell_id: spell.spell_id,
            visible: new_value
        }))

        // if the spell became active make sure to also enable the parent group.
        // passing "child" as group_source to differenciate between clicks on the
        // group itself and triggers like these, which should only affect the
        // group itself, but not its children
        if (new_value) {
            set_group_active({group_active: new_value, group_source: "child"})
        }

        // Invoke any additional onClick Callbacks
        onClick && onClick(new_value)
    }

    // Listen to State Changes of the parent Group
    React.useEffect(() => {

        // if the state was not changed from the group level,
        // we ignore the event.
        // (eg.: the state was change from another child in the group)
        if (group_source !== "group") { return}

        // otherwise (eg.: the entire group was toggled)
        // we match the spells state to the parent state
        dispatch(set_spell_visible({
            spell_id: spell.spell_id,
            visible: group_active
        }))
    }, [group_active])

    ////////////////////////////////
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
