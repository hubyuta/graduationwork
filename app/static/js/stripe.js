const stripe = Stripe('pk_test_51M3tRAGbiMLnjNfpWjSVAMduqxgnNsxCFB8XfkZjYKKaXZ0H4dpZkvwop2istMFpIi0jUdyJjCXAVGVarsh3wBzJ001XufrOpR');
const elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
const style = {
    base: {
      // Add your base input styles here. For example:
      fontSize: '16px',
      color: '#32325d',
      amount: 100,
      currency: 'jpy',
      payment_method_types: ['apple_pay', 'google_pay', 'card'],
      payment_method_configuration: 'pmc_1OZZRrGbiMLnjNfpjFsVghQl',
      automatic_payment_methods: {
            enabled: true,
      },
    },
};
  
// Create an instance of the card Element.
const card = elements.create('card', {style});
// const card = elements.create('apple_pay', 'google_pay','card', {style});
  
// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Create a token or display an error when the form is submitted.
const form = document.getElementById('payment-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {token, error} = await stripe.createToken(card);

  if (error) {
    // Inform the customer that there was an error.
    const errorElement = document.getElementById('card-errors');
    errorElement.textContent = error.message;
  } else {
    // Send the token to your server.
    stripeTokenHandler(token);
  }
});

const stripeTokenHandler = (token) => {
    // Insert the token ID into the form so it gets submitted to the server
    const form = document.getElementById('payment-form');
    const hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
  
    // Submit the form
    form.submit();
}