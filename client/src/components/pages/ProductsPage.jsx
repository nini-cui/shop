import { Link } from "react-router-dom";
import ProductList from "../products/ProductList";
import "./ProductPage.css";

function ProductPage() {
  return (
    <div>
      <div className="create-product-container">
        <Link to="/products/create" className="create-product-btn">
          Create Product
        </Link>
      </div>
      <ProductList />
    </div>
  );
}

export default ProductPage;
