import ButtonGroup from "./shared/ButtonGroup"
import FilterButton from "./shared/FilterButton"
import { get_boss } from "../../store/bosses"
import { get_occuring_bosses, get_occuring_specs } from "../../store/fights"
import { get_spec } from "../../store/specs"
import { set_filter } from "../../store/ui"
import { useAppSelector, useAppDispatch } from "../../store/store_hooks"


function BossFilterButton({name} : {name: string}) {

    const boss = useAppSelector(state => get_boss(state, name))
    const zone = "sanctum-of-domination"  // FIXME
    const dispatch = useAppDispatch()
    if (!boss) { return null }

    function onClick({value} : {value: boolean}) {
        dispatch(set_filter({ group: "spec", name: name, value: value }))
    }

    return (
        <FilterButton
            onClick={onClick}
            name="boss"
            full_name={boss.full_name}
            icon_name={`bosses/${zone}/${boss.full_name_slug}`}
        />
    )
}


function SpecFilterButton({spec_name} : {spec_name : string}) {

    const spec = useAppSelector(state => get_spec(state, spec_name))
    const dispatch = useAppDispatch()
    if (!spec) { return null }

    const class_name = spec_name.split("-")[0]

    function onClick({value} : {value: boolean}) {
        dispatch(set_filter({ group: "spec", name: spec_name, value: value }))
    }


    return (
        <FilterButton
            onClick={onClick}
            name={class_name}
            full_name={spec.full_name}
            icon_name={`specs/${spec_name}`}
        />
    )
}


export default function SpecSettings() {

    const specs = useAppSelector(get_occuring_specs)
    const bosses = useAppSelector(get_occuring_bosses)

    return (<>
        <ButtonGroup name="Boss" className="wow-boss">
            {bosses.map(name => 
                <BossFilterButton key={name} name={name} />
            )}
        </ButtonGroup>

        <ButtonGroup name="Specs">
            {specs.map(name =>
                <SpecFilterButton key={name} spec_name={name} />
            )}
        </ButtonGroup>
    </>)
}
