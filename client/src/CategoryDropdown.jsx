import { useState, useEffect } from "react";

function CategoryDropdown() {
    const listCategoryEndpoint = "http://localhost:8000/categories/"
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState("");

    async function listCategories() {
        const resp = await fetch(listCategoryEndpoint);

        if (!resp.ok) {
            throw new Error("Failed to fetch categories");
        }

        const categories = await resp.json();
        setCategories(categories)
    }

    useEffect(() => {
        listCategories().catch(console.error);
    }, [])

    
    return (
        <div>
            <select
                value={selectedCategory}
                onChange={(event) => 
                    setSelectedCategory(event.target.value)
                }
            >
                <option value="">Select a category</option>

                {
                    categories.map((category) => (
                        <option key={category.id} value={category.id}>
                            {category.name}
                        </option>
                    ))
                }

            </select>
            
        </div>
    )
}

export default CategoryDropdown;