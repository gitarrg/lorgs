import Actor from '../../types/actor'
import Icon from '../../components/shared/Icon'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import { useFormContext, useWatch } from 'react-hook-form'

// @ts-ignore
import styles from "./PlayerWidget.scss"


export default function PlayerWidget({player} : {player: Actor}) {

    const attr_name = `players[${player.source_id}]`

    ////////////////////////////////
    // Hooks
    const { setValue } = useFormContext();
    const is_selected = useWatch({name: attr_name})
    const spec = useAppSelector(state => get_spec(state, player.spec))

    if (!spec) { return null }
    const wow_class = spec.class.name_slug

    ////////////////////////////////
    function toggle_selection() {
        setValue(attr_name, !is_selected)
    }

    ////////////////////////////////
    // Render
    return (
        <div
            className={`${styles.container} bg-dark rounded wow-${wow_class} ${is_selected ? "" : "disabled"}`}
            onClick={toggle_selection}
        >
            <Icon spec={spec} size="m" />
            <span>{player.name}</span>

        </div>
    )
}
