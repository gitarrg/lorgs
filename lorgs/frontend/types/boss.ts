
import type Spec from "./spec"

/**
 * Type for a Boss in the Game.
 *
 * There can only be one of each type. eg.: there is only one "Painsmith Raznal"
 */
export default interface Boss extends Spec {

    class: {
        name: "boss"
        name_slug: "boss"
    }

    // role: string

    /** encounter ID */
    id: number

    /** Nice short Name */
    // name: string

    /** Complete Name */
    // full_name: string

    // name_slug: "painsmith" NOT USED

    /** Complete name slugified. Primary identifier */
    // full_name_slug: string

    /** URL to the icon */
    // icon_path: string

    // loaded: boolean

    // spells_by_type: {[key: string]: number[] } // todo: spell type
}

