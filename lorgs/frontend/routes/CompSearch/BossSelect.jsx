/* Component to select which boss to display */


import { useSelector } from 'react-redux'
import { useFormContext, useWatch } from "react-hook-form";


/* Button to select a single boss */
function BossButton({boss}) {

    // State Vars
    const form_methods = useFormContext();
    const selected_boss_name_slug = useWatch({name: "boss_name_slug"})

    // Constants
    const icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
    const is_active = (selected_boss_name_slug == boss.full_name_slug ? "active" : "")

    function onClick() {
        form_methods.setValue("boss_name_slug", boss.full_name_slug)
    }

    // Render
    return (
        <img
            className={`boss-button icon-spec icon-m border-black rounded ${is_active}`}
            src={icon_path}
            alt={boss.name}
            data-tip={boss.full_name}
            alt={boss.full_name}
            onClick={onClick}
        />
    )
}

/* Group of Buttons to allow the user to choose a Boss */
export default function BossSelect() {
    const bosses = useSelector(state => state.bosses)

    return (

        <div className="boss-search-container ml-auto">
            <h4 className="mb-0">Boss:</h4>

            <div className="boss-button-container bg-dark p-1 rounded border">
                {bosses.map(boss => 
                    <BossButton
                        key={boss.full_name_slug}
                        boss={boss}
                    />
                )}
            </div>
        </div>
    )
}
