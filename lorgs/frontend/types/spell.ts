

type Spell = {

    spell_id: number

    spell_type: string

    name: string

    color: string

    cooldown: number

    duration: number

    /** name of just the icon filename */
    icon: string

    show: boolean

    tooltip_info?: string

    tags?: string[]
}

export default Spell
