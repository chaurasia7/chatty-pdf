import { use, useState } from "react";

function UploadForm() {
  const [files, setFiles] = useState(null);


  const handleSubmit = async (event) => {

    event.preventDefault();

    const  filesUploaded = [...event.target.files]

    if (!filesUploaded || filesUploaded.length === 0) {
      console.error("No files selected");
      return;
    }


    const formData = new FormData();
    filesUploaded.forEach((file) => {
      formData.append("upload_file", file);
    });

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        console.log("File uploaded successfully");
      } else {
        console.error("File upload failed");
      }
    } catch (error) {
      console.error("There was an error", error);
    }
  };

  return (
    <div className="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-6 py-4 bg-white shadow">

      {/* Logo */}
      <div className="flex items-center space-x-2">
        <div className="bg-green-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center text-sm">
          ai
        </div>
        <div className="text-lg font-semibold text-gray-800">
          planet
          <span className="block text-xs text-green-500 font-normal">formerly DPH</span>
        </div>
      </div>

      {/* Upload Button */}
      <form  className="flex items-center space-x-2">
        <label className="cursor-pointer inline-flex items-center px-4 py-2 bg-white text-sm font-medium text-gray-800 border border-gray-300 rounded hover:bg-gray-100 transition duration-200">
          <input
            type="file"
            multiple
            accept=".pdf"
            onChange={handleSubmit}
            className="hidden"
          />
          📄 Upload PDF
        </label>
      </form>
    </div>
  );
}

export default UploadForm;
