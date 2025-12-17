// ======================================
// SHARED CART SYSTEM
// Works across home.html and user.html
// ======================================

class CartManager {
    constructor() {
        this.storageKey = 'coffee_shop_cart';
    }

    // Get cart from sessionStorage
    getCart() {
        const cartData = sessionStorage.getItem(this.storageKey);
        return cartData ? JSON.parse(cartData) : [];
    }

    // Save cart to sessionStorage
    saveCart(cart) {
        sessionStorage.setItem(this.storageKey, JSON.stringify(cart));
        this.notifyCartUpdate();
    }

    // Add item to cart
    addItem(product) {
		let cart = this.getCart();
		const existingItem = cart.find(item => item.id === product.id);

		if (existingItem) {
			existingItem.quantity += 1;
		} else {
			cart.push({
				id: product.id,
				name: product.name,
				price: product.price,
				image: product.image || null,
				quantity: 1
			});
		}

		this.saveCart(cart);
		return cart;
	}

    // Update item quantity
    updateQuantity(productId, change) {
        let cart = this.getCart();
        const item = cart.find(i => i.id === productId);

        if (item) {
            item.quantity += change;
            if (item.quantity <= 0) {
                cart = cart.filter(i => i.id !== productId);
            }
        }

        this.saveCart(cart);
        return cart;
    }

    // Remove item from cart
    removeItem(productId) {
        let cart = this.getCart();
        cart = cart.filter(i => i.id !== productId);
        this.saveCart(cart);
        return cart;
    }

    // Clear entire cart
    clearCart() {
        sessionStorage.removeItem(this.storageKey);
        this.notifyCartUpdate();
    }

    // Get cart total
    getTotal() {
        const cart = this.getCart();
        return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    // Get total items count
    getItemCount() {
        const cart = this.getCart();
        return cart.reduce((sum, item) => sum + item.quantity, 0);
    }

    // Notify other pages of cart updates
    notifyCartUpdate() {
        // Dispatch custom event
        window.dispatchEvent(new Event('cartUpdated'));
    }
}

// Create global cart manager instance
window.cartManager = new CartManager();

console.log('✅ Shared cart system loaded');