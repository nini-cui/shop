# create categories
curl -X POST http://localhost:8000/categories/ -H "Content-Type: application/json" -d '{"name": "test", "slug": "test"}'

# create products
curl -X POST http://localhost:8000/products/ -H "Content-Type: application/json" -d '{"name": "Floppy Bunny Keychain", "slug": "floppy-bunny-keychain", "description": "Meet your new adorable companion! The Floppy Bunny Keychain features a soft, floppy-eared bunny design that adds a touch of cuteness to your everyday essentials. Perfect for decorating your keys, handbag, backpack, or purse, it also makes a lovely little gift for bunny lovers and anyone who adores cute accessories.", "price": 30.0, "stock_quantity": 1, "category_ids": [1, 2, 3]}'

# list products by category
curl -X GET http://localhost:8000/products/?category_id=3

# create buckets
curl -X POST http://localhost:8000/storage/bucket

# upload images
curl -X POST http://localhost:8000/storage/images -F "file=@images/bunny.png" -F "bucket_name=keyring-product-images"