const sleep = ms => new Promise(res => setTimeout(res, ms));

function setBlink(content) {
    for (const e of animBlinkElements) {
        e.textContent = content;
    }
}

async function blink() {
    while (true) {
        setBlink("o");
        await sleep(2000 + Math.random() * 2000);
        setBlink("—");
        await sleep(150);
    }
}

const animBlinkElements = document.getElementsByClassName("anim-blink");
blink();

