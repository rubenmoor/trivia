{
  # «¡Trivia!» (plans/19-repo-layout.md, D-18, D-35).
  #
  #   nix build .#app              the game as it ships: built client + Python server, run with `trivia`
  #   nix run .#qgen -- batch      the LLM question batch (authoring/RUNBOOK.md, D-36)
  #   nix develop / direnv allow   everything for development, incl. `trivia`, `trivia-authoring`,
  #                                `qgen`, `trivia-media`, `trivia-desktop`, `trivia-desktop-build`, `trivia-steam`, `trivia-release-check`, `trivia-report-server` and `trivia-gallery` running from this checkout
  #
  # The authoring tools edit files in the checkout (authoring/data, app/data/pool.json, work/), so
  # they are wrappers that run the checkout's scripts with pinned Python, ImageMagick and Claude Code.
  description = "Family trivia party game";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # `pm`, the project manager CLI, in the dev shell only.
    pm = {
      url = "github:rubenmoor/project-manager";
      inputs.nixpkgs.follows = "nixpkgs";  # one nixpkgs for both
    };
  };

  outputs = { self, nixpkgs, pm }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ];  # nixpkgs 26.11 dropped x86_64-darwin
      forAll = f: nixpkgs.lib.genAttrs systems (system: f (import nixpkgs {
        inherit system;
        # Claude Code for the pipeline (D-35); SteamCMD for Steam uploads (D-93).
        config.allowUnfreePredicate = pkg: builtins.elem (nixpkgs.lib.getName pkg) [ "claude-code" "steamcmd" "steam-unwrapped" ];
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

      # Steamworks SDK 1.62 libs for `trivia-desktop` in dev (plan 85; Valve licence, never shipped).
      # nixpkgs has no package for them; URL and hash as nixpkgs' rimsort. x86_64-linux only.
      steamSdk = pkgs: pkgs.fetchzip {
        url = "https://web.archive.org/web/20250527013243/https://partner.steamgames.com/downloads/steamworks_sdk_162.zip";
        hash = "sha256-yDA92nGj3AKTNI4vnoLaa+7mDqupQv0E4YKRRUWqyZw=";
      };

      authoringTools = pkgs: rec {
        qgen = fromCheckout pkgs "qgen" "authoring/tools/qgen.py" [ pkgs.claude-code pkgs.imagemagick pkgs.nodejs_22 ];
        trivia-media = fromCheckout pkgs "trivia-media" "authoring/tools/media.py" [ pkgs.imagemagick ];
        trivia-authoring = fromCheckout pkgs "trivia-authoring" "authoring/server/main.py" [ pkgs.nodejs_22 ];
        trivia-dev = fromCheckout pkgs "trivia" "app/server/main.py" [ ];
        # The Electron shell from this checkout (plan 54); the npm Electron doesn't run on NixOS.
        trivia-desktop = pkgs.writeShellApplication {
          name = "trivia-desktop";
          runtimeInputs = [ pkgs.git pkgs.electron ];
          text = ''
            root=$(git rev-parse --show-toplevel 2>/dev/null) || {
              echo "trivia-desktop: run this inside the trivia repository" >&2; exit 2; }
            if [ ! -f "$root/app/desktop/main.mjs" ]; then
              echo "trivia-desktop: $root is not the trivia repository (no app/desktop/main.mjs)" >&2; exit 2
            fi
            ${pkgs.lib.optionalString (pkgs.stdenv.hostPlatform.system == "x86_64-linux") ''export TRIVIA_STEAM_SDK=''${TRIVIA_STEAM_SDK:-${steamSdk pkgs}}''}
            exec electron "$root/app/desktop" "$@"
          '';
        };
        # SteamCMD (D-93) in its own HOME, so its self-update and login cache stay out of the Steam client's root.
        steamcmd = pkgs.writeShellApplication {
          name = "steamcmd";
          text = ''
            home=''${TRIVIA_STEAMCMD_HOME:-''${XDG_DATA_HOME:-$HOME/.local/share}/trivia/steamcmd}
            mkdir -p "$home"
            HOME=$home exec ${pkgs.steamcmd}/bin/steamcmd "$@"
          '';
        };
        trivia-steam = fromCheckout pkgs "trivia-steam" "authoring/steam/steam.py" [ steamcmd ];
        # Local builds for Windows and Linux (plan 56): pool check, client, staged media, electron-builder.
        # `--dir`: also the dir target (release/{win,linux}-unpacked/, plan 89).
        trivia-desktop-build = pkgs.writeShellApplication {
          name = "trivia-desktop-build";
          runtimeInputs = [ pkgs.git pkgs.nodejs_22 qgen ];
          text = ''
            root=$(git rev-parse --show-toplevel 2>/dev/null) || {
              echo "trivia-desktop-build: run this inside the trivia repository" >&2; exit 2; }
            if [ ! -f "$root/app/desktop/electron-builder.yml" ]; then
              echo "trivia-desktop-build: $root is not the trivia repository (no app/desktop/electron-builder.yml)" >&2; exit 2
            fi
            qgen validate
            export ELECTRON_SKIP_BINARY_DOWNLOAD=1  # the npm Electron doesn't run on NixOS
            [ -d "$root/app/desktop/node_modules" ] || npm ci --prefix "$root/app/desktop"
            script=dist
            if [ "''${1:-}" = "--dir" ]; then script=dist:dir; shift; fi  # + unpacked folders for the Steam depots
            exec npm run "$script" --prefix "$root/app/desktop" -- "$@"
          '';
        };
        # Question report server (plan 103, decision 117): wrangler from nixpkgs, run in report-server/.
        trivia-report-server = pkgs.writeShellApplication {
          name = "trivia-report-server";
          runtimeInputs = [ pkgs.git pkgs.wrangler pkgs.openssl pkgs.nodejs_22 ];
          text = ''
            root=$(git rev-parse --show-toplevel 2>/dev/null) || {
              echo "trivia-report-server: run this inside the trivia repository" >&2; exit 2; }
            if [ ! -f "$root/report-server/wrangler.toml" ]; then
              echo "trivia-report-server: $root is not the trivia repository (no report-server/wrangler.toml)" >&2; exit 2
            fi
            cd "$root/report-server"
            export WRANGLER_SEND_METRICS=false
            cmd=''${1:-}; shift || true
            case "$cmd" in
              dev)  # local D1, fake tickets; extra args to `wrangler dev` (e.g. --test-scheduled)
                if [ ! -f .dev.vars ]; then
                  {
                    echo "DEV_FAKE_TICKETS=1"
                    echo "PULL_TOKEN=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '=')"
                    echo "HASH_SALT=$(openssl rand -hex 32)"
                  } > .dev.vars
                fi
                echo "pull token: $(sed -n 's/^PULL_TOKEN=//p' .dev.vars)"
                wrangler d1 migrations apply DB --local
                exec wrangler dev --local --ip 127.0.0.1 --port 8787 "$@" ;;
              deploy)
                wrangler d1 migrations apply DB --remote
                exec wrangler deploy "$@" ;;
              tail) exec wrangler tail --format pretty "$@" ;;
              secret) exec wrangler secret put "$@" ;;  # STEAM_WEB_API_KEY, PULL_TOKEN, HASH_SALT
              seed-telemetry) exec node seed-telemetry.mjs "$@" ;;  # dev only: [N] [URL], localhost
              *) echo "usage: trivia-report-server dev|deploy|tail|secret <NAME>|seed-telemetry [N] [URL]" >&2; exit 2 ;;
            esac
          '';
        };
        # Screen gallery (plan 100, decision 115): nixpkgs Playwright, Chromium only.
        trivia-gallery = pkgs.writeShellApplication {
          name = "trivia-gallery";
          runtimeInputs = [ pkgs.git pkgs.nodejs_22 (pkgs.python3.withPackages (p: [ p.playwright ])) ];
          text = ''
            root=$(git rev-parse --show-toplevel 2>/dev/null) || {
              echo "trivia-gallery: run this inside the trivia repository" >&2; exit 2; }
            if [ ! -f "$root/authoring/tools/gallery.py" ]; then
              echo "trivia-gallery: $root is not the trivia repository (no authoring/tools/gallery.py)" >&2; exit 2
            fi
            export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers.override { withFirefox = false; withWebkit = false; }}
            export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
            exec python3 "$root/authoring/tools/gallery.py" "$@"
          '';
        };
        # Before every Steam upload (SW-6, plan 89); nix, steam-run and Xvfb from the dev shell.
        trivia-release-check = fromCheckout pkgs "trivia-release-check" "authoring/steam/release_check.py"
          [ pkgs.nodejs_22 qgen trivia-media trivia-desktop-build trivia-steam ];
      };
    in {
      packages = forAll (pkgs:
        let tools = authoringTools pkgs; in {
          # What ships (D-35): app/ only. Game state and the media cache go to
          # $XDG_DATA_HOME/trivia/ unless TRIVIA_STATE / TRIVIA_MEDIA say otherwise.
          app = pkgs.buildNpmPackage {
            pname = "trivia";
            version = (builtins.fromJSON (builtins.readFile ./app/desktop/package.json)).version;  # D-91
            src = pkgs.lib.fileset.toSource {
              root = ./.;
              fileset = pkgs.lib.fileset.unions [ ./package.json ./package-lock.json ./app ];
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
          default = self.packages.${pkgs.stdenv.hostPlatform.system}.app;
          # The authoring commands, for `nix run .#qgen` etc. They never ship.
          authoring = pkgs.symlinkJoin {
            name = "trivia-authoring";
            paths = with tools; [ qgen trivia-media trivia-authoring ];
          };
        } // { inherit (tools) qgen trivia-media trivia-authoring trivia-report-server; });

      devShells = forAll (pkgs:
        let tools = authoringTools pkgs; in {
          default = pkgs.mkShell {
            packages = [
              pkgs.nodejs_22 pkgs.python3 pkgs.imagemagick pkgs.claude-code pkgs.electron
              tools.qgen tools.trivia-media tools.trivia-authoring tools.trivia-dev tools.trivia-desktop
              tools.trivia-desktop-build tools.trivia-report-server tools.trivia-gallery
              pkgs.xvfb  # authoring/store/screenshots.mjs, authoring/steam/smoke.mjs
            ] ++ nixpkgs.lib.optionals (pkgs.stdenv.hostPlatform.system == "x86_64-linux") [
              tools.trivia-steam tools.trivia-release-check tools.steamcmd  # SteamCMD: x86_64-linux only
              # smoke.mjs: an FHS runtime like Steam's, plus what Electron links
              (pkgs.steam.override { extraLibraries = p: with p; [ nss nspr gtk3 atk at-spi2-atk at-spi2-core libxcomposite ]; }).run
            ]
              ++ nixpkgs.lib.optional (pm.packages ? ${pkgs.stdenv.hostPlatform.system}) pm.packages.${pkgs.stdenv.hostPlatform.system}.default;
          };
        });
    };
}
