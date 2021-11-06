

/** A Class in the game. eg.: Druid, Shaman, Warrior */
export default interface Class {

    id: number
    name: string
    name_slug?: string

    /** full_name_slug for each spec */
    specs: string[]

    // just to silence some TS errors
    class?: any

}
