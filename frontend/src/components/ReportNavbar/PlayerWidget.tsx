import Icon from '../../components/shared/Icon'
import SelectGridItem from "./SelectGrid/SelectGridItem"
import styles from "./PlayerWidget.scss"
import type Actor from '../../types/actor'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'


export default function PlayerWidget({player} : {player: Actor}) {

    const field_name = `player[${player.source_id}]`
    const spec = useAppSelector(state => get_spec(state, player.spec))
    if (!spec) { return null }

    const className = `${styles.container} wow-${spec.class.name_slug}`

    ////////////////////////////////
    // Render
    return (
        <SelectGridItem field_name={field_name} className={className}>
            <Icon spec={spec} size="s" />
            <span>{player.name}</span>
        </SelectGridItem>
    )
}
