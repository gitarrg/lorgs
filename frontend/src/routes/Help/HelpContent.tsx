import { DISCORD_LINK } from "../../constants"
import styles from "./Help.scss"


const WARNING = <p className="text-black h3 text-center">(🚧 Work in progress and subject to UI changes. 🚧)</p>

const OVERVIEW = <div>
    <h1 id="overview">Overview:</h1>

    <p>After selecting the spec you want to examine you will see the top ranking logs for the first boss of the current tier.</p>

    <p>Change to whichever boss is the most relevant one for you in the top right panel.<br />
    Then you will notice three main sections:</p>

    <p>The <a href="#timeline"><strong className="wow-mage">encounter timeline</strong></a>,&nbsp;
    <a href="spells_toolbar"><strong className="wow-deathknight">spell selection</strong></a>&nbsp;
    and the <a href="#navigation"><strong className="wow-rogue">navigation bar</strong></a>.
    </p>
    <img className="img-fluid" src="https://cdn.discordapp.com/attachments/886940165338169344/887028864755318874/unknown.png" alt="overview" />
</div>


////////////////////////////////////////////////////////////////////////////////


const TIMELINE_INTRO = <div>
    <h1 id="timeline">Timeline</h1>
    <div className="row mb-3">
        <div className="col">
            <p>
                On the timeline you will see the top logs for your chosen encounter and their casting patterns in a directly comparable fashion.<br />
                One log for every line.
            </p>
        </div>
    </div>
</div>


const TIMELINE_SPELL = <div className="row mb-3">
    <div className="col">
        <img className="img-fluid" src="https://i.imgur.com/sqREhiR.png" alt="cast element components" />
    </div>

    <div className="col">
        <p>All instances of relevant spell casts are highlighted on the timeline, with up to three elements:</p>

        <strong><i className="fas fa-clock" /> Cast Time</strong>
        <p>How far into the encounter this spell was cast.</p>

        <strong><i className="fas fa-stream" /> Duration</strong>
        <p>How long the spell is active for <em className="text-muted">(when applicable)</em>.</p>

        <strong><i className="fas fa-hourglass" /> Cooldown</strong>
        <p>How long the spell has been on cooldown.<br />
            <small className="text-muted">In some cases (for spells that have their cooldowns reduced by talents, legendaries or other effects) the value here is an estimate.</small>
        </p>
    </div>
</div>


const TIMELINE_FOCUS = <div className="row mb-3">
    <div className="col">
        <h3 id="timeline_focus">Spell selection</h3>
        <p><strong className="wow-rogue">Click</strong> on any ability on the timeline <strong className="wow-rogue">to focus</strong> it and all instances of the same spell.</p>
        <p><strong className="wow-mage">Ctrl+Click</strong> to <strong className="wow-mage">focus multiple spells</strong> at once.</p>
    </div>

    <div className="col">
        <img className="img-fluid" src="https://i.imgur.com/oYVTTCQ.gif" alt="focus spell gif" />
    </div>
</div>


const TIMELINE_NAV_DRAG = <div className="row mb-3">
    <div className="col">
        <h3 id="timeline_nav">Timeline navigation</h3>
        <strong className="wow-legendary">Click and Drag</strong> on the timeline-ticks or anywhere on the background <strong className="wow-legendary">to move</strong>.
    </div>
    <div className="col">
        <img className="img-fluid" src="https://i.imgur.com/Kxbr3bv.gif" />
    </div>
</div>

const TIMELINE_NAV_ZOOM = <div className="row mb-3">
    <div className="col">
        <p>Hold <strong className="wow-paladin">Ctrl or Shift and Scroll</strong> your Mousewheel <strong className="wow-paladin">to zoom</strong> in and out.</p>
    </div>
    <div className="col">
        <img className="img-fluid" src="https://i.imgur.com/w9bJclN.gif" />
    </div>
</div>


const TIMELINE_PLAYER_NAMES = <div>
    <h3 id="timeline_boss">Boss Lane</h3>
    <div className="row mb-3">
        <div className="col-7">
            <img className="img-fluid" src="https://i.imgur.com/2jklPmA.png" />
        </div>

        <div className="col-5">
            <div className="card text-dark bg-info">
                <div className="card-body">
                    <h5 className="card-text"><strong><i className="fas fa-info-circle"></i> The Boss's Casts are taken from the first lane on the timeline!</strong></h5>
                </div>
            </div>

            <p>
                Some encounters change based on push timings, or specific strat executations.<br />
                In these instances the exact boss lane timings might be inaccurate from log to log.
            </p>

            <p>
                Keep that in mind when you ask yourself why some players use their CD's a few seconds before or after an important ability.
                This can most likely be due to that guild getting said boss ability a few seconds off from what that particular fight shown in the boss lane.
            </p>
        </div>

    </div>

    <h3 id="timeline_players">Player Names</h3>
    <div className="row mb-3">
        <div className="col">
            <p>Hover over the log lane number on the left to reveal the player’s name.<br />
            From there you can click on their name to open the corresponding log on warcraftlogs.</p>
            <img src="https://i.imgur.com/RPZhdDx.gif" width="500px" />
        </div>
    </div>

</div>


const TIMELIME_RULER = <div className="row mb-3">
    <div className="col">
        <h3 id="timeline_ruler">Timeline Markers</h3>
        <p>To help you check through timings across many parses, not just the first few, you can add markers that will highlight the exact time slice you are looking at across all logs.</p>
        <p>
            <strong className="wow-monk">Double click to add</strong> markers.<br />
            <strong className="wow-deathknight">Right click</strong> on a marker <strong className="wow-deathknight">to remove</strong> it.<br />
                Left click and <strong className="wow-druid">drag to move</strong> it around.
        </p>
    </div>

    <div className="col">
        <img src="https://i.imgur.com/kVQj74B.gif" width="300px" />
    </div>
</div>

////////////////////////////////////////////////////////////////////////////////

const SPELLS_TOOLBAR_OVERVIEW = <div>
    <h1 id="spells_toolbar">Spells Toolbar</h1>
    <img className="img-fluid" src="https://cdn.discordapp.com/attachments/886940165338169344/887124365978775612/unknown.png" />
</div>


const SPELLS_TOOLBAR_DISPLAY = <div>
    <h3 id="spells_toolbar_display">Display-Group</h3>
    <div className="row mb-3">
        <div className="col">
            <p>the Display Group offers you three buttons to customize the overall view:</p>

            <strong><i className="fas fa-clock"></i> Cast Time</strong>
            <p>Show/Hide the time stamp for each cast</p>

            <strong><i className="fas fa-stream"></i> Duration</strong>
            <p>Show/Hide for how long each cast was active.<br />
                <small className="text-muted">eg.: Healing Tide Totem is active for 10sec.</small>
            </p>

            <strong><i className="fas fa-hourglass"></i> Cooldown</strong>
            <p>Show/Hide spell cooldowns.<br />
            Toggle the display for the cooldown-bars, that indicate for how long the spell was on cooldown.
            This can be useful to see if players decided to hold a spell, or used it right as it came of cooldown.
            </p>
        </div>

        <div className="col">
            <img className="img-fluid" src="https://i.imgur.com/8fn8mIv.gif" />
        </div>
    </div>
</div>


const SPELLS_TOOLBAR_SPELLS = <div>
    <h3 id="spells_toolbar_spells">Spells/Consumables/Items</h3>

    <div className="row mb-3">
        <p>The next icon you will see is one for each spell/consumable/trinket that has been found in the top 50 logs.</p>
        <div className="col">
            <p>Click on any spell to show/hide it.<br />
            Click on a Group-Name to toggle all spells in that group.</p>
            <img className="img-fluid" src="https://i.imgur.com/KryE3Dr.gif" />
        </div>

        <div className="col">
            <p>These are most often split into 4 categories:</p>
            <strong>Boss:</strong>
            <p>Abilities used by the encounter</p>
            <strong>Spec:</strong>
            <p>Spells cast by the player(s)</p>
            <strong>Potions:</strong>
            <p>Pots and consumables</p>
            <strong>Trinkets:</strong>
            <p>On-use trinkets and similar items</p>
            <p></p>

            <div className="card text-dark bg-warning rounded p-2" style={{maxWidth: "22rem"}}>
                <h5 className="h4"><strong>⚠️ Not every ability is listed ⚠️</strong></h5>
                <p className="card-text">
                    All of tracked abilities are manual added to a whitelist.<br />
                    If there are any missing spells you would like to see added, please feel free to reach out on
                    <a href={DISCORD_LINK}><strong className="text-black"> 👉 discord</strong></a>.
                </p>
            </div>
        </div>
    </div>
</div>

const NAVIGATION = <div>
    <h1 id="navigation">Navigation</h1>

    <div className="row mb-3">
        <div className="col-4">
            <strong>A: Specs</strong>
            <p>Choose a different spec</p>
        </div>

        <div className="col-4">
            <strong>B: Bosses</strong>
            <p>Swap between different bosses of the current raid tier</p>
        </div>
        <div className="col-4">
            <strong><i className="fas fa-home"></i> C: Home</strong>
            <p>Go back to the start page</p>
        </div>
    </div>
    <img className="img-fluid" src="https://cdn.discordapp.com/attachments/886940165338169344/887143350128492574/unknown.png" />
</div>


////////////////////////////////////////////////////////////////////////////////


function Block({class_names="", children}) {
    return (
        <div className={class_names}>
            {children}
        </div>
    )
}


////////////////////////////////////////////////////////////////////////////////

export default function HelpContent() {
    return (
        <div className={styles.content}>

            <Block class_names="border rounded bg-warning">{WARNING}</Block>

            <Block>{OVERVIEW}</Block>

            <hr />

            <Block>
                {TIMELINE_INTRO}
                {TIMELINE_SPELL}
                {TIMELINE_FOCUS}
                {TIMELINE_NAV_DRAG}
                {TIMELINE_NAV_ZOOM}
                {TIMELINE_PLAYER_NAMES}
                {TIMELIME_RULER}
            </Block>

            <hr />

            <Block>
                {SPELLS_TOOLBAR_OVERVIEW}
                {SPELLS_TOOLBAR_DISPLAY}
                {SPELLS_TOOLBAR_SPELLS}
            </Block>

            <hr />

            <Block>
                {NAVIGATION}
            </Block>
        </div>
    )
}
