target := "$HOME/.local/share/Steam/steamapps/compatdata/236850/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Europa Universalis IV/mod/anbARB"
proton := "C:/users/steamuser/Documents/Paradox Interactive/Europa Universalis IV/mod/anbARB"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ proton }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"

