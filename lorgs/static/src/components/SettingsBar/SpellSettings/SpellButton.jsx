import React from 'react'


export default function SpellButton(props) {


    const [show, setShow] = React.useState(props.spell.show)

    let spell = props.spell
    let group = props.spell.group
    let wow_class = group.spec.split("-")[0]
    const disabled = !show && "disabled"

    function toggle_spell() {

        // update the spell
        spell.show = !spell.show
        setShow(spell.show)

        // custom event for the Stage
        var event = new CustomEvent("toggle_spell");
        event.show = spell.show
        event.spell_id = spell.spell_id
        document.dispatchEvent(event);
    }

    
    return (
        <a href="#_" data-wowhead={spell.tooltip_info}>
            <img
                className={`button icon-s rounded wow-border-${wow_class} ${disabled}`}
                src={spell.icon_path}
                data-spell_id={spell.spell_id}
                onClick={toggle_spell}
            />
        </a>
    )
}
