<script>
  export let show;
</script>

<style>
  .overlay {
    display: flex;
    justify-content: center;
    align-items: center;
    
    position: absolute;
    top: 0px;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.7);
    color: #333;
  }

  .loader-container {
  }

  .loader {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
  }
  .loader div {
    position: absolute;
    top: 33px;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #666;
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
  }
  .loader div:nth-child(1) {
    left: 8px;
    animation: loader1 0.6s infinite;
  }
  .loader div:nth-child(2) {
    left: 8px;
    animation: loader2 0.6s infinite;
  }
  .loader div:nth-child(3) {
    left: 32px;
    animation: loader2 0.6s infinite;
  }
  .loader div:nth-child(4) {
    left: 56px;
    animation: loader3 0.6s infinite;
  }
  @keyframes loader1 {
    0% {
      transform: scale(0);
    }
    100% {
      transform: scale(1);
    }
  }
  @keyframes loader3 {
    0% {
      transform: scale(1);
    }
    100% {
      transform: scale(0);
    }
  }
  @keyframes loader2 {
    0% {
      transform: translate(0, 0);
    }
    100% {
      transform: translate(24px, 0);
    }
  }
</style>

{#if show}
<div class="overlay">
  <div class="loader-container">
    <div class="loader"><div></div><div></div><div></div><div></div></div>
  </div>
</div>
{/if}
