

import React from 'react'
import { LOGO_URL } from '../constants'



export default function HeaderLogo({wow_class = "wow-priest"}) {



    return (
        <div className={`${wow_class} header-logo-container rounded wow-border`}>
            <a href="/" data-tip="back to start page">
                <img className="header-logo icon-l " src={LOGO_URL}/>
            </a>
        </div>
    )
}
