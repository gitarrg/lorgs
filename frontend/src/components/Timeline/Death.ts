import EventLine from "./EventLine"


export default class Death extends EventLine {

    get color() {
        return "#ff4d4d"
    }

    _get_text_label() {
        return "💀 " + super._get_text_label()
    }

    _get_text_tooltip() {
        const t = this._get_tooltip_elements()

        // additonal logic in case no spell info is given
        const s = t.spell ? ` from ${t.spell}` : ""
        return `${t.icon} ${t.time} ${t.player} dies${s}.`
    }
}
