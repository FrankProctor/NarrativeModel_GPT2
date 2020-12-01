export interface GeneratorSetting {
  readonly outputLength: number;
  readonly numOutput: number;
  readonly trimEnding: boolean;
}

export interface GeneratedText {
  readonly id: string;
  readonly promptText: string;
  readonly results: string[];
  readonly model: string;
}
