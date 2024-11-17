import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { DocumentIcon, VideoCameraIcon, PhotographIcon } from '@heroicons/react/outline';

const FileDrop = () => {
  const [files, setFiles] = useState([]);

  const onDrop = (acceptedFiles) => {
    setFiles((prevFiles) => [
      ...prevFiles,
      ...acceptedFiles.map((file) => ({
        name: file.name,
        type: file.type,
        preview: URL.createObjectURL(file),
      })),
    ]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif'],
      'video/*': ['.mp4', '.mov', '.avi'],
      'application/pdf': ['.pdf'],
    },
  });

  const renderFileIcon = (type) => {
    if (type.startsWith('image')) return <PhotographIcon className="w-10 h-10 text-blue-500" />;
    if (type.startsWith('video')) return <VideoCameraIcon className="w-10 h-10 text-green-500" />;
    if (type === 'application/pdf') return <DocumentIcon className="w-10 h-10 text-red-500" />;
    return <DocumentIcon className="w-10 h-10 text-gray-500" />;
  };

  return (
    <div className="flex flex-col items-center">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-5 cursor-pointer transition ${
          isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-blue-500">Drop the files here...</p>
        ) : (
          <p className="text-gray-500">Drag & drop some files here, or click to select files</p>
        )}
      </div>
      <div className="mt-5 grid grid-cols-3 gap-4 w-full">
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center space-x-3 p-2 border rounded-lg shadow-sm bg-white"
          >
            {renderFileIcon(file.type)}
            <div>
              <p className="text-sm font-medium">{file.name}</p>
              <p className="text-xs text-gray-400">{file.type}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileDrop;