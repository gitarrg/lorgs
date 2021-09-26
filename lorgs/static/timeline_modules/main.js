/* */


import Scene from "./scene.js"


////////////////////////////////////////////////////////////////////////////////
// INIT

async function main() {
    console.log("main.js [main]", SETTINGS)

    if (SETTINGS === undefined) {
        console.error("Settings not found")
        return;
    }

    // create the scene
    let scene = new Scene(SETTINGS)
    await scene.load()
}

window.addEventListener("load", main)

