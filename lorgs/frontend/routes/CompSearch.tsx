/* Page/Form to search for specific Comps*/

import React from 'react'
import { useHistory } from 'react-router-dom';
import { useForm, FormProvider } from "react-hook-form";

import BossSelect from './CompSearch/BossSelect'
import BossSelection from './CompSearch/BossSelection'
import PlayerRoleSearch from './CompSearch/PlayerRoleSearch'
import PlayerSelection from './CompSearch/PlayerSelection'
import PlayerSpecSearch from './CompSearch/PlayerSpecSearch'
import SearchSubmitButton from './CompSearch/SearchSubmitButton'
import KilltimeGroup from './CompSearch/KilltimeGroup';


/* Takes the form data dict and generates the search string.*/
function build_search_string(from_data) {

    let search = new URLSearchParams()

    ////////////////////////////////////////
    // Get Filters for roles and specs
    const types = ["role", "spec"]
    types.forEach(type => {

        const items = from_data[type]
        for (const [key, {count, op}] of Object.entries(items)) {
            if (count) {
                search.append(type, `${key}.${op}.${count}`)
            }
        }
    })

    ////////////////////////////////////////
    // get single values
    const params = ["killtime_min", "killtime_max"]
    params.forEach(param => {
        const value = from_data[param]
        if (value !== undefined) {
            search.append(param, value)
        }
    })


    return search.toString()
}


/* Generate the new url from the form data.*/
function build_new_url(data) {

    let url = new URL(window.location)
    url.pathname = `/comp_ranking/${data.boss_name_slug}`
    url.search = build_search_string(data)
    return url
}


export default function CompSearch() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const form_methods = useForm();
    const history = useHistory();

    ////////////////////////////////////////////////////////////////////////////
    // Hooks Part2
    //
    React.useEffect(() => {
        document.title = "Lorrgs: Comp Search"
    }, [])


    ////////////////////////////////////////////////////////////////////////////
    // Callbacks
    //
    function onSubmit(data) {

        // build the new url
        const new_url = build_new_url(data)
        const rel_url = `${new_url.pathname}${new_url.search}` // exclude the hostname

        // redirect to the new url
        console.log("new_url", new_url)
        history.push(rel_url);
    }


    ////////////////////////////////////////////////////////////////////////////
    // Render
    //
    return (

        <FormProvider {...form_methods}>

            <form onSubmit={form_methods.handleSubmit(onSubmit)}>

            <div className="mt-5 d-flex flex-column justify-content-center">
                <div className="comp-search-container">

                    {/* row 1: Header */}
                    <div className="m-0 ml-auto d-flex align-items-center">
                        <BossSelection />
                    </div>
                    <h1 className="my-0 mx-3">vs.</h1>
                    <div className="m-0 mr-auto d-flex align-items-center">
                        <PlayerSelection />
                    </div>

                    {/* row 2: spacer */}
                    <hr className="full_row my-2" />

                    {/* row 3 left: boss/fight fields */}
                    <div className="ml-auto">
                        <BossSelect />
                        <div className="d-flex">
                            <div className="ml-auto"></div>
                            <KilltimeGroup />
                        </div>
                    </div>

                    {/* row 3 middle */}
                    <div></div>

                    {/* row 3 right: player filters */}
                    <div className="mr-auto">
                        <div className="d-flex">
                            <PlayerRoleSearch />
                            <PlayerSpecSearch className="ml-3"/>
                        </div>

                        {/* needs to be inside here, to align with the right border */}
                        <div className="d-flex mt-3">
                            <SearchSubmitButton />
                        </div>
                    </div>


                </div>
            </div>

            </form>
        </FormProvider>
    )
}
