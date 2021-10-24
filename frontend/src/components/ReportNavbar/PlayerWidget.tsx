import Icon from '../../components/shared/Icon'
import type Actor from '../../types/actor'
import { get_spec } from '../../store/specs'
import { get_player_selected, player_selected } from '../../store/user_reports'
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'

// @ts-ignore
import styles from "./PlayerWidget.scss"


export default function PlayerWidget({player} : {player: Actor}) {

    ////////////////////////////////
    // Hooks
    // const selected = player.selected
    const selected = useAppSelector(state => get_player_selected(state, player.source_id))
    const spec = useAppSelector(state => get_spec(state, player.spec))
    const dispatch = useAppDispatch()

    if (!spec) { return null }
    const wow_class = spec.class.name_slug

    ////////////////////////////////
    function onClick() {
        dispatch(player_selected({
            source_id: player.source_id,
            selected: !selected,
        }))
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
