<script>
  import Card from "./Card.svelte";

  export let generatedText;
  export let onRemoveGenerateText;
</script>

<style>
  .container {
    margin: 20px 0;
    color: #333;
  }

  .inner {
    padding: 20px;
  }

  .prompt {
    border-bottom: 1px solid #999;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }

  .remove {
    margin-left: 10px;
    cursor: pointer;
    color: #f33;
    font-size: 10pt;
  }
  
  .remove:hover {
    color: #633;
  }

  .result {
    border: 1px dotted #ccc;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 10px;
    background-color: #f8f8f8;
  }

  .model {
    font-size: 10pt;
    background-color: #999;
    color: #eee;
    padding: 4px 8px;
    border-radius: 8px;
  }

</style>

<div class="container">
  <Card>
    <div class="inner">
      <div class="prompt">
        {generatedText.promptText}
        <span class="remove" on:click|preventDefault={() => onRemoveGenerateText(generatedText.id)}>Remove</span>
      </div>

      {#each generatedText.results as result}
        <div class="result">{result}</div>
      {/each}

      <span class="model">{generatedText.model}</span>
    </div>
  </Card>
</div>
