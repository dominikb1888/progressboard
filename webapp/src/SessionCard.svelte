<script>
  export let session;
</script>

<div class="session-card">
  <a class="exercise" href={session.url}>{session.exercise}</a>
</div>

<style>
  .session-card {
    background-color: white;
    border-radius: 20px;
    --tw-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
      0 10px 10px -5px rgba(0, 0, 0, 0.04);
    box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
      var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
  }
  .session-image {
    max-width: 1rem;
    margin-top: 10px;
  }
  .session-name {
    font-size: 8px;
    font-weight: bold;
    margin-top: 3px;
  }
  .session-details {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    border-top: 1px solid #d1d5db;
    background-color: #f3f4f6;
  }
  .detail-field {
    font-size: 8px;
    font-weight: bold;
    padding: 15px 0;
  }
  .detail-field:not(:last-child) {
    border-right: 1px solid #d1d5db;
  }
  .price-change {
    color: #dc2626;
  }
  .positive {
    color: #16a34a;
  }
  @media (min-width: 1024px) {
    .detail-field {
      font-size: 18px;
      padding: 15px;
    }
  }
</style>
