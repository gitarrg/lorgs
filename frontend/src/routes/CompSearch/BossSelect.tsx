/* Component to select which boss to display */

import FormGroup from './FormGroup';
import WebpImg from "../../components/WebpImg";
import type Boss from '../../types/boss';
import { get_bosses } from '../../store/bosses';
import { useAppSelector } from '../../store/store_hooks';
import { useFormContext, useWatch } from "react-hook-form";



/* Button to select a single boss */
function BossButton({boss} : {boss: Boss}) {

    // State Vars
    const form_methods = useFormContext();
    const selected_boss_name_slug = useWatch({name: "boss_name_slug"})

    // Constants
    const is_selected = (selected_boss_name_slug == boss.full_name_slug ? "active" : "")

    function onClick() {
        form_methods.setValue("boss_name_slug", boss.full_name_slug)
    }

    // Render
    return (
        <div data-tooltip={boss.full_name}>
            <WebpImg
                className={`boss-button icon-spec icon-m border-black rounded ${is_selected}`}
                src={boss.icon_path}
                alt={boss.name}
                onClick={onClick}
            />
        </div>
    )
}

/* Group of Buttons to allow the user to choose a Boss */
export default function BossSelect() {

    const bosses = useAppSelector(state => get_bosses(state))


    return (
        <FormGroup name="Boss:" className="boss-button-container">
            {Object.values(bosses).map(boss =>
                <BossButton
                key={boss.full_name_slug}
                boss={boss}
                />
            )}
        </FormGroup>
    )
}
