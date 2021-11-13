import Icon from '../../components/shared/Icon'
import SelectGridItem from "./SelectGrid/SelectGridItem"
import styles from "./PlayerWidget.scss"
import type Actor from '../../types/actor'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import { get_class } from '../../store/classes'


export default function PlayerWidget({player} : {player: Actor}) {

    const field_name = `player[${player.source_id}]`
    const spec = useAppSelector(state => get_spec(state, player.spec))
    const wow_class_name = spec?.class.name_slug || player.class
    const wow_class = useAppSelector(state => get_class(state, wow_class_name))
    const className = `${styles.container} wow-${wow_class_name}`

    ////////////////////////////////
    // Render
    return (
        <SelectGridItem field_name={field_name} className={className}>
            <Icon spec={spec || wow_class} size="s" />
            <span>{player.name}</span>
        </SelectGridItem>
    )
}
