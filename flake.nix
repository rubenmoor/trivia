{
  # Dev environment (D-18): Node 22 for the Svelte client, Python 3 for the server and tools.
  # `nix develop`, or `direnv allow` once (.envrc). Game night only needs Python and client/dist/.
  description = "Family trivia party game";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [ pkgs.nodejs_22 pkgs.python3 ];
        };
      });
    };
}
