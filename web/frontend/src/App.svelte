<script>
  import {onMount, onDestroy} from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { v4 as uuid4 } from 'uuid';

  import Toolbar from "./components/ToolBar.svelte";
  import PromptInput from "./components/PromptInput.svelte";
  import LoadingOverlay from './components/LoadingOverlay.svelte';
  import GeneratedTextCard from './components/GeneratedTextCard.svelte';

  import {SelectedModelStore, GeneratorSettingStore} from './stores'

  import {HTTPAPIClient} from "./api"

  const apiClient = new HTTPAPIClient();

  let existingModels = null;
  let isLoadingModel = false;
  let isGenerating = false;

  let generatedTexts = loadGeneratedTexts();
  const GeneratedTextHistorySize = 100;

  let selectedModel;
  let generatorSetting;

  const unsubscribeSelectedModelStore = SelectedModelStore.subscribe(v => {
    selectedModel = v;
    console.log('>>',selectedModel)
  });
  
  const unsubscribeGeneratorSettingStore = GeneratorSettingStore.subscribe(v => {
    generatorSetting = v;
  });

  onMount(() => {
    apiClient.getModels().then(models => {
      existingModels = models;
    });

    apiClient.getCurrentModel().then(model => {
      console.log(model)
      SelectedModelStore.update(_ => model);
    });
  });

  onDestroy(() => {
    unsubscribeSelectedModelStore();
    unsubscribeGeneratorSettingStore();
  });

  function onChangeModel(model) {
    SelectedModelStore.update(_ => model);
    isLoadingModel = true;
    return apiClient.loadModel(model).finally(() => {
      isLoadingModel = false;
    })
  }

  function onGenerate(promptText) {
    apiClient.getCurrentModel().then(model => {
      const promise = (model !== selectedModel) ? onChangeModel(selectedModel) : Promise.resolve(null);
      promise.then(() => {
        doGenerate(promptText);
      })
    })
  }

  function doGenerate(promptText) {
    isGenerating = true;
    apiClient.generate(promptText, generatorSetting)
      .then(results => {
        
        generatedTexts = [{
          id: uuid4(),
          promptText,
          results,
          model: selectedModel,
        }, ...generatedTexts.slice(0, GeneratedTextHistorySize-1)];

        saveGeneratedTexts();
      })
      .finally(() => {
        isGenerating = false
      })
  }

  function onClearHistory() {
    generatedTexts = []
    saveGeneratedTexts();
  }

  function onRemoveGenerateText(id) {
    generatedTexts = generatedTexts.filter(x => x.id !== id)
    saveGeneratedTexts();
  }

  function saveGeneratedTexts() {
    window.localStorage.setItem("generatedTexts", JSON.stringify(generatedTexts));
  }

  function loadGeneratedTexts() {
    const data = window.localStorage.getItem("generatedTexts");
    if (data) {
      return JSON.parse(data);
    }

    return [];
  }

</script>

<style>
  main {
    padding: 20px;
    max-width: 960px;
    margin: 0 auto;
  }

  @media (max-width: 960px) {
    main {
      max-width: none;
    }
  }
</style>

<Toolbar 
  models={existingModels || []} 
  selectedModel={selectedModel}
  onChangeModel={onChangeModel}
  onClearHistory={onClearHistory} />
<main>
  <PromptInput {onGenerate} {isGenerating} />
  {#each generatedTexts as generatedText (generatedText.id)}
    <div in:fly="{{ y: 100, duration: 500 }}" out:fade>
      <GeneratedTextCard {generatedText} {onRemoveGenerateText} />
    </div>
  {/each}
</main>
<LoadingOverlay show={existingModels === null || selectedModel == null || isLoadingModel}/>
