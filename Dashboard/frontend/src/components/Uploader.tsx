import axios from "axios";
import { useDropzone } from "react-dropzone";

interface Props {
  selectedFile: File | null;
  setSelectedFile: React.Dispatch<React.SetStateAction<File | null>>;
  message: string;
  setMessage: React.Dispatch<React.SetStateAction<string>>;
}

const Uploader = ({
  selectedFile,
  setSelectedFile,
  message,
  setMessage,
}: Props) => {
  const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL;

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setMessage("Uploading...");
      await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage("Video uploaded successfully!");
    } catch (error) {
      setMessage("Error uploading video");
      console.error("Error:", error);
    }
  };

  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    maxFiles: 1,
    accept: {
      "video/*": [],
    },
  });

  const acceptedFileItems = acceptedFiles.map((file) => {
    setSelectedFile(file);
    return <li key={file.path}>{file.name}</li>;
  });

  return (
    <>
      <section>
        <div
          {...getRootProps({
            className: "p-16 bg-gray-100 rounded-md shadow-md dropzone",
          })}
        >
          <input {...getInputProps()} />
          <p className="text-center">
            Drop a video file here, or click to select file
          </p>
        </div>
        {acceptedFileItems.length !== 0 && (
          <aside className="text-center">
            <h4 className="font-semibold">Accepted files</h4>
            <ul>{acceptedFileItems}</ul>
          </aside>
        )}
      </section>
      <button
        className="px-4 py-2 mx-1.5 w-sm self-center font-semibold bg-green-600 text-white border-none rounded-sm cursor-pointer hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
        onClick={handleUpload}
      >
        Upload Video
      </button>
      {message && <p className="text-center">{message}</p>}
    </>
  );
};

export default Uploader;
