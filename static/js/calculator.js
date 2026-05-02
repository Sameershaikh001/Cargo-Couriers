class RateCalculator {
    constructor() {
        this.baseRates = {
            standard: { base: 50, perKm: 2, perKg: 8 },
            express: { base: 80, perKm: 3, perKg: 10 },
            same_day: { base: 120, perKm: 5, perKg: 12 }
        };
        
        this.init();
    }
    
    init() {
        const form = document.getElementById('rateCalculatorForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleCalculate(e));
            this.addRealTimeUpdates();
        }
    }
    
    addRealTimeUpdates() {
        const inputs = ['weight', 'distance', 'service_type'];
        inputs.forEach(input => {
            const element = document.getElementById(input);
            if (element) {
                element.addEventListener('input', () => this.calculateRealTime());
            }
        });
    }
    
    calculateRealTime() {
        const weight = parseFloat(document.getElementById('weight')?.value) || 0;
        const distance = parseFloat(document.getElementById('distance')?.value) || 0;
        const serviceType = document.getElementById('service_type')?.value;
        
        if (weight > 0 && distance > 0 && serviceType) {
            const rate = this.calculateRate(weight, distance, serviceType);
            this.displayRate(rate);
        }
    }
    
    calculateRate(weight, distance, serviceType) {
        const rates = this.baseRates[serviceType] || this.baseRates.standard;
        return rates.base + (distance * rates.perKm) + (weight * rates.perKg);
    }
    
    displayRate(rate) {
        const resultElement = document.getElementById('rateResult');
        if (resultElement) {
            resultElement.innerHTML = `
                <div class="alert alert-info fade-in">
                    <h5>Estimated Rate: ₹${rate.toFixed(2)}</h5>
                    <small class="text-muted">This is an estimate. Final rate may vary based on actual weight and dimensions.</small>
                </div>
            `;
        }
    }
    
    handleCalculate(e) {
        e.preventDefault();
        this.calculateRealTime();
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RateCalculator();
});