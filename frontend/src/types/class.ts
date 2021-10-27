

/** A Class in the game. eg.: Druid, Shaman, Warrior */
export default interface Class {

    id: number
    name: string

    /** full_name_slug for each spec */
    specs: string[]
}
