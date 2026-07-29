alias ia := install-all
alias io := install-old
    
install-all:
    cd ck3-de-jure-title-conquest && just install
    cd ck3-text-tool && just install
    cd eu4-text-tool && just install
    cd eu5-text-tool && just install
    cd hoi4-use-overlord-color && just install
    cd stellaris-auto-build-starbase && just install
    cd stellaris-cheat-building && just install

install-old:
    cd stellaris-auto-build-starbase-old && just install

