import { useEffect, useState } from "react";
import "./ProductList.css";
import { useAuth } from "react-oidc-context";

function ProductCard({ product }) {
  const [imageIndex, setImageIndex] = useState(0);

  const images = product.images || [];

  function nextImage() {
    setImageIndex((current) => (current + 1) % images.length);
  }

  function previousImage() {
    setImageIndex((current) => (current - 1 + images.length) % images.length);
  }

  return (
    <div className="product-card">
      <div className="product-image-container">
        {images.length > 0 ? (
          <>
            <img
              src={images[imageIndex].image_url}
              alt={product.name}
              className="product-image"
            />

            {images.length > 1 && (
              <>
                <button
                  className="image-nav previous-image"
                  onClick={previousImage}
                >
                  &#10094;
                </button>

                <button className="image-nav next-image" onClick={nextImage}>
                  &#10095;
                </button>

                <span className="image-counter">
                  {imageIndex + 1} / {images.length}
                </span>
              </>
            )}
          </>
        ) : (
          <div className="no-product-image">No image available</div>
        )}
      </div>

      <div className="product-info">
        <h3>{product.name}</h3>
        <p className="product-price">${Number(product.price).toFixed(2)}</p>
        <p>Stock: {product.stock_quantity}</p>
      </div>
    </div>
  );
}

function ProductList() {
  const auth = useAuth();

  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const pageSize = 8;

  useEffect(() => {
    const token = auth.user?.access_token;
    console.log("Access Token:", token);

    if (!token) {
        return;
    }

    async function fetchProducts() {
      try {
        const resp = await fetch(
          `http://localhost:8000/products/?page=${page}&page_size=${pageSize}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (!resp.ok) {
          throw new Error(`HTTP error: ${resp.status}`);
        }

        const data = await resp.json();

        setProducts(data.products);
        setHasNext(data.next);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    }

    fetchProducts();
  }, [page, auth.user?.access_token]);

  return (
    <div className="product-list-container">
      <div className="product-grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>

      <div className="pagination">
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>
          Previous
        </button>

        <span>Page {page}</span>

        <button disabled={!hasNext} onClick={() => setPage(page + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}

export default ProductList;
