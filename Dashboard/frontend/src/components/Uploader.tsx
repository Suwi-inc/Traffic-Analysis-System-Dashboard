import axios from "axios";
import { useDropzone } from "react-dropzone";
import { messageAtom, isUploadedAtom } from "../atoms";
import { useAtom, useSetAtom } from "jotai";

interface UploadResponse {
  filename: string;
  temp_path: string;
}

const Uploader = () => {
  const [message, setMessage] = useAtom(messageAtom);
  const setIsUploaded = useSetAtom(isUploadedAtom);

  const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL;

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (acceptedFiles.length === 0) {
      setMessage("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", acceptedFiles[0]);

    try {
      setMessage("Uploading...");
      const resp = await axios.post<UploadResponse>(
        `${API_BASE_URL}/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (resp.status === 200) {
        setIsUploaded(true);
      } else {
        throw new Error("Error uploading video");
      }
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
    return <li key={file.path}>{file.name}</li>;
  });

  return (
    <form onSubmit={handleUpload} className="flex flex-col gap-4 w-full">
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
      <button className="px-4 py-2 mx-1.5 w-sm self-center font-semibold bg-green-600 text-white border-none rounded-sm cursor-pointer hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
        Upload Video
      </button>
      {message && <p className="text-center">{message}</p>}
    </form>
  );
};

export default Uploader;
