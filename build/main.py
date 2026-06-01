import sys, markdown
from pathlib import Path

POST_TEMPLATE_PATH  = Path("./build/post_template.html")
HEAD_PATH = Path("./build/head.html")

MD_EXT = [
    "extra"
]
MD_CONFIG = {
    "extra": {
        "footnotes": {
            "BACKLINK_TEXT": "<"
        }
    }
}


def convert_post(file, posts_dir, post_template, head, private=False, hidden=False):
    lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
    
    id = file.stem
    if private or hidden: id = id + ".wip"
        
    title = lines[0].rstrip("\n").lstrip("#").strip()
    pre = "[private] " if private else "[hidden] " if hidden else ""
    title = pre + title

    subtitle = lines[1].rstrip("\n")
    date = lines[2].rstrip("\n")

    body_md = "".join(lines[3:])
    
    body_html = markdown.markdown(
        body_md,
        extensions=MD_EXT,
        extension_configs=MD_CONFIG
    )

    html = post_template.format(
        head=head,
        title=title, 
        subtitle=subtitle, 
        date=date,
        body=body_html
    )

    post_dir = posts_dir / id
    post_dir.mkdir(parents=True, exist_ok=True)

    (post_dir / "index.html").write_text(html, encoding="utf-8")
    
    print("    " + pre + id)

    return id, title, subtitle, date, private, hidden


def clean_string(s):
    return s.replace("\"", "&quot;").replace("\\", "&#92;")


def patch_script(manifest, posts_dir):
    script_path = (posts_dir / "script.js")
    script = script_path.read_text(encoding="utf-8")

    patched_script = script.replace("INSERT_MANIFEST_HERE", manifest)
    script_path.write_text(patched_script, encoding="utf-8")


def create_manifest(posts, output_dir, posts_dir):
    manifest_item = """  {{
    "id": "{id}",
    "title": "{title}",
    "subtitle": "{subtitle}",
    "date": "{date}",
    "private": {private},
    "hidden": {hidden}
  }},\n"""

    manifest = "[\n"

    for post in posts:
        manifest = manifest + manifest_item.format(
            id = post[0],
            title=clean_string(post[1]),
            subtitle=clean_string(post[2]),
            date=post[3],
            private="true" if post[4] else "false",
            hidden="true" if post[5] else "false"
        )

    manifest = manifest[:-2] + "\n]"

    (output_dir / "manifest.json").write_text(manifest, encoding="utf-8")

    print("created manifest")

    patch_script(manifest, posts_dir)
    
    print("patched script")


def build(source_dir, output_dir, is_dev):
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    posts_dir = output_dir / "posts"

    # complete/published posts
    source_posts = source_dir / "posts"

    # almost complete posts, sent out for testing
    source_hidden = source_dir / "hidden"

    # incomplete posts, only viewable locally
    source_private = source_dir / "private"

    post_template = POST_TEMPLATE_PATH.read_text(encoding="utf-8")
    head = HEAD_PATH.read_text(encoding="utf-8")
    
    posts = []
    print("converting posts:")

    for file in source_posts.iterdir():
        if file.suffix != ".md" or not file.is_file():
            continue

        posts.append(convert_post(file, posts_dir, post_template, head))

    for file in source_hidden.iterdir():
        if file.suffix != ".md" or not file.is_file():
            continue

        post = convert_post(file, posts_dir, post_template, head, hidden=True)
        if is_dev: posts.append(post)

    if is_dev:
        for file in source_private.iterdir():
            if file.suffix != ".md" or not file.is_file():
                continue

            posts.append(convert_post(file, posts_dir, post_template, head, private=True))

    create_manifest(posts, output_dir, posts_dir)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[-1]=="dev")

