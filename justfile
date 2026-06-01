src := "https://github.com/shrub719/sb-src"

clean:
    -rm -r shrublog

get-posts:
    if [ ! -d "src" ]; then \
      git clone {{src}} src; \
    fi
    cd src && git pull

setup: clean
    mkdir -p shrublog/posts/assets
    cp -r build/site/** shrublog/
    cp -r src/assets/** shrublog/posts/assets/

build: setup get-posts
    python3 build/main.py src shrublog

serve:
    python3 -m http.server

[default]
dev: setup
    python3 build/main.py src shrublog dev

alias upd := get-posts

