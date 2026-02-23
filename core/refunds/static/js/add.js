// ============================================================================
// REFUND CALCULATOR
// Calculates final refund amount by subtracting fees from total refund amount
// ============================================================================

class RefundCalculator {
  constructor() {
    // Main refund inputs
    this.amountInput = document.querySelector(
      'input[name="total_amount_of_refund"]'
    );
    this.feeInput = document.querySelector('input[name="fee"]');

    // Display elements
    this.finalDisplay = document.getElementById("final-total");
    this.finalHidden = document.querySelector('input[name="final_refund"]');
    this.container = document.getElementById("final-total-container");

    this.init();
  }

  init() {
    // Listen for changes to amount and fee inputs
    [this.amountInput, this.feeInput].forEach((input) => {
      input?.addEventListener("input", () => this.calculate());
    });

    // Initial calculation
    this.calculate();
    this.addEventListeners();
  }

  calculate() {
    // Get refund amounts from individual ticket rows if they exist
    const ticketRefunds = this.sumTicketRefunds();

    this.amountInput.value = ticketRefunds;

    const fee = this.parseValue(this.feeInput?.value);

    // Calculate final refund (never negative)
    const finalRefund = Math.max(0, ticketRefunds - fee);

    // Update display and hidden input
    this.updateDisplay(finalRefund);
  }

  addEventListeners() {
    document.querySelectorAll(".refund_amount").forEach((n) => {
      n.addEventListener("input", () => this.calculate());
    });
  }

  sumTicketRefunds() {
    const refundInputs = document.querySelectorAll(".refund_amount");
    return Array.from(refundInputs).reduce((sum, input) => {
      return sum + this.parseValue(input.value);
    }, 0);
  }

  parseValue(value) {
    const cleaned = String(value || "").replace(/,/g, "");
    const number = parseFloat(cleaned);
    return Number.isFinite(number) ? number : 0;
  }

  updateDisplay(amount) {
    // Format for display with 2 decimal places
    this.finalDisplay.textContent = amount.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });

    // Store exact value in hidden input
    this.finalHidden.value = amount.toFixed(2);

    // Flash animation
    this.flashContainer();
  }

  flashContainer() {
    this.container.style.opacity = "0.5";
    setTimeout(() => {
      this.container.style.opacity = "1";
    }, 50);
  }
}

// ============================================================================
// TICKET FORMSET MANAGER
// Manages dynamic ticket rows (add/remove) for Django formsets
// ============================================================================

class TicketFormsetManager {
  constructor(calculator) {
    this.calculator = calculator;

    // Maximum allowed rows
    this.MAX_ROWS = 10;

    // Container and buttons
    this.container = document.querySelector("#ticket-container");
    this.addButton = document.getElementById("add-ticket-btn");
    this.removeButton = document.getElementById("remove-ticket-btn");
    this.template = document.getElementById("ticket-row-template");

    // Django formset management field
    this.form = this.container?.closest("form");
    this.totalFormsInput = this.form?.querySelector(
      'input[name$="-TOTAL_FORMS"]'
    );

    this.init();
  }

  init() {
    if (!this.container) return;

    // Bind events to existing rows
    this.getVisibleRows().forEach((row) => this.bindRowEvents(row));

    // Setup add/remove buttons
    this.addButton?.addEventListener("click", () => this.addTicketRow());
    this.removeButton?.addEventListener("click", () => this.removeLastTicket());

    // Check max rows on init
    this.updateAddButtonState();
  }

  // Get/Set Django formset TOTAL_FORMS count
  getTotalForms() {
    return this.totalFormsInput ? parseInt(this.totalFormsInput.value, 10) : 0;
  }

  setTotalForms(count) {
    if (this.totalFormsInput) {
      this.totalFormsInput.value = String(count);
    }
  }

  getVisibleRows() {
    return Array.from(this.container.children).filter(
      (row) => row.style.display !== "none"
    );
  }

  // Add event listeners to a ticket row
  bindRowEvents(row) {
    // Refund amount input - clean and recalculate
    const refundInput = row.querySelector(".refund-amount");
    if (refundInput) {
      refundInput.addEventListener("input", () => {
        // Only allow numbers, periods, and dashes
        refundInput.value = refundInput.value.replace(/[^0-9.\-]/g, "");
        this.calculator.calculate();
      });
    }

    // Fare input - clean only
    const fareInput = row.querySelector(".fare-input");
    if (fareInput) {
      fareInput.addEventListener("input", () => {
        fareInput.value = fareInput.value.replace(/[^0-9.\-]/g, "");
      });
    }

    // Remove button
    const removeButton = row.querySelector(".remove-ticket");
    if (removeButton) {
      removeButton.addEventListener("click", () => this.removeTicketRow(row));
    }
  }

  // Add a new ticket row
  addTicketRow() {
    if (!this.template) return null;

    const currentIndex = this.getTotalForms();

    // Check if max rows reached
    if (currentIndex >= this.MAX_ROWS) {
      alert(`Maximum ${this.MAX_ROWS} rows allowed`);
      return null;
    }

    // Replace Django's __prefix__ placeholder with actual index
    let html = this.template.innerHTML.replace(
      /__prefix__/g,
      String(currentIndex)
    );

    // Create row element
    const wrapper = document.createElement("div");
    wrapper.innerHTML = html.trim();
    const newRow = wrapper.firstElementChild;

    if (!newRow) return null;

    // Add to container and setup events
    this.container.appendChild(newRow);
    this.bindRowEvents(newRow);
    this.setTotalForms(currentIndex + 1);
    this.calculator.calculate();
    this.calculator.addEventListeners();
    this.updateAddButtonState();

    return newRow;
  }

  // Remove a specific ticket row
  removeTicketRow(row) {
    const deleteCheckbox = row.querySelector('input[name$="-DELETE"]');
    const idInput = row.querySelector('input[name$="-id"]');

    // If row has database ID, mark for deletion (soft delete)
    if (deleteCheckbox && idInput && idInput.value) {
      deleteCheckbox.checked = true;
      row.style.display = "none";
    } else {
      // Otherwise remove from DOM completely
      row.remove();
      this.reindexRows();
    }

    this.calculator.calculate();
    this.updateAddButtonState();
  }

  // Remove the last visible ticket row
  removeLastTicket() {
    const visibleRows = this.getVisibleRows();
    const lastRow = visibleRows[visibleRows.length - 1];

    if (lastRow) {
      this.removeTicketRow(lastRow);
    }
  }

  // Reindex all form fields after row removal
  reindexRows() {
    const visibleRows = this.getVisibleRows();

    visibleRows.forEach((row, index) => {
      row.setAttribute("data-form-index", index);

      // Update all form elements with new index
      row
        .querySelectorAll("input, select, textarea, label")
        .forEach((element) => {
          if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${index}-`);
          }
          if (element.id) {
            element.id = element.id.replace(/-\d+-/, `-${index}-`);
          }
          if (element.htmlFor) {
            element.htmlFor = element.htmlFor.replace(/-\d+-/, `-${index}-`);
          }
        });
    });

    this.setTotalForms(visibleRows.length);
  }

  // Update add button state based on max rows
  updateAddButtonState() {
    const visibleRows = this.getVisibleRows().length;
    if (this.addButton) {
      this.addButton.disabled = visibleRows >= this.MAX_ROWS;
    }
  }
}

// ============================================================================
// PURCHASE TYPE TOGGLE
// Shows/hides different purchase information sections
// ============================================================================

class PurchaseTypeToggle {
  constructor() {
    this.select = document.querySelector("#id_purchase_type");
    this.container = document.querySelector("#purchase-container");

    this.init();
  }

  init() {
    if (!this.select || !this.container) return;

    if (this.select.value) {
      this.toggle(this.select.value);
    }

    this.select.addEventListener("change", (e) => this.toggle(e.target.value));
  }

  toggle(selectedValue) {
    // Hide all sections
    console.log(selectedValue);

    selectedValue = selectedValue.trim();

    this.container.childNodes.forEach((node) => {
      if (node.hidden !== undefined) {
        node.hidden = true;
      }
    });

    // Show selected section
    const selectedSection = document.querySelector(`#${selectedValue}`);
    if (selectedSection) {
      selectedSection.hidden = false;
    }
  }
}

// ============================================================================
// INITIALIZE APPLICATION
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  const calculator = new RefundCalculator();
  const ticketManager = new TicketFormsetManager(calculator);
  const purchaseToggle = new PurchaseTypeToggle();
});
