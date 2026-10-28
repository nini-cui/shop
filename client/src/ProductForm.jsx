import { useState } from "react";
import ImageUpload from "./ImageUpload";
import CategoryDropdown from "./CategoryDropdown";

function ProductForm() {
    const [productName, setProductName] = useState("");
    const [productDescription, setProductDescription] = useState("");
    const [productPrice, setProductPrice] = useState("");
    const [productStockQuantity, setProductStockQuantity] = useState("");

    return (
        <form>
            <div>
                <label>Product Name</label>
                <input 
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
                    onChange={(event) => setStockQuantity(event.target.value)}
                />
            </div>

            <CategoryDropdown/>
            <ImageUpload/>

            <button type="submit">Create Product</button>
        </form>
    );
}

export default ProductForm;