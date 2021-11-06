import { get_roles } from "../../store/roles"
import { get_spec, load_spec_spells } from "../../store/specs"
import { useAppSelector } from "../../store/store_hooks"
import { NavLink, useRouteMatch, Route, useParams } from 'react-router-dom';
import { get_spell } from "../../store/spells";
import Spec from "../../types/spec";
import { useDispatch } from 'react-redux'
import { get_is_loading } from "../../store/ui";

import styles from "./AdminSpells.scss"

////////////////////////////////////////////////////////////////////////////////
// SubNav
//

function SpecButton({spec_slug=""}) {

    const spec = useAppSelector(state => get_spec(state, spec_slug))
    const {url } = useRouteMatch()
    if (!spec) { return null }

    return (
        <NavLink to={`${url}/${spec_slug}`} className={styles.spec_button} activeClassName="active">
            <img className={`icon-m wow-border-${spec.class.name_slug}`} src={spec.icon_path} />
        </NavLink>
    )
}


function AdminSpellsSubNav() {

    const roles = useAppSelector(state => get_roles(state))

    return (
        <div className="d-flex">
            {Object.values(roles).map(role =>
                <div key={role.code} className="mr-4">
                    {role.specs.map(spec_slug =>
                        <SpecButton key={spec_slug} spec_slug={spec_slug} />
                    )}
                </div>
            )}
        </div>
    )
}

////////////////////////////////////////////////////////////////////////////////
// Spell Display
//
function SpellRow({spell_id, spec} : {spell_id: number, spec: Spec } ) {

    const spell = useAppSelector(state => get_spell(state, spell_id))
    if (!spell) { return null }




    return (
        <tr>
            <td>
                <a data-wowhead={spell.tooltip_info}>
                    <img src={spell.icon_path} className={`icon-s button rounded`}/>
                </a>
            </td>
            <td className="text-monospace">{spell_id}</td>
            <td>{spell.name}</td>
            <td>{spell.cooldown}</td>
            <td>{spell.duration}</td>

        </tr>
    )
}

function SpellTypeRows({spec, spell_type} : { spec: Spec, spell_type: string}) {

    const spell_ids = spec.spells_by_type[spell_type]

    return (
        <>
        <tr>
            <th colSpan={99} className={`wow-${spec.class.name_slug}`}>
                { spell_type }
            </th>
        </tr>
        {spell_ids.map(spell_id =>
            <SpellRow key={spell_id} spec={spec} spell_id={spell_id} />
        )}
        </>
    )
}

function SpellDisplay() {

    const { spec_slug } : { spec_slug: string } = useParams()
    const spec = useAppSelector(state => get_spec(state, spec_slug))
    const dispatch = useDispatch()
    const is_loading = useAppSelector(state => get_is_loading(state))

    if (!spec) { return null }

    if (!spec.loaded && !is_loading) {

        console.log("loading spec:", spec.full_name_slug)
        dispatch(load_spec_spells(spec.full_name_slug))
    }

    const spell_types = sort_spell_types(Object.keys(spec.spells_by_type ?? {}))

    return (
        <table className={styles.spell_table}>
            <thead>
                <tr>
                    <th>&nbsp;</th>
                    <th>Spell ID</th>
                    <th>Name</th>
                    <th>Duration</th>
                    <th>Cooldown</th>
                </tr>
            </thead>

            <tbody>
                {spell_types.map(spell_type =>
                    <SpellTypeRows key={spell_type} spec={spec} spell_type={spell_type}/>
                )}
            </tbody>
        </table>
    )
}



////////////////////////////////////////////////////////////////////////////////
// Main
//


export default function AdminSpells() {

    // const spec_slug = "not set"
    const { path } = useRouteMatch()

    return (
        <div>
            <div className="p-2 bg-dark rounded border d-flex">
            <AdminSpellsSubNav />
            </div>

            <div className="p-2 bg-dark rounded border d-flex mt-3">
                <Route path={`${path}/:spec_slug`}>
                    <SpellDisplay />
                </Route>
            </div>
        </div>
    )
}
