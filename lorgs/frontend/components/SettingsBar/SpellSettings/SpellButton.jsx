import React from 'react'


export default function SpellButton({spec, spell}) {

    if (spell.was_used === false) {return null}

    const [show, setShow] = React.useState(spell.show)
    let wow_class = spec.full_name_slug.split("-")[0]  // TODO: include class_name in api?
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
