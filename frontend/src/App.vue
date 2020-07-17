<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
  :root {
    --primary: #202442;
    --primary-dark: #070B1F;
    --primary-dark-alt: #25294A;
    --tertiary: #3b54ec;
    --tertiary-alt: rgba(59, 84, 236, 0.1);
    --dim-white: rgba(248, 248, 255, 0.8);
  }

  #app {
    width: 100%;
    height: 100vh;
  }

  .page {
    height: 100%;
    width: 100%;
  }

  .m-0 {
    margin: 0 !important;
  }

  .modal, .modal-content {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal__card {
    background-color: ghostwhite;
    border-radius: 6px;
    height: auto;
    width: auto;
    padding: 1.5rem 2rem;
  }

  .modal__card__title {
    font-size: 16px;
    font-weight: 400;
    color: #000000;
    text-align: center;
    margin-bottom: 1rem;
  }

  .modal__form {
    .modal__form__group:nth-child(even) {
      margin: 0.8rem 0;
    } 

    .form__group__label {
      display: block;
      font-size: 12px;
      text-transform: capitalize;
      color: grey;
      margin-bottom: 0.2rem;
      font-weight: 400;
    }

    .form__group__input {
      width: 100%;
      font-size: 13px;
      height: 32px;
      border-radius: 4px;
      border: 1px solid gainsboro;
      padding: 0 0.5rem;
      box-sizing: border-box;
      color: #4a4a4a;
      margin-bottom: 8px;

      &.form__group__input-invalid {
        border-color: crimson;
      }

      &:focus {
        border-color: #4a4a4a;
      }
    }

    .modal__form__divider {
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 500;
      color: lightslategray;
      margin: 1rem 0 0.5rem 0;
    }

    .modal__form__flex {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }

    .form__group__input-select {
      background-color: white;

      option {
        text-transform: capitalize;
      }
    }

    .form__group__info {
      font-size: 12px;
      color: grey;
      display: block;
      font-weight: 400;
    }

    .modal__form__flex-inputonly {
      .form__group__input {
        width: auto;
        &:not(:last-child) {
          margin-right: 16px;
        }
      }
    }

    .modal__form__controls {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      justify-content: space-between;
      margin-top: 2rem;
    }

    .modal__form__cancel, .modal__form__submit, .modal__form__danger {
      font-size: 13px;
      padding: 0 1.5rem;
      margin-bottom: 8px;
    }

    .modal__form__cancel {
      background-color: rgba(211, 211, 211, 0.2);
      border: none;

      &:hover {
        color: white;
        background-color: lightgrey;
      }
    }

    .modal__form__submit {
      background-color: var(--tertiary);
      border: none;
      color: white;

      &:hover {
        color: var(--tertiary);
        background-color: var(--tertiary-alt)
      }
    }

    .modal__form__danger {
      margin-right: 8px;
      background-color: crimson;
      border: none;
      color: white;

      &:hover {
        background-color: rgba(219, 20, 60, 0.3);
        color: crimson;
      }
    }
  }

  input::placeholder {
    color: lightgray;
  }

  .label__required {
    color: crimson;
  }

  @media screen and (max-width: 768px) {
    .modal-content {
      max-height: 100%;
    }
  }

  .swal-modal {
    width: 360px;

    .swal-title {
      padding: 0;
      font-size: 20px;
    }

    .swal-button--confirm {
      background-color: var(--tertiary);
    }

    .swal-button--danger {
      background-color: crimson;
    }
  }

  .vgt-table {
    background-color: transparent !important;

    thead th {
      border: 1px solid var(--tertiary) !important;
      background: var(--tertiary-alt) !important;

      span {
        color: var(--dim-white);
      }

      &:before, &:after {
        display: none;
      }
    }

    tbody td {
      border: 1px solid var(--tertiary) !important;
      span {
        color: var(--dim-white);
        text-transform: capitalize !important;
      }
    }
  }

  .vgt-wrap__footer {
    border: 1px solid var(--tertiary) !important;
    background: transparent !important;

    .footer__row-count {
      display: none;
    }

    span, a, div, select {
      color: var(--dim-white) !important;
    }
  }

  .form__group__input-currency {
    -moz-appearance: textfield;

    &::-webkit-outer-spin-button, &::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }

  .load__more__btn {
    display: block;
    margin: 1rem auto;
    padding: 1rem 2rem;
    border-radius: 4px;
    border: none;
    background-color: #3b53ec1e;
    color: var(--tertiary);
    line-height: inherit;
    height: inherit;
    cursor: pointer;
    font-size: 14px;

    &:hover {
      color: var(--dim-white);
      background-color: var(--tertiary);   
    }
  }

  .appreciation__history {
    .container {
      margin: 1rem;
      background-color: var(--tertiary-alt);
      border-radius: 6px;
      padding: 16px;
      padding-bottom: 24px;
    }
    
    .appreciation {
      width: 100%;
      padding-top: 4px;

      .appreciation__info {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
      }

      .appreciation__date {
        color: var(--dim-white);
        font-size: 16px;
      }

      .transaction__amount {
        color: var(--tertiary);
        font-size: 20px;
      }

      &:not(:last-child) {
        border-bottom: 0.5px solid var(--dim-white);
        margin-bottom: 4px;
        padding-bottom: 10px;
      }

      .appreciation__amount {
        font-size: 16px;
        color: var(--tertiary);

        &.appreciation__amount-old {
          color: var(--dim-white);
        }
      }

      .appreciation__arrow {
        font-size: 16px;
        margin: 0 0.5rem;
        color: green;
      }
    }
  }
</style>
