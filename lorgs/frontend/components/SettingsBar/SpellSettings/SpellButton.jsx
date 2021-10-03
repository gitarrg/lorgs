import React from 'react'


/* to avoid react rerenders when clicking the <a> tags */
function no_link(e) {
    e.preventDefault()
}


export default function SpellButton({spec, spell}) {

    if (spell.was_used === false) {return null}

    const [show, setShow] = React.useState(spell.show)
    let wow_class = spec.class.name_slug
    const disabled = !show && "disabled"

    function toggle_spell() {

        // update the spell
        spell.show = !spell.show
        setShow(spell.show)

        // custom event for the Stage
        let event = new CustomEvent("toggle_spell");
        event.show = spell.show
        event.spell_id = spell.spell_id
        document.dispatchEvent(event);
    }

    
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
