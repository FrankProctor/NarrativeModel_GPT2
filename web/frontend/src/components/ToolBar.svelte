<script>
  import {onDestroy} from 'svelte';
  import {GeneratorSettingStore} from "../stores";

  export let models;
  export let selectedModel;
  export let onChangeModel;
  export let onClearHistory;

  let outputLength;
  let numOutput;
  let trimEnding;

  const unsubscribe = GeneratorSettingStore.subscribe(setting => {
    outputLength = setting.outputLength;
    numOutput = setting.numOutput;
    trimEnding = setting.trimEnding;
  });

  onDestroy(() => {
    unsubscribe();
  })

  function onOutputLengthChange() {
    outputLength = Math.max(10, outputLength) || 10;
    GeneratorSettingStore.update(v => ({ ...v, outputLength }));
  }

  function onNumOutputChange() {
    numOutput = Math.max(1, numOutput) || 1;
    GeneratorSettingStore.update(v => ({ ...v, numOutput }));
  }

  function onTrimEndingChange() {
    GeneratorSettingStore.update(v => ({ ...v, trimEnding }));
  }
</script>

<style>
  header {
    background-color: #ccc;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.15);
    margin-bottom: 20px;
    padding: 5px 20px;

    color: #333;
  }

  ul {
    margin: 0;
    padding: 0;
  }

  li {
    display: inline-block;
    margin-right: 20px;
    font-size: 10pt;
    height: 3em;
    line-height: 3em;
  }

  li:last-child {
    margin-right: 0;
  }

  li > input[type="number"] {
    width: 45px;
    text-align: center;
    background: transparent;
    border: 0;
    color: #666;
    border-bottom: 1px dashed #666;
    border-radius: 0;
  }
  
  li > input[type="radio"] {
    margin-left:4px;
    margin-right: 2px;
  }

  li > input:focus, li > select:focus {
    outline: none;
  }

  li > label {
    font-weight: 300;
  }

  li > label:after {
    font-weight: normal;
    content: " :";
  }

  a, a:visited {
    color: #333;
    text-decoration: none;
  }

  a:hover {
    color: #999;
  }
</style>

<header>
  <ul>
    <li>
      <label>Model</label>
      <select bind:value={selectedModel} on:change="{() => onChangeModel(selectedModel)}">
        {#each models as model}
          <option value={model} selected={selectedModel===model}>{model}</option>
        {/each}
      </select>
    </li>
    <li>
      <label>Output Length</label>
      <input
        type="number"
        inputmode="numeric"
        pattern="[0-9]+"
        bind:value="{outputLength}"
        on:change="{onOutputLengthChange}" />
    </li>
    <li>
      <label># Output</label>
      <input
        type="number"
        inputmode="numeric"
        pattern="[0-9]+"
        bind:value="{numOutput}"
        on:change="{onNumOutputChange}" />
    </li>
    <li>
      <label>Trim Ending</label>
      <input 
        type="radio" 
        bind:group={trimEnding} 
        value={true} 
        on:change={onTrimEndingChange}/>
      Yes
      <input 
        type="radio" 
        bind:group={trimEnding} 
        value={false} 
        on:change={onTrimEndingChange}/>
      No
    </li>
    <li>
      <a href="/" on:click|preventDefault={onClearHistory} >Clear History</a>
    </li>
  </ul>
</header>
