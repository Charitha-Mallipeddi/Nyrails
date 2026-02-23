

class ManualPaymentToggle {
  constructor() {
    this.manualPaymentBtn = document.querySelector("#manual-payment-btn");
    this.manualPaymentForm = document.querySelector("#manual-payment-form");
    this.isManualPayment = document.querySelector("input[name='is_manual_payment']");

    this.amountDue = document.querySelector("input[name='amount_due']");
    this.amountPaid = document.querySelector("input[name='amount_paid']");
    this.balance = document.querySelector("input[name='balance']");

    this.init();
  }

  init() {
    this.manualPaymentBtn.addEventListener("click", (e) => this.toggle());
    this.amountPaid.addEventListener("input", (e) => this.updateBalance());
    this.amountDue.addEventListener("input", (e) => this.updateBalance());
  }

  updateBalance() {
    const amountDue = parseFloat(this.amountDue.value || 0);
    const amountPaid = parseFloat(this.amountPaid.value || 0);
    const finalBalance = Math.max(0, amountDue - amountPaid);
    this.balance.value = finalBalance.toFixed(2);
  }

  toggle() {
    if (!this.manualPaymentForm) {
      return;
    }

    if (this.manualPaymentForm.classList.contains("d-none")) {
      this.manualPaymentForm.classList.remove("d-none");
      this.manualPaymentBtn.innerHTML = "Remove Manual Payment";
      this.isManualPayment.checked = true;
      this.isManualPayment.value = "true";
    } else {
      this.manualPaymentForm.classList.add("d-none");
      this.manualPaymentBtn.innerHTML = "Add Manual Payment";
      this.isManualPayment.checked = false;
      this.isManualPayment.value = "false";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new ManualPaymentToggle();
});
