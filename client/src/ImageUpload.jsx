import { useState } from "react";

function ImageUpload({ imageKeys, setImageKeys }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const imageUploadEndpoint = "http://localhost:8000/storage/images";
  const uploadMethod = "POST";
  const uploadBucketName = import.meta.env.VITE_UPLOAD_BUCKET_NAME;

  async function handleImageUpload() {
    if (!file) {
      setMessage("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("bucket_name", uploadBucketName);

    // upload images to S3
    try {
      const resp = await fetch(imageUploadEndpoint, {
        method: uploadMethod,
        body: formData,
      });

      if (!resp.ok) {
        throw new Error("Upload failed");
      }

      const data = await resp.json();
      setMessage(`Upload successful! Image key: ${data.image_key}`);
      setImageKeys((prevKeys) => [...prevKeys, data.image_key]);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  }

  return (
    <div className="image-upload-container">
      <label className="product-label">Product Images</label>

      <div className="image-upload-area">
        <label className="upload-action-button choose-file-button">
            Choose File
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={(event) => setFile(event.target.files[0] || null)}
          />
        </label>

        {file && <p className="selected-file">{file.name}</p>}

        <button
          type="button"
          className="upload-action-button image-upload-button"
          onClick={handleImageUpload}
          disabled={!file}
        >
          Upload Image
        </button>
      </div>
    </div>
  );
}

export default ImageUpload;
