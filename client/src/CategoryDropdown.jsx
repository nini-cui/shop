import { useState, useEffect } from "react";

function CategoryDropdown({ selectedCategories, setSelectedCategories }) {
    const listCategoryEndpoint = "http://localhost:8000/categories/"
    const [categories, setCategories] = useState([]);

    async function listCategories() {
        const resp = await fetch(listCategoryEndpoint);

        if (!resp.ok) {
            throw new Error("Failed to fetch categories");
        }

        const data = await resp.json();
        setCategories(data)
    }

    useEffect(() => {
        listCategories().catch(console.error);
    }, [])

    
    return (
        <div>
            <p>Categories</p>

            {categories.map((category) => (
                <label key={category.id}>
                    <input
                        type="checkbox"
                        checked={selectedCategories.includes(category.id)}
                        onChange={(event) => {
                            if (event.target.checked) {
                                setSelectedCategories([
                                    ...selectedCategories,
                                    category.id,
                                ]);
                            } else {
                                setSelectedCategories(
                                    selectedCategories.filter(
                                        (id) => id !== category.id
                                    )
                                );
                            }
                        }}
                    />
                    {category.name}
                </label>
            ))}
        </div>
    )
}

export default CategoryDropdown;