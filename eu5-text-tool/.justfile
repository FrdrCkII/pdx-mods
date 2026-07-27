target := "/home/main/.local/share/Steam/steamapps/compatdata/3450310/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Europa Universalis V/mod/textTool"

install:
    mkdir --parents "{{ target }}"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"
