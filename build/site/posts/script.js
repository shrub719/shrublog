function rgbToHex(rgb) {
  return "#" + (1 << 24 | rgb[0] << 16 | rgb[1] << 8 | rgb[2]).toString(16).slice(1);
}

function randomColour() {
    const colour = [60, 179, 113];
    const range = 50;
    
    for (let i = 0; i < 3; i++) {
        colour[i] = colour[i] + Math.floor(Math.random() * range * 2 - range);
    }

    return rgbToHex(colour);
}


const manifest = INSERT_MANIFEST_HERE;
manifest.sort((a, b) => (
    b.date.localeCompare(a.date)
));

const postList = document.getElementById("post-list");

console.log(manifest);
manifest.forEach((post) => {
    const element = document.createElement("div");
    element.classList.add("post-item");
    if (post.private) element.classList.add("private-post");
    if (post.hidden) element.classList.add("hidden-post");

    const title = document.createElement("h2");
    const link = document.createElement("a");
    link.textContent = post.title;
    link.href = "./" + post.id;
    if (!post.private && !post.hidden) link.style.color = randomColour();
    title.appendChild(link);

    const subtitle = document.createElement("p");
    const escapedSubtitle = post.subtitle
        .replace(/&quot;/g, "\"")
        .replace(/&#92;/g, "\\");
    subtitle.textContent = escapedSubtitle;
    console.log(escapedSubtitle);

    const date = document.createElement("p");
    date.classList.add("date");
    date.textContent = post.date;

    element.appendChild(title);
    element.appendChild(subtitle);
    element.appendChild(date);

    postList.appendChild(element);
});

