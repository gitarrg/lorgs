
import React from 'react'
import { useWatch } from "react-hook-form";


export default function SearchSubmitButton() {

    // state to enable/disable the button
    const boss_name_slug = useWatch({name: "boss_name_slug"})

    return (
        <button
            type="submit"
            disabled={boss_name_slug === undefined}
            className="search_submit_button btn btn-lg btn-primary shadow mt-3 ml-auto p-2"
        >
            Search
        </button>
    )
}
