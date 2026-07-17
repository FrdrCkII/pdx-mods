target := "$HOME/.local/share/Steam/steamapps/compatdata/236850/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Europa Universalis IV/mod/textTool"
proton := "C:/users/steamuser/Documents/Paradox Interactive/Europa Universalis IV/mod/textTool"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ proton }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"

