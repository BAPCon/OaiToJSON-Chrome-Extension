// ...
// to-do

async function parseExternalContent(content) {
    try {
        const response = await fetch("https://s4c9vq66eh.execute-api.us-east-2.amazonaws.com/dev/process_open_ai", {
            method: "POST",
            body: JSON.stringify({ content })
        });
        return await response.json();
    } catch (error) {
        console.error("Error parsing external content:", error);
    }
}

async function getMessageElements() {
    const messageElements = getClassElements("thread-item");
    const messages = [];

    messageElements.forEach(messageElement => {
        let role = "system";
        let content = "";
        
        if (messageElement.children[0].className === "run-instructions") {
            content = messageElement.querySelector(".instruction-content").textContent;
        } else {
            role = messageElement.querySelector(".thread-item-header").textContent === "User" ? "User" : "Assistant";
            content = messageElement.querySelector(".markdown-content").innerHTML;
        }
        
        messages.push({ role, content });
    });

    try {
        const response = await fetch("https://s4c9vq66eh.execute-api.us-east-2.amazonaws.com/dev/process_open_ai", {
            method: "POST",
            body: JSON.stringify({ content: messages })
        });
        const jsonResponse = await response.json();
        const processedContent = JSON.parse(jsonResponse).content;
        const urlParams = new URLSearchParams(window.location.search);
        const threadParam = urlParams.get('thread');
        
        downloadToFile(JSON.stringify(processedContent), `${threadParam}.json`, 'application/json');
    } catch (error) {
        console.error("Error sending messages to server:", error);
    }
}

function downloadToFile(content, fileName, contentType) {
    const a = document.createElement("a");
    const file = new Blob([content], { type: contentType });
    
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

function getClassElements(className) {
    return Array.from(document.getElementsByClassName(className));
}

// Initiate process
getMessageElements();