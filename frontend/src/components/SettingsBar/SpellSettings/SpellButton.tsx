import { MouseEvent, useContext, useEffect } from 'react'
import { useDispatch } from 'react-redux'

import { get_spell, set_spell_visible, get_spell_visible } from '../../../store/spells'
import { ButtonGroupContext } from '../shared/ButtonGroup'
import type Spec from '../../../types/spec'
import type Boss from '../../../types/boss'
import { useAppSelector } from '../../../store/store_hooks'

import styles from "./SpellButton.scss"
import Class from '../../../types/class'
import { get_spec_for_spell_id } from '../../../store/specs'


/* to avoid react rerenders when clicking the <a> tags */
function no_link(e: MouseEvent<HTMLAnchorElement> ) {
    e.preventDefault()
}

const WARNING_SIGN = "⚠️"
const DYNAMIC_CD_WARNING = (
    <div
        className="dynamic_cd_warning"
        data-tooltip="The displayed Cooldown for this spell is not exact and only shows an estimate."
        data-tooltip-size="small"
    >{WARNING_SIGN}</div>
)

export default function SpellButton({spec, spell_id, onClick} : { spec: Spec|Boss|Class, spell_id: number, onClick?: Function } ) {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    //
    const dispatch = useDispatch()
    const spell = useAppSelector(state => get_spell(state, spell_id))
    const visible = useAppSelector(state => get_spell_visible(state, spell_id))
    const group_context = useContext(ButtonGroupContext)

    // hack for raid cd's, which are listed as 
    // const spec2 = useAppSelector(state => get_spec_for_spell_id(state, spell_id))
    // console.log({spec})
    // if (spec.full_name_slug == "other-raid") {
    //     spec = spec2
    // }

    ////////////////////////////////////////////////////////////////////////////
    // Vars
    //
    let wow_class = spec.class?.name_slug || spec.name_slug
    const disabled = visible ? "" : "disabled"
    const dynamic_cd = spell.tags?.includes("dynamic_cd")// ? "dynamic_cd" : "";

    ////////////////////////////////////////////////////////////////////////////

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
        if (new_value && group_context.setter) {
            group_context.setter({active: new_value, source: "child"})
        }

        // Invoke any additional onClick Callbacks
        onClick && onClick(new_value)
    }

    // Listen to State Changes of the parent Group
    useEffect(() => {

        // if the state was not changed from the group level,
        // we ignore the event.
        // (eg.: the state was change from another child in the group)
        if (group_context.source !== "group") { return}

        // otherwise (eg.: the entire group was toggled)
        // we match the spells state to the parent state
        dispatch(set_spell_visible({
            spell_id: spell.spell_id,
            visible: group_context.active
        }))

        // Invoke any additional onClick Callbacks
        onClick && onClick(group_context.active)

    }, [group_context.active])

    if (!spell) { return null }
    if (!spec) { return null }

    ////////////////////////////////
    // Render
    return (
        <div className={styles.spell_button}>
        <a data-wowhead={spell.tooltip_info}>
            <img
                className={`button icon-s rounded wow-border-${wow_class} ${disabled}`}
                src={spell.icon_path}
                data-spell_id={spell.spell_id}
                onClick={toggle_spell}
            />
        </a>

        {visible && dynamic_cd && DYNAMIC_CD_WARNING}

        </div>
    )
}
