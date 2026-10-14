// Example full conversion (MIT): guess the number with keyboard, pad or mouse.
const shell = window.triviaShell; // the game's desktop bridge; missing in a plain browser
const $ = (id) => document.getElementById(id);
let secret = 1 + Math.floor(Math.random() * 100);
let guess = 50;
let tries = 0;

function step(by) {
  guess = Math.min(100, Math.max(1, guess + by));
  $("guess").textContent = guess;
}

function submit() {
  tries++;
  if (guess === secret) {
    $("hint").textContent = `Yes, ${secret}! ${tries} tries. New number picked.`;
    secret = 1 + Math.floor(Math.random() * 100);
    tries = 0;
  } else {
    $("hint").textContent = guess < secret ? "Higher." : "Lower.";
  }
}

const quit = () => (shell ? shell.quit() : window.close());

$("down").onclick = () => step(-1);
$("up").onclick = () => step(1);
$("go").onclick = submit;
$("quit").onclick = quit;
addEventListener("wheel", (e) => step(e.deltaY < 0 ? 1 : -1));
addEventListener("keydown", (e) => {
  const keys = { ArrowUp: () => step(1), ArrowDown: () => step(-1), PageUp: () => step(10), PageDown: () => step(-10),
    Enter: submit, " ": submit, Escape: quit };
  if (keys[e.key]) {
    e.preventDefault();
    keys[e.key]();
  }
});

// Pad (standard mapping): A 0, B 1, d-pad up 12, down 13; act on press, not while held.
const held = new Set();
function poll() {
  for (const pad of navigator.getGamepads()) {
    if (!pad) continue;
    const acts = { 0: submit, 1: quit, 12: () => step(1), 13: () => step(-1) };
    for (const [i, act] of Object.entries(acts)) {
      const key = `${pad.index}:${i}`;
      if (pad.buttons[i]?.pressed && !held.has(key)) act();
      if (pad.buttons[i]?.pressed) held.add(key);
      else held.delete(key);
    }
  }
  requestAnimationFrame(poll);
}
poll();

// Tell the shell this start worked; otherwise the next start runs without mods.
shell?.mods?.ready();
