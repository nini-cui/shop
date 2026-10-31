import { useState, useEffect } from "react";

function CategoryDropdown({ selectedCategories, setSelectedCategories }) {
  const listCategoryEndpoint = "http://localhost:8000/categories/";
  const [categories, setCategories] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  async function listCategories() {
    const resp = await fetch(listCategoryEndpoint);

    if (!resp.ok) {
      throw new Error("Failed to fetch categories");
    }

    const data = await resp.json();
    setCategories(data);
  }

  useEffect(() => {
    listCategories().catch(console.error);
  }, []);

  const selectedCategoryNames = categories
    .filter((category) => selectedCategories.includes(category.id))
    .map((category) => category.name);

  return (
    <div className="form-group">
      <lable>Categories</lable>

      <button
        type="button"
        className="category-dropdown-button"
        onClick={(event) => setIsOpen(!isOpen)}
      >
        <span>
          {selectedCategoryNames.length > 0
            ? selectedCategoryNames.join(", ")
            : "Select Categories"}
        </span>
      </button>

      {isOpen && (
        <div>
          {categories.map((category) => (
            <label key={category.id}>
              <input
                type="checkbox"
                checked={selectedCategories.includes(category.id)}
                onChange={(event) => {
                  if (event.target.checked) {
                    setSelectedCategories([...selectedCategories, category.id]);
                  } else {
                    setSelectedCategories(
                      selectedCategories.filter((id) => id !== category.id),
                    );
                  }
                }}
              />
              {category.name}
            </label>
          ))}
        </div>
      )}
    </div>
  );
}

export default CategoryDropdown;
