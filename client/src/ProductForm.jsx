import { useState } from "react";
import ImageUpload from "./ImageUpload";
import CategoryDropdown from "./CategoryDropdown";
import "./ProductForm.css"

function ProductForm() {
    const [productName, setProductName] = useState("");
    const [productDescription, setProductDescription] = useState("");
    const [productPrice, setProductPrice] = useState("");
    const [productStockQuantity, setProductStockQuantity] = useState("");
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [imageKeys, setImageKeys] = useState([]);

    const createProductEndpoint = "http://localhost:8000/products/"

    async function handleSubmit(event) {
        event.preventDefault();

        const productData = {
            name: productName,
            description: productDescription,
            price: Number(productPrice),
            stock_quantity: Number(productStockQuantity),
            category_ids: selectedCategories,
            image_keys: imageKeys
        }

        try {
            const resp = await fetch(createProductEndpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(productData)
            });

            const data = await resp.json();

            if (!resp.ok) {
                console.error("API error:", data);
                throw new Error(JSON.stringify(data.detail));
            }

            console.log("Product created successfully:", data);
        } catch (error) {
            console.error("Error creating product:", error);
        }
    }

    return (
        <div className="product-form-container">
            <h2>Create Product</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="productName">Product Name</label>
                    <input 
                        id="productName"
                        type="text"
                        className="form-input product-name-input"
                        placeholder="Enter Product Name"
                        value={productName}
                        onChange={(event) => setProductName(event.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="productDescription">Product Description</label>
                    <textarea 
                        id="productDescription"
                        className="form-input form-textarea"
                        placeholder="Enter Product Description"
                        value={productDescription}
                        onChange={(event) => setProductDescription(event.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="productPrice">Product Price</label>

                    <div>
                        <span className="currency-symbol">$</span>
                        <input
                            id="productPrice"
                            type="number"
                            step="1.0"
                            min="0"
                            className="form-input number-input price-input"
                            placeholder="0.00"
                            value={productPrice}
                            onChange={(event) => setProductPrice(event.target.value)}
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="productStockQuantity">Stock Quantity</label>

                     <div>
                        <input
                            id="productStockQuantity"
                            type="number"
                            min="0"
                            step="1"
                            className="form-input number-input stock-quantity-input"
                            placeholder="1"
                            value={productStockQuantity}
                            onChange={(event) => setProductStockQuantity(event.target.value)}
                        />
                    </div>
                </div>

                <CategoryDropdown
                    selectedCategories={selectedCategories}
                    setSelectedCategories={setSelectedCategories}
                />
                
                <ImageUpload
                    imageKeys={imageKeys}
                    setImageKeys={setImageKeys}
                />

                <button type="submit">Create Product</button>
            </form>
         </div>
    );
}

export default ProductForm;