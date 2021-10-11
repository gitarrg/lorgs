/* Constants used only inside the Timeline Module */


export const LINE_HEIGHT = 28

export const DEFAULT_ZOOM = 4

// Events
export const EVENT_ZOOM_CHANGE = "zoom_change"
export const EVENT_SPELL_DISPLAY = "spell_display"
export const EVENT_DISPLAY_SETTINGS = "display_settings"

export const EVENT_CHECK_IMAGES_LOADED = "check_images_loaded"
export const EVENT_IMAGES_LOADED = "images_loaded"

// This event is also used inside the spells-reducer and must therefore match the name there!
export const EVENT_SPELL_SELECTED = "spells/spell_selected"

// triggered when fight/player filters have changed
export const EVENT_APPLY_FILTERS = "apply_filters"
