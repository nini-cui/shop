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
                        className="form-input"
                        placeholder="Enter Product Name"
                        value={productName}
                        onChange={(event) => setProductName(event.target.value)}
                    />
                </div>

                <div>
                    <label>Product Description</label>
                    <textarea 
                        value={productDescription}
                        onChange={(event) => setProductDescription(event.target.value)}
                    />
                </div>

                <div>
                    <label>Product Price</label>
                    <input
                        type="number"
                        step="0.01"
                        value={productPrice}
                        onChange={(event) => setProductPrice(event.target.value)}
                    />
                </div>

                <div>
                    <label>Stock Quantity</label>
                    <input
                        type="number"
                        value={productStockQuantity}
                        onChange={(event) => setProductStockQuantity(event.target.value)}
                    />
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