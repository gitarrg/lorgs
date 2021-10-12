import React from 'react'


const LOGO_SVG = (
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 200 200">
    <path d="M41 33l15-19 15 19H61v134h78v-10l20 15-20 15v-10H51V33H41zm30-20h33v116h55v28h-8v-20.031H96V21H71v-8z"
    fillRule="evenodd"/>
</svg>
)


export default function HeaderLogo({wow_class = "wow-boss"}) {

    return (
        <div className="header-logo-container">
            <a href="/">
                <svg className={`header-logo ${wow_class} wow-border icon-l bg-dark rounded`}>
                    {LOGO_SVG}
                </svg>
            </a>
        </div>
    )
}
