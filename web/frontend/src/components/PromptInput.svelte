<script>
  import Card from "./Card.svelte";
  import Button from "./Button.svelte";
  import LoadingOverlay from "./LoadingOverlay.svelte";

  export let onGenerate;
  export let isGenerating;

  let promptText = "";
  $: isGenerateButtonDisabled = promptText.trim().length === 0;

  function onGenerateClicked(e) {
    e.preventDefault();
    onGenerate(promptText);
    promptText = ""
  }
</script>

<style>
  .container {
    position: relative;
  }

  h2 {
    margin: 0;
    padding: 0 20px;
    padding-top: 20px;

    color: #333;
  }

  form {
    padding: 20px;
    text-align: right;
  }

  textarea {
    box-sizing: border-box;
    width: 100%;
    font-size: 12pt;
    line-height: 1.5em;
    height: calc(4.5em + 16px);
    resize: vertical;
    padding: 8px;
    margin-bottom: 8px;
    border-color: #ccc;

    -webkit-appearance: none;
  }

  textarea:focus {
    outline: none;
  }
</style>

<Card>
  <div class="container">
    <h2>Prompt</h2>
    <form>
      <textarea
        bind:value="{promptText}"
        placeholder="Enter the prompt there..."></textarea>
      <Button
        type="submit"
        disabled="{isGenerateButtonDisabled}"
        on:click="{onGenerateClicked}">
        Generate
      </Button>
    </form>
    <LoadingOverlay show="{isGenerating}" />
  </div>
</Card>
