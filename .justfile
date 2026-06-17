alias ia := install-all

install-all:
    cd ck3-de-jure-title-conquest && just install
    cd hoi4-use-overlord-color && just install
    cd stellaris-auto-build-starbase && just install
    cd stellaris-cheat-building && just install

