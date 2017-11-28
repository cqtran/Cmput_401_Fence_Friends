function confirmDiscard() {
  return "Discard changes?";
}

function markDirty() {
  window.onbeforeunload = confirmDiscard;
}

function markClean() {
  window.onbeforeunload = null;
}