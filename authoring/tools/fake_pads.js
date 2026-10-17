// Fake standard pads for an init script (trivia-gallery, the packaged smoke's --multiplayer; decision 199): callers run
// `(${src})(ids)`, ids null or one per pad connected at load (null: the default id).
// `__pads(n, ids)` connects n (mixed Xbox/PlayStation ids), `__press(button, pad = 0)` presses and releases one (letter
// pickers open from the pad only); `__padOff(pad)` unplugs it. The first press connects one pad.
(initial) => {
  const IDS = [
    "Xbox 360 Controller (STANDARD GAMEPAD)",
    "Wireless Controller (STANDARD GAMEPAD Vendor: 054c Product: 09cc)",
  ];
  const made = (index, id) => ({
    id, index, mapping: "standard", connected: true, timestamp: 0,
    axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })),
  });
  let pads = [];
  navigator.getGamepads = () => pads;
  const plug = (n, ids) => {
    pads = Array.from({ length: n }, (_, i) => made(i, ids?.[i] ?? IDS[i % IDS.length]));
    for (const g of pads) window.dispatchEvent(Object.assign(new Event("gamepadconnected"), { gamepad: g }));
  };
  if (initial) pads = initial.map((id, i) => made(i, id ?? IDS[i % IDS.length]));
  window.__pads = (n, ids) => plug(n, ids);
  window.__padOff = (i) => {
    const g = pads[i];
    pads[i] = null;
    window.dispatchEvent(Object.assign(new Event("gamepaddisconnected"), { gamepad: g }));
  };
  window.__press = async (b, i = 0) => {
    if (!pads.length) {
      plug(1);
      await new Promise((r) => setTimeout(r, 100));
    }
    const pad = pads[i];
    pad.buttons[b] = { pressed: true, touched: true, value: 1 };
    await new Promise((r) => setTimeout(r, 120));
    pad.buttons[b] = { pressed: false, touched: false, value: 0 };
    await new Promise((r) => setTimeout(r, 120));
  };
}
