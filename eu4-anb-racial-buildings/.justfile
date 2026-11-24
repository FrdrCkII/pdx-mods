target := "/home/main/.local/share/Paradox Interactive/Europa Universalis IV/mod/anbARB"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ target }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"

