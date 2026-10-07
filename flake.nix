{
  # «¡Trivia!» (plans/19-repo-layout.md, D-18, D-35).
  #
  #   nix build .#app              the game as it ships: built client + Python server, run with `trivia`
  #   nix run .#qgen -- batch      the LLM question batch (authoring/RUNBOOK.md, D-36)
  #   nix develop / direnv allow   everything for development, incl. `trivia`, `trivia-authoring`,
  #                                `qgen` and `trivia-media` running from this checkout
  #
  # The authoring tools edit files in the checkout (authoring/data, app/data/pool.json, work/), so
  # they are wrappers that run the checkout's scripts with pinned Python, ImageMagick and Claude Code.
  description = "Family trivia party game";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f (import nixpkgs {
        inherit system;
        # Claude Code is the one unfree package the pipeline needs (D-35).
        config.allowUnfreePredicate = pkg: nixpkgs.lib.getName pkg == "claude-code";
      }));

      # A command that runs a script from the repo checkout it is called in.
      fromCheckout = pkgs: name: script: runtimeInputs: pkgs.writeShellApplication {
        inherit name;
        runtimeInputs = [ pkgs.git pkgs.python3 ] ++ runtimeInputs;
        text = ''
          root=$(git rev-parse --show-toplevel 2>/dev/null) || {
            echo "${name}: run this inside the trivia repository" >&2; exit 2; }
          if [ ! -f "$root/${script}" ]; then
            echo "${name}: $root is not the trivia repository (no ${script})" >&2; exit 2
          fi
          exec python3 "$root/${script}" "$@"
        '';
      };

      authoringTools = pkgs: {
        qgen = fromCheckout pkgs "qgen" "authoring/tools/qgen.py" [ pkgs.claude-code pkgs.imagemagick ];
        trivia-media = fromCheckout pkgs "trivia-media" "authoring/tools/media.py" [ pkgs.imagemagick ];
        trivia-authoring = fromCheckout pkgs "trivia-authoring" "authoring/server/main.py" [ ];
        trivia-dev = fromCheckout pkgs "trivia" "app/server/main.py" [ ];
      };
    in {
      packages = forAll (pkgs:
        let tools = authoringTools pkgs; in {
          # What ships (D-35): app/ only. Game state and the media cache go to
          # $XDG_DATA_HOME/trivia/ unless TRIVIA_STATE / TRIVIA_MEDIA say otherwise.
          app = pkgs.buildNpmPackage {
            pname = "trivia";
            version = "0.1.0";
            src = pkgs.lib.fileset.toSource {
              root = ./.;
              fileset = pkgs.lib.fileset.unions [ ./package.json ./package-lock.json ./app ./authoring/ui/package.json ];
            };
            npmDepsHash = "sha256-njHPPjPRJW/Qe+INDPjHGxg1haZ7ZYrLBJAsfgYAin4=";
            npmWorkspace = "app/client";
            env.VITE_AUTHORING_URL = "";  # no authoring server in a packaged game: hide its links
            nativeBuildInputs = [ pkgs.makeWrapper ];
            installPhase = ''
              runHook preInstall
              share=$out/share/trivia/app
              mkdir -p $share/client $out/bin
              cp -r app/server app/data $share/
              cp -r app/client/dist $share/client/dist
              makeWrapper ${pkgs.python3}/bin/python3 $out/bin/trivia \
                --add-flags $share/server/main.py \
                --run 'data=''${XDG_DATA_HOME:-$HOME/.local/share}/trivia' \
                --run 'export TRIVIA_STATE=''${TRIVIA_STATE:-$data/state}' \
                --run 'export TRIVIA_MEDIA=''${TRIVIA_MEDIA:-$data/media}'
              runHook postInstall
            '';
            meta.mainProgram = "trivia";
          };
          default = self.packages.${pkgs.system}.app;
          # The authoring commands, for `nix run .#qgen` etc. They never ship.
          authoring = pkgs.symlinkJoin {
            name = "trivia-authoring";
            paths = with tools; [ qgen trivia-media trivia-authoring ];
          };
        } // { inherit (tools) qgen trivia-media trivia-authoring; });

      devShells = forAll (pkgs:
        let tools = authoringTools pkgs; in {
          default = pkgs.mkShell {
            packages = [
              pkgs.nodejs_22 pkgs.python3 pkgs.imagemagick pkgs.claude-code
              tools.qgen tools.trivia-media tools.trivia-authoring tools.trivia-dev
            ];
          };
        });
    };
}
