import { Link } from "react-router-dom";
import ProductList from "../products/ProductList";
import useCurrentUser from "../common/hook/useCurrentUser";
import "./ProductPage.css";

function ProductPage() {
  const currentUser = useCurrentUser();

  const canCreateProduct =
    currentUser?.roles?.includes("seller") ||
    currentUser?.roles?.includes("admin");

  return (
    <div>
      {canCreateProduct && (
        <div className="create-product-container">
          <Link to="/products/create" className="create-product-btn">
            Create Product
          </Link>
        </div>
      )}

      <ProductList />
    </div>
  );
}

export default ProductPage;
