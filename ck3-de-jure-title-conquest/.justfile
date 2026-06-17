target := "$HOME/.local/share/Paradox Interactive/Crusader Kings III/mod/deJureTitleConquest"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ target }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"

