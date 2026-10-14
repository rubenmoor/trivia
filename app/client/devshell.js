// Dev server's page shim (plan 99): the save half of the desktop bridge over /@trivia/save, no Steam. Never in dist/.
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
    toggleFullscreen: async () => {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen().catch(() => {});
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
