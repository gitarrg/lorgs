import ButtonGroup from '../shared/ButtonGroup'
import FilterButton from '../shared/FilterButton'
import { set_filter } from '../../../store/ui'
import { useAppDispatch } from '../../../store/store_hooks'


function FilterCovenantButton({covenant} : {covenant: string}) {

    // Hooks
    const covenant_slug = covenant.toLowerCase()
    const dispatch = useAppDispatch()

    function onClick({value}: {value: boolean}) {
        dispatch(set_filter({ group: "covenant", name: covenant_slug, value: value }))
    }

    // Render
    return (
        <FilterButton
            key={covenant_slug}
            onClick={onClick}
            name={covenant_slug}
            full_name={covenant}
            icon_name={`covenants/${covenant_slug}`}
        />
    )
}


export default function FilterCovenantGroup() {
    return (
        <ButtonGroup name="Covenant">
            <FilterCovenantButton covenant="Kyrian" />
            <FilterCovenantButton covenant="Venthyr" />
            <FilterCovenantButton covenant="Nightfae" />
            <FilterCovenantButton covenant="Necrolord" />
        </ButtonGroup>
    )
}
