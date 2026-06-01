// Shared helpers for the manuscript.

// Authoring note (mirrors the old LaTeX \hly{} outline scaffolding).
#let todo(body) = block(
  fill: rgb("#fff3bf"), inset: 6pt, radius: 3pt, width: 100%,
  text(fill: rgb("#664d03"), size: 9pt)[*note:* #body],
)
