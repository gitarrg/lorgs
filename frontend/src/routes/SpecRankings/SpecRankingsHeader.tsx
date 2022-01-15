import HeaderLogo from './../../components/HeaderLogo'
import type Boss from '../../types/boss'
import type Spec from '../../types/spec'
import { WCL_URL } from '../../constants'
import { get_boss } from '../../store/bosses'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import { get_difficulty } from '../../store/ui'


const DIFFICULTY_IDS : {[key: string]: number} = {}
DIFFICULTY_IDS["mythic"] = 5
DIFFICULTY_IDS["heroic"] = 4
DIFFICULTY_IDS["normal"] = 3


function get_spec_ranking_url(spec: Spec, boss: Boss, difficulty: string) {

    const metric = spec.role == "heal" ? "hps" : "dps"
    const difficulty_id = DIFFICULTY_IDS[difficulty] ?? 5

    const search_params = new URLSearchParams({
        boss: boss.id.toString(),
        class: spec.class.name.replace(" ", ""),  // WCL uses no spaces in classnames
        spec: spec.name,
        metric: metric,
        difficulty: difficulty_id.toString(),
    })

    let url = new URL(WCL_URL)
    url.pathname = "/zone/rankings/28"
    url.hash = search_params.toString()
    return url.toString()
}


export default function SpecRankingsHeader({spec_slug, boss_slug} : {spec_slug: string, boss_slug: string}) {

    // hoosk
    const spec = useAppSelector(state => get_spec(state, spec_slug))
    const boss = useAppSelector(state => get_boss(state, boss_slug))
    const difficulty = useAppSelector(get_difficulty)
    if (!spec || !boss) { return null }

    // prep vars
    const spec_name = spec.full_name + "s"
    const class_name = "wow-" + spec.class.name_slug
    const url = get_spec_ranking_url(spec, boss, difficulty)

    // Render
    return (
        <h1 className="m-0 d-flex align-items-center">
            <HeaderLogo wow_class={class_name} />
            <div className="ml-2" />
            <a href={url} target="_blank">
                <span className={class_name}>{spec_name}</span>
                <span>&nbsp;vs.&nbsp;</span>
                <span className="wow-boss">{boss.full_name}</span>
            </a>
        </h1>
    )
}
