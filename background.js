const playground_url = 'openai.com/playground?assistant';

chrome.runtime.onInstalled.addListener(() => {
    chrome.action.setBadgeText({
      text: 'OFF'
    });
  });
  
// When the user clicks on the extension action
chrome.action.onClicked.addListener(async (tab) => {
  if (tab.url.indexOf(playground_url) != -1) {
  await chrome.scripting.executeScript({
      files: ['content.js'],
      target: { tabId: tab.id }
  });
  }
});