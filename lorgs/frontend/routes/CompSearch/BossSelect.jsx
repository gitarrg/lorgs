/* Component to select which boss to display */


import { useSelector } from 'react-redux'
import { useFormContext, useWatch } from "react-hook-form";
import { get_bosses } from '../../store/bosses';



/* Button to select a single boss */
function BossButton({boss}) {

    // State Vars
    const form_methods = useFormContext();
    const selected_boss_name_slug = useWatch({name: "boss_name_slug"})

    // Constants
    const is_active = (selected_boss_name_slug == boss.full_name_slug ? "active" : "")

    function onClick() {
        form_methods.setValue("boss_name_slug", boss.full_name_slug)
    }

    // Render
    return (
        <img
            className={`boss-button icon-spec icon-m border-black rounded ${is_active}`}
            src={boss.icon_path}
            alt={boss.name}
            data-tip={boss.full_name}
            alt={boss.full_name}
            onClick={onClick}
        />
    )
}

/* Group of Buttons to allow the user to choose a Boss */
export default function BossSelect() {

    const bosses = useSelector(state => get_bosses(state))


    return (

        <div className="boss-search-container ml-auto">
            <h4 className="mb-0">Boss:</h4>

            <div className="boss-button-container bg-dark p-1 rounded border">
                {Object.values(bosses).map(boss =>
                    <BossButton
                        key={boss.full_name_slug}
                        boss={boss}
                    />
                )}
            </div>
        </div>
    )
}
