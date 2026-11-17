// Shipped video encode (decision 185; 8 Mbit/s ceiling, milestone 21: a ceiling against huge files, not a squeeze; libvpx-vp9 needs -b:v 8M, not 0, with -maxrate: constrained quality), shared by stage-media.mjs and the dev servers' playable copies (playable.mjs).
export const VIDEO = [
  ...["-map", "0:v:0", "-map", "0:a:0?"],
  ...["-vf", "scale=w=min(1920\\,iw):h=min(1080\\,ih):force_original_aspect_ratio=decrease:force_divisible_by=2"],
  ...["-c:v", "libvpx-vp9", "-crf", "33", "-b:v", "8M", "-maxrate", "8M", "-bufsize", "16M", "-row-mt", "1", "-deadline", "good", "-cpu-used", "2"],
  ...["-c:a", "libopus", "-b:a", "96k"],
];
