


const CONFIG_DEV = {
    GOOGLE_ANALYTICS_ID: "dev_mode",

    CDN_TAGS: [
        // React
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.development.js" },
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.development.js" },

        // React Form Hook
        { src: "https://cdn.jsdelivr.net/npm/react-hook-form@7.17.0/dist/index.umd.min.js" },

        // Redux
        { src: "https://cdnjs.cloudflare.com/ajax/libs/redux/4.1.1/redux.js"},
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react-redux/7.2.5/react-redux.js"},

        // Reselect
        { src: "https://cdnjs.cloudflare.com/ajax/libs/reselect/4.0.0/reselect.min.js",   integrity: "sha512-tsMvk3BMjJ0KwWsH8OofK2tR1AJc670PtUcMrjW6hpSHNmWmR5MDOgD5lDPJDCOFonZfbBCMw4e/wy5pAseusg=="},

        // Konva
        { src: "https://cdnjs.cloudflare.com/ajax/libs/konva/8.2.1/konva.min.js",         integrity: "sha512-Kae4IrvcqQ8H13MSTCuxrsUt9pHxzYOyNjTh3QqDtKhYYeLzexguA1aY4+lUAWZnrCRQ6CFx8zHVO8lKLkC/5A=="},
    ],
}


const CONFIG_PROD = {
    GOOGLE_ANALYTICS_ID: "G-Y92VPCY6QW",

    CDN_TAGS: [
        // React
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.production.min.js",         integrity: "sha512-qlzIeUtTg7eBpmEaS12NZgxz52YYZVF5myj89mjJEesBd/oE9UPsYOX2QAXzvOAZYEvQohKdcY8zKE02ifXDmA=="},
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.production.min.js", integrity: "sha512-9jGNr5Piwe8nzLLYTk8QrEMPfjGU0px80GYzKZUxi7lmCfrBjtyCc1V5kkS5vxVwwIB7Qpzc7UxLiQxfAN30dw=="},

        // React Form Hook
        { src: "https://cdn.jsdelivr.net/npm/react-hook-form@7.17.0/dist/index.umd.min.js" },

        // Redux
        { src: "https://cdnjs.cloudflare.com/ajax/libs/redux/4.1.1/redux.min.js",             integrity: "sha512-F21iSaHGX/3NFz5SuwoH6pGhTPxtoJoWWULqQVPQPtLm7nbK5r8vRSSSYy3Aj+H39cVrVm4+3ikGoVD1AjE0sQ=="},
        { src: "https://cdnjs.cloudflare.com/ajax/libs/react-redux/7.2.5/react-redux.min.js", integrity: "sha512-9Opp+Ej8hMqTKKXZlOMMhJqmnmc+xsVNzFPRW5VoEMFYp2r6ooFj58PzFoUZgzutlXpmIvKZP9gQSLqSRSkoww=="},

        // Reselect
        { src: "https://cdnjs.cloudflare.com/ajax/libs/reselect/4.0.0/reselect.min.js",   integrity: "sha512-tsMvk3BMjJ0KwWsH8OofK2tR1AJc670PtUcMrjW6hpSHNmWmR5MDOgD5lDPJDCOFonZfbBCMw4e/wy5pAseusg=="},

        // Konva
        { src: "https://cdnjs.cloudflare.com/ajax/libs/konva/8.2.1/konva.min.js",         integrity: "sha512-Kae4IrvcqQ8H13MSTCuxrsUt9pHxzYOyNjTh3QqDtKhYYeLzexguA1aY4+lUAWZnrCRQ6CFx8zHVO8lKLkC/5A=="},
    ],
}


exports.get_vars = function(mode) {
    if (mode == "production") { return CONFIG_PROD}
    return CONFIG_DEV
}
