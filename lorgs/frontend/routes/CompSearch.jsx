/* Page/Form to search for specific Comps*/

import React from 'react'
import { useHistory } from 'react-router-dom';
import { useForm, FormProvider } from "react-hook-form";

import BossSelect from './CompSearch/BossSelect.jsx'
import BossSelection from './CompSearch/BossSelection.jsx'
import PlayerRoleSearch from './CompSearch/PlayerRoleSearch.jsx'
import PlayerSelection from './CompSearch/PlayerSelection.jsx'
import PlayerSpecSearch from './CompSearch/PlayerSpecSearch.jsx'
import SearchSubmitButton from './CompSearch/SearchSubmitButton.jsx'


/* Takes the form data dict and generates the search string.*/
function build_search_string(from_data) {

    let search = new URLSearchParams()

    const types = ["role", "spec"]
    types.forEach(type => {

        const items = from_data[type]
        for (const [key, {count, op}] of Object.entries(items)) {
            if (count) {
                search.append(type, `${key}.${op}.${count}`)
            }
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

    const form_methods = useForm();
    const history = useHistory();

    function onSubmit(data) {

        // build the new url
        const new_url = build_new_url(data)
        const rel_url = `${new_url.pathname}${new_url.search}` // exclude the hostname

        // redirect to the new url
        console.log("new_url", new_url)
        history.push(rel_url);
    }

    // Render
    return (

        <FormProvider {...form_methods}>

            <form onSubmit={form_methods.handleSubmit(onSubmit)}>

            <div className="mt-5 d-flex flex-column justify-content-center">
                <div className="comp-search-container">

                    <BossSelection />
                    <h1 className="my-0 mx-3">vs.</h1>
                    <PlayerSelection />

                    <hr className="my-2" />

                    <BossSelect />
                    <div></div>
                    <div className="mr-auto">
                        <div className="d-flex">
                            <PlayerRoleSearch />
                            <PlayerSpecSearch />
                        </div>

                        <div className="d-flex">
                            <div className="ml-auto mt-5">
                                <SearchSubmitButton />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            </form>
        </FormProvider>
    )
}
