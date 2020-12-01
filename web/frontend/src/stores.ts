import { writable } from "svelte/store";

export const GeneratorSettingStore = writable({
  outputLength: 50,
  numOutput: 1,
  trimEnding: true,
});

export const SelectedModelStore = writable(null);
