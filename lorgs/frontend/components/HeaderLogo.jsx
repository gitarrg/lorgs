

import React from 'react'
import { LOGO_URL } from '../constants'



export default function HeaderLogo({wow_class = "wow-priest"}) {



    return (
        <div className={`${wow_class} header-logo-container rounded border-mid wow-border`}>
            <a href="/" title="home" data-tip="back to start page">
                <img className="header-logo icon-l " src={LOGO_URL}/>
            </a>
        </div>
    )
}
