<script lang="ts" module>
  // Fireworks (plans/04-ui-tv-display.md, "Correct", UI-9): a full-screen transparent canvas over
  // the screen, hand-written particles, no library. Five variants, one picked at random on
  // ¡Correcto!; Victory plays the finale (all of them in sequence, then a last volley).
  // Preview on the Start screen: /?fuegos=rockets|confetti|shapes|sparklers|stars|finale
  export type FireworksMode = "single" | "finale";
</script>

<script lang="ts">
  import { onMount } from "svelte";
  import { sfx } from "./sound.svelte";

  let { mode = "single", variant = null }: { mode?: FireworksMode; variant?: string | null } = $props();

  let canvas = $state<HTMLCanvasElement>();

  type Kind = "spark" | "confetti" | "star" | "rocket";
  type P = {
    x: number; y: number; vx: number; vy: number;
    life: number; max: number; color: string; size: number;
    gravity: number; drag: number; kind: Kind;
    spin?: number; angle?: number; wobble?: number;
    onDeath?: () => void;
  };
  type Variant = (at: number) => void; // schedules its events from time `at` (seconds)

  // Theme colours (10-visual-design.md): amber, sky, mint, coral, paper, gold.
  const COLORS = ["#ffb81c", "#4cc9f0", "#2fe39a", "#ff5470", "#eef1f6", "#ffe08a"];
  const pick = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];
  const rand = (a: number, b: number) => a + Math.random() * (b - a);

  onMount(() => {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const c = canvas!;
    const g = c.getContext("2d")!;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    let W = 0, H = 0;
    const resize = () => {
      W = innerWidth;
      H = innerHeight;
      c.width = W * dpr;
      c.height = H * dpr;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    addEventListener("resize", resize);

    const particles: P[] = [];
    const events: { t: number; run: () => void }[] = [];
    const at = (t: number, run: () => void) => events.push({ t, run });
    const u = () => Math.min(W / 120, H / 67.5); // the theme's size unit

    function burst(x: number, y: number, n: number, speed: number, color?: string, shape?: (i: number) => [number, number]) {
      const col = color ?? pick(COLORS);
      for (let i = 0; i < n; i++) {
        const [dx, dy] = shape ? shape(i) : (() => {
          const a = Math.random() * Math.PI * 2, s = Math.sqrt(Math.random());
          return [Math.cos(a) * s, Math.sin(a) * s];
        })();
        particles.push({
          x, y, vx: dx * speed * u(), vy: dy * speed * u(), life: 0, max: rand(1, 1.6),
          color: Math.random() < 0.15 ? "#eef1f6" : col, size: rand(0.15, 0.3) * u(),
          gravity: 12 * u(), drag: 1.6, kind: "spark",
        });
      }
    }

    function rocket(t: number, x: number, peak: number, then: (x: number, y: number) => void) {
      at(t, () => {
        sfx("cohete");
        const p: P = {
          x, y: H + 10, vx: rand(-1.5, 1.5) * u(), vy: -Math.sqrt(2 * 60 * u() * (H - peak)), life: 0, max: 9,
          color: "#ffe08a", size: 0.3 * u(), gravity: 60 * u(), drag: 0, kind: "rocket",
        };
        p.onDeath = () => {
          sfx("estallido");
          then(p.x, p.y);
        };
        particles.push(p);
      });
    }

    const VARIANTS: Record<string, Variant> = {
      rockets(t0) {
        for (let i = 0; i < 5; i++) {
          rocket(t0 + i * 0.45, rand(0.15, 0.85) * W, rand(0.12, 0.38) * H, (x, y) => burst(x, y, 90, 26));
        }
      },
      confetti(t0) {
        at(t0, () => sfx("cañón de confeti"));
        for (const side of [0, 1]) {
          for (let i = 0; i < 160; i++) {
            at(t0 + Math.random() * 0.35, () => {
              const angle = side ? -Math.PI / 2 - rand(0.15, 0.7) : -Math.PI / 2 + rand(0.15, 0.7);
              const s = rand(55, 90) * u();
              particles.push({
                x: side ? W + 5 : -5, y: H - 2 * u(), vx: Math.cos(angle) * s, vy: Math.sin(angle) * s,
                life: 0, max: rand(2.6, 3.6), color: pick(COLORS), size: rand(0.5, 0.9) * u(),
                gravity: 9 * u(), drag: 1.4, kind: "confetti", spin: rand(-8, 8), angle: rand(0, 6), wobble: rand(0, 6),
              });
            });
          }
        }
      },
      shapes(t0) {
        const ring = (n: number) => (i: number): [number, number] => {
          const a = (i / n) * Math.PI * 2;
          return [Math.cos(a), Math.sin(a)];
        };
        const heart = (n: number) => (i: number): [number, number] => {
          const a = (i / n) * Math.PI * 2;
          return [(16 * Math.sin(a) ** 3) / 17, -(13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a)) / 17];
        };
        rocket(t0, 0.3 * W, 0.3 * H, (x, y) => burst(x, y, 80, 22, "#4cc9f0", ring(80)));
        rocket(t0 + 0.6, 0.7 * W, 0.28 * H, (x, y) => burst(x, y, 90, 20, "#ff5470", heart(90)));
        rocket(t0 + 1.2, 0.5 * W, 0.2 * H, (x, y) => {
          burst(x, y, 70, 26, "#ffb81c", ring(70));
          burst(x, y, 50, 14, "#2fe39a", ring(50));
        });
      },
      sparklers(t0) {
        for (let k = 0; k < 3; k++) {
          const cx = (0.25 + k * 0.25) * W, cy = 0.45 * H, r = 0.12 * H, phase = k * 2;
          for (let s = 0; s < 70; s++) {
            const t = t0 + s * 0.035;
            at(t, () => {
              const a = phase + s * 0.18;
              const x = cx + Math.cos(a) * r * 1.3, y = cy + Math.sin(a * 2) * r * 0.6;
              for (let i = 0; i < 4; i++) {
                const d = Math.random() * Math.PI * 2;
                particles.push({
                  x, y, vx: Math.cos(d) * rand(4, 12) * u(), vy: Math.sin(d) * rand(4, 12) * u(),
                  life: 0, max: rand(0.25, 0.55), color: pick(["#ffe08a", "#ffb81c", "#eef1f6"]),
                  size: rand(0.12, 0.22) * u(), gravity: 10 * u(), drag: 2, kind: "spark",
                });
              }
            });
          }
        }
        at(t0, () => sfx("bengalas"));
      },
      stars(t0) {
        for (let i = 0; i < 70; i++) {
          at(t0 + Math.random() * 1.8, () => particles.push({
            x: rand(0, W), y: -10, vx: rand(-2, 2) * u(), vy: rand(6, 14) * u(), life: 0, max: rand(2.6, 3.4),
            color: pick(["#ffe08a", "#ffb81c", "#eef1f6", "#4cc9f0"]), size: rand(0.5, 1.1) * u(),
            gravity: 6 * u(), drag: 0.2, kind: "star", spin: rand(-2, 2), angle: rand(0, 6),
          }));
        }
        at(t0, () => sfx("estrellas"));
      },
    };

    if (mode === "finale") {
      // All variants in sequence, overlapping a little, then a last big volley (04, "Victory").
      ["rockets", "confetti", "shapes", "sparklers", "stars"].forEach((name, i) => VARIANTS[name](0.2 + i * 2.2));
      for (let i = 0; i < 9; i++) rocket(11.4 + i * 0.18, rand(0.1, 0.9) * W, rand(0.1, 0.35) * H, (x, y) => burst(x, y, 110, 30));
      at(12.2, () => VARIANTS.confetti(12.2));
    } else {
      VARIANTS[variant && variant in VARIANTS ? variant : pick(Object.keys(VARIANTS))](0.1);
    }
    events.sort((a, b) => a.t - b.t);

    function star(x: number, y: number, r: number, a: number) {
      g.beginPath();
      for (let i = 0; i < 10; i++) {
        const rr = i % 2 ? r * 0.45 : r;
        const aa = a + (i * Math.PI) / 5;
        g.lineTo(x + Math.cos(aa) * rr, y + Math.sin(aa) * rr);
      }
      g.closePath();
      g.fill();
    }

    let start = performance.now();
    let last = start;
    let raf = 0;
    const frame = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      const t = (now - start) / 1000;
      while (events.length && events[0].t <= t) events.shift()!.run();
      g.clearRect(0, 0, W, H);
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.life += dt;
        p.vx -= p.vx * p.drag * dt;
        p.vy += p.gravity * dt - p.vy * p.drag * dt;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (p.kind === "rocket" && p.vy >= -2 * u()) p.life = p.max; // apex: explode
        if (p.life >= p.max) {
          particles.splice(i, 1);
          p.onDeath?.();
          continue;
        }
        const fade = 1 - p.life / p.max;
        if (p.kind === "spark" || p.kind === "rocket") {
          g.globalCompositeOperation = "lighter";
          g.globalAlpha = p.kind === "rocket" ? 1 : fade;
          g.fillStyle = p.color;
          g.beginPath();
          g.arc(p.x, p.y, p.size * (p.kind === "rocket" ? 1.4 : 1), 0, Math.PI * 2);
          g.fill();
          if (p.kind === "rocket") {
            for (let k = 0; k < 2; k++) particles.push({
              x: p.x, y: p.y, vx: rand(-3, 3) * u(), vy: rand(2, 6) * u(), life: 0, max: 0.35,
              color: "#ffb81c", size: 0.15 * u(), gravity: 2 * u(), drag: 2, kind: "spark",
            });
          }
        } else if (p.kind === "confetti") {
          g.globalCompositeOperation = "source-over";
          g.globalAlpha = Math.min(1, fade * 2);
          p.angle! += p.spin! * dt;
          p.vx += Math.sin(p.life * 6 + p.wobble!) * 6 * u() * dt; // flutter
          g.save();
          g.translate(p.x, p.y);
          g.rotate(p.angle!);
          g.scale(1, Math.cos(p.life * 9 + p.wobble!)); // tumbling
          g.fillStyle = p.color;
          g.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
          g.restore();
        } else {
          g.globalCompositeOperation = "lighter";
          g.globalAlpha = Math.min(1, fade * 1.5) * (0.7 + 0.3 * Math.sin(p.life * 12));
          p.angle! += p.spin! * dt;
          g.fillStyle = p.color;
          star(p.x, p.y, p.size, p.angle!);
        }
      }
      g.globalAlpha = 1;
      if (events.length || particles.length) raf = requestAnimationFrame(frame);
      else g.clearRect(0, 0, W, H);
    };
    raf = requestAnimationFrame((now) => {
      start = last = now;
      frame(now);
    });
    return () => {
      cancelAnimationFrame(raf);
      removeEventListener("resize", resize);
    };
  });
</script>

<canvas bind:this={canvas} class="fireworks" aria-hidden="true"></canvas>

<style>
  .fireworks {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 15;
    pointer-events: none;
  }
</style>
