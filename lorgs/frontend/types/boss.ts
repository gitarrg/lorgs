

type Boss = {

    class: string // usually "boss"
    role: string

    /** encounter ID */
    // id: number NOT USED

    /** Nice short Name */
    name: string

    /** Complete Name */
    full_name: string

    // name_slug: "painsmith" NOT USED

    /** Complete name slugified. Primary identifier */
    full_name_slug: string

    /** URL to the icon */
    icon_path: string

    loaded: boolean

    spells_by_type: {[key: number]: any} // todo: spell type
}

export default Boss

