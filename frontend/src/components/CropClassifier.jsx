import React, { useState } from 'react';
import axios from 'axios';

function CropClassifier() {
    const [crop, setCrop] = useState('');
    const [file, setFile] = useState(null);
    const [prediction, setPrediction] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleCropChange = (e) => {
        setCrop(e.target.value);
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleClassify = async () => {
        if (!crop || !file) {
            setError('Please select a crop and upload an image');
            return;
        }

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('crop', crop);
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5000/classify_crop', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setPrediction(response.data.prediction);
        } catch (error) {
            console.error('Error classifying the crop:', error);
            setError('Error classifying the crop');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div id="crop-classifier" className="container mx-auto p-4">
            <h2 className="text-2xl mb-4" style={{ color: '#597445' }}>Know Who Attacked Your Crop</h2>
            <div className="p-4 border rounded shadow-lg" style={{ backgroundColor: '#E7F0DC' }}>
                <div className="mb-4">
                    <label className="block mb-2">Select Crop</label>
                    <select value={crop} onChange={handleCropChange} className="w-full p-2 border rounded">
                        <option value="">Select Crop</option>
                        <option value="banana">Banana</option>
                        <option value="wheat">Wheat</option>
                        <option value="cotton">Cotton</option>
                        <option value="watermelon">Watermelon</option>
                    </select>
                </div>
                <div className="mb-4">
                    <label className="block mb-2">Upload Image</label>
                    <input type="file" onChange={handleFileChange} className="w-full p-2 border rounded" />
                </div>
                <button
                    onClick={handleClassify}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                    disabled={loading}
                >
                    {loading ? <span className="animate-spin">🔄</span> : 'Classify'}
                </button>
                {error && (
                    <div className="mt-4 text-red-500">
                        <p>{error}</p>
                    </div>
                )}
                {prediction && (
                    <div className="mt-4">
                        <h3 className="text-xl" style={{ color: '#658147' }}>Prediction</h3>
                        <p>{prediction}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default CropClassifier;
