

interface Class {
    id: number
    name: string
    name_slug: string
}


type Spec = {

    class: Class
    role: string

    /** Just the Name of the Spec itself. eg: "Holy" */
    name: string

    /** Complete Name including the Class: eg.: "Holy Paladin" */
    full_name: string

    /** Complete name slugified. eg: "holy-paladin" */
    full_name_slug: string

    /** URL to the icon */
    icon_path?: string
}

export default Spec
