import EventLine from "./EventLine"


export default class Resurrection extends EventLine {

    get color() {
        return "#8cff2e"
    }

    _get_text_label() {
        return "🠝 " + super._get_text_label()
    }

    _get_text_tooltip() {
        const t = this._get_tooltip_elements()
        return `${t.icon} ${t.time} ${t.source} resurrects ${t.player} with ${t.spell}`
    }
}
