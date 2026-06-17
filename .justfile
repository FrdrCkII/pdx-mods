alias ia := install-all

install-all:
    cd stellaris-auto-build-starbase && just install
    cd hoi4-use-overlord-color && just install

