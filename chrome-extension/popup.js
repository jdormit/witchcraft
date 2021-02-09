
// some declarations just to make linters stop complaining
/**
 * @class chrome
 * @property extension.getBackgroundPage
 * @property chrome.extension.getURL
 * @property tabs.onActivated
 * @property tabs.sendMessage
 * @property browserAction.setBadgeText
 * @property chrome.browserAction.setIcon
 * @property chrome.browserAction.setTitle
 */

class Popup {

    constructor () {
        const background = chrome.extension.getBackgroundPage();

        this.fullUrlRegex = /^https?:\/\//;

        /** @type {Witchcraft} */
        this.witchcraft = background.window.witchcraft;

        this.makeButtonFromAnchor("docs");
        this.makeButtonFromAnchor("report-issue");
        this.showVersion();
        this.showServerStatus();
        this.renderScriptsTable();
        this.makeAdvancedPanel();
    }

    showVersion() {
        document.getElementById("version").innerText = chrome.runtime.getManifest().version;
    }

    makeButtonFromAnchor(id, pageName = id) {
        const anchor = typeof id === "string" ? document.getElementById(id) : id;
        anchor.addEventListener("click", () => {
            this.witchcraft.openFileNative(anchor.getAttribute("data-filename"));
            return false;
        });
    }

    showServerStatus() {
        document.getElementById("server-status")
            .classList.toggle("offline", !this.witchcraft.isServerReachable);
    }

    /** @return {void} */
    async renderScriptsTable() {
        const scriptsTable = document.getElementById("scripts-table");
        const noScriptsElement = document.getElementById("no-scripts");

        const currentTabId = await this.getCurrentTabId();
        const scriptNames = this.witchcraft.getScriptNamesForTab(currentTabId);

        const hasScripts = scriptNames && scriptNames.size > 0;
        noScriptsElement.classList.toggle("hidden", hasScripts);
        scriptsTable.classList.toggle("hidden", !hasScripts);

        if (hasScripts) {
            for (const scriptName of scriptNames) {
                const fileName = scriptName.substr(scriptName.lastIndexOf("/") + 1);

                const tdName = document.createElement("td");
                tdName.classList.add("script-name");
                const aName = document.createElement("div");
                aName.classList.add("script-button");
                tdName.appendChild(aName);
                aName.innerText = fileName;
                aName.setAttribute("data-filename", fileName)
                this.makeButtonFromAnchor(aName, "script");

                const tdType = document.createElement("td");
                const extensionMatch = scriptName.match(/\.([^.]+)$/);
                if (extensionMatch) {
                    const extension = extensionMatch[1];
                    tdType.classList.add(extension.toLowerCase());
                    tdType.innerText = extension.toUpperCase();
                } else {
                    tdType.innerText = "?";
                }

                const tr = document.createElement("tr");
                tr.appendChild(tdName);
                tr.appendChild(tdType);
                scriptsTable.appendChild(tr);
            }
        }
    }

    async getCurrentTabId() {
        return new Promise(resolve => {
            chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
                if (Array.isArray(tabs) && tabs.length > 0) {
                    resolve(tabs[0].id);
                } else {
                    resolve(undefined);
                }
            });
        });
    }

    makeAdvancedPanel() {
        const scriptDirInput = document.getElementById("script-directory");
        scriptDirInput.value = this.witchcraft.getScriptDirectory();
        scriptDirInput.addEventListener("input", event => {
            this.witchcraft.setScriptDirectory(event.target.value);
        });

        const resetButton = document.getElementById("script-directory-reset");
        resetButton.addEventListener("click", event => {
            console.info(this.witchcraft.defaultScriptDirectory);
            this.witchcraft.setScriptDirectory(this.witchcraft.defaultScriptDirectory);
            scriptDirInput.value = this.witchcraft.getScriptDirectory();
            event.preventDefault();
            return false;
        });
    }
}

// this script will run every time the popup is shown (i.e., every time the user clicks on the extension icon)
// it reads information from the background window and shows it to the user
window.addEventListener("load", () => new Popup());
