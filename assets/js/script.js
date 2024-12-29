function getGiscusTheme() {
    // 假设localStorage中存储的是用户的偏好主题
    const preferredTheme = localStorage.getItem("pref-theme");
    // 当偏好主题为light时，返回no_border_light；当偏好主题为dark时，返回noborder_gray
    let giscusTheme;
    switch (preferredTheme) {
        case "light":
            giscusTheme = "no_border_light";
            break;
        case "dark":
            giscusTheme = "noborder_gray";
            break;
        default:
            giscusTheme = "noborder_gray"; // 默认为dark，可根据需要调整
    }
    return giscusTheme;
}

function setGiscusTheme() {
    function sendMessage(message) {
        const iframe = document.querySelector('iframe.giscus-frame');
        if (!iframe) return;
        iframe.contentWindow.postMessage({ giscus: message }, 'https://giscus.app');
    }
    // 更新sendMessage调用，以确保应用正确的主题
    sendMessage({
        setConfig: {
            theme: getGiscusTheme(),
        },
    });
}

const attrs = {
    "src": "https://giscus.app/client.js",
    "data-repo": "JingyiWu-codespace/blog_comments",
    "data-repo-id": "R_kgDOLPpadg",
    "data-category": "Announcements",
    "data-category-id": "DIC_kwDOLPpads4CdEvR",
    "data-mapping": "pathname",
    "data-strict": "0",
    "data-reactions-enabled": "1",
    "data-emit-metadata": "0",
    "data-input-position": "bottom",
    "data-theme": getGiscusTheme(), // 这里调用getGiscusTheme以设置正确的主题
    "data-lang": "en",
    "crossorigin": "anonymous",
    "async": ""
};

const giscusScript = document.createElement("script");
Object.entries(attrs).forEach(([key, value]) => giscusScript.setAttribute(key, value));
document.body.appendChild(giscusScript);

// 监听主题切换按钮（如果存在），以允许用户手动更改主题
const toggle = document.querySelector('#theme-toggle');
if (toggle) {
    toggle.addEventListener('click', setGiscusTheme);
}
