target := "$HOME/.local/share/Paradox Interactive/Hearts of Iron IV/mod/useOverlordColor"
game := "$HOME/.local/share/Steam/steamapps/common/Hearts of Iron IV"

install:
    mkdir --parents "{{ target }}"
    cat descriptor.mod | sed "s|@PATH@|{{ target }}|g" > "{{ target }}.mod"
    rsync -av --delete-excluded --exclude={".justfile"} . "{{ target }}"
    
update:
    mkdir --parents ./common
    rsync -av --delete "{{ game }}/common/autonomous_states" ./common
    bash ./update.sh

