  // Quantity Plus & Minus functionality
  const qtyInput = document.getElementById('qty');
  document.getElementById('btn-plus').addEventListener('click', () => {
    let currentVal = parseInt(qtyInput.value) || 1;
    if (currentVal < parseInt(qtyInput.max)) qtyInput.value = currentVal + 1;
  });
  
  document.getElementById('btn-minus').addEventListener('click', () => {
    let currentVal = parseInt(qtyInput.value) || 1;
    if (currentVal > parseInt(qtyInput.min)) qtyInput.value = currentVal - 1;
  });