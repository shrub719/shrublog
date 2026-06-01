clean:
    -rm -r shrublog

setup: clean
    mkdir -p shrublog/posts/assets
    cp -r build/site/** shrublog/
    cp -r src/assets/** shrublog/posts/assets/

build: setup
    python3 build/main.py src/ shrublog/

serve:
    python3 -m http.server

[default]
dev: setup
    python3 build/main.py src/ shrublog/ dev
