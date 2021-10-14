

interface Class {
    id: number
    name: string
    name_slug: string
}


export default interface Spec {

    class: Class
    role: string

    /** Just the Name of the Spec itself. eg: "Holy" */
    name: string

    /** Complete Name including the Class: eg.: "Holy Paladin" */
    full_name: string

    /** Complete name slugified. eg: "holy-paladin" */
    full_name_slug: string

    /** URL to the icon */
    icon_path: string

    spells_by_type: { [key: string]: number[] }

    loaded: boolean

}
