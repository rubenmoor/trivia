// Dev server's page shim (plan 99): the save half of the desktop bridge over /@trivia/save, no Steam. Never in dist/.
// The server appends `muted = true` under PM_WORKER/TRIVIA_MUTE=1 (plan 123).
(() => {
  async function call(method, path = "", body = undefined) {
    const res = await fetch(`/@trivia/save${path}`, { method, body });
    if (!res.ok) throw new Error((await res.json().catch(() => null))?.error ?? `save_${res.status}`);
    return res;
  }
  const no = (value) => () => Promise.resolve(value);
  window.triviaShell = {
    desktop: true,
    devServer: true,
    isFullscreen: async () => !!document.fullscreenElement,
    setFullscreen: async (yes) => {
      if (!yes) await document.exitFullscreen().catch(() => {});
      else await document.documentElement.requestFullscreen().catch(() => {});
    },
    onFullscreen: (cb) => {
      const on = () => cb(!!document.fullscreenElement);
      document.addEventListener("fullscreenchange", on);
      return () => document.removeEventListener("fullscreenchange", on);
    },
    quit: no(undefined),
    loadSave: async () => {
      const res = await call("GET");
      return res.status === 204 ? null : res.text();
    },
    writeSave: async (text) => {
      await call("PUT", "", text);
    },
    backupSave: async (kind) => (await (await call("POST", `/backup?kind=${encodeURIComponent(kind)}`)).json()).path,
    steam: {
      available: false,
      user: false,
      dev: false,
      steamId: no(null),
      language: no(null),
      overlay: { enabled: no(false) },
      showTextInput: no(false),
      inputTypes: no(null),
      setPresence: no(undefined),
      unlock: no(false),
    },
  };
})();
