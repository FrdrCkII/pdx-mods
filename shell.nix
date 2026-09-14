let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = [
    pkgs.just
    pkgs.rsync
    pkgs.python3
  ];
}
