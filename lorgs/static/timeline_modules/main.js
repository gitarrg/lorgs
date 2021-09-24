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

    // check to make sure this only runs once
    if (SETTINGS.done) {return;}
    SETTINGS.done = true;


    // create the scene
    let scene = new Scene(SETTINGS)
    await scene.load()

    if (SETTINGS.loading_spinner) {
        hide(SETTINGS.loading_spinner)
    }

}

window.addEventListener("load", main)

