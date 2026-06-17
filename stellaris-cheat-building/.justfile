target := "$HOME/.local/share/Paradox Interactive/Stellaris/mod/cheatBuilding"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ target }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"
    
