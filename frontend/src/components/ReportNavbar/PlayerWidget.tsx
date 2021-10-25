import Icon from '../../components/shared/Icon'
import type Actor from '../../types/actor'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import { useFormContext, useWatch } from 'react-hook-form'

// @ts-ignore
import styles from "./PlayerWidget.scss"


export default function PlayerWidget({player} : {player: Actor}) {

    const field_name = `player[${player.source_id}]`

    ////////////////////////////////
    // Hooks
    // const selected = player.selected
    const selected = useWatch({ name: field_name });
    const spec = useAppSelector(state => get_spec(state, player.spec))
    const { setValue } = useFormContext();

    if (!spec) { return null }
    const wow_class = spec.class.name_slug

    ////////////////////////////////
    function onClick() {
        setValue(field_name, !selected)
    }

    ////////////////////////////////
    // Render
    return (
        <div
            className={`${styles.container} bg-dark rounded wow-${wow_class} ${selected ? "" : "disabled"}`}
            onClick={onClick}
        >
            <Icon spec={spec} size="m" />
            <span>{player.name}</span>

        </div>
    )
}
