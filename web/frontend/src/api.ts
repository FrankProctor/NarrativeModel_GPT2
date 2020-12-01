import { GeneratorSetting } from "./models";

export interface APIClient {
  getModels: () => Promise<string[]>;
  loadModel: (modelName: string) => Promise<void>;
  generate: (
    promptText: string,
    setting: GeneratorSetting
  ) => Promise<string[]>;
}

export class HTTPAPIClient implements APIClient {
  private baseURL: string;

  constructor() {
    this.baseURL = window.location.origin;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private processResponse<T>(resp: any): T {
    if (resp.status === "failed") {
      throw resp.error;
    } else if (resp.status === "ok") {
      return resp.result || null;
    }

    throw "Unexpected response";
  }

  private get<T>(endpoint: string): Promise<T> {
    return fetch(`${this.baseURL}/api/${endpoint}`)
      .then(resp => resp.json())
      .then(resp => this.processResponse(resp));
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private post<T>(endpoint: string, payload: any): Promise<T> {
    return fetch(`${this.baseURL}/api/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then(resp => resp.json())
      .then(resp => this.processResponse(resp));
  }

  getModels(): Promise<string[]> {
    return this.get("models");
  }
  
  getCurrentModel(): Promise<string> {
    return this.get("model");
  }

  async loadModel(model: string): Promise<void> {
    await this.post("load-model", { model });
  }

  generate(promptText: string, setting: GeneratorSetting): Promise<string[]> {
    return this.post("generate", {
      "prompt_text": promptText,
      "output_length": setting.outputLength,
      "num_output": setting.numOutput,
      "trim_ending": setting.trimEnding,
    });
  }
}
