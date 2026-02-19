import { useState } from 'react';
import { Upload, ArrowLeft, Loader2, Leaf, AlertTriangle, CheckCircle, AlertCircle } from 'lucide-react';

export default function PlantDiseaseClassifier() {
  const [currentPage, setCurrentPage] = useState('upload');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setUploadedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async () => {
    if (!uploadedImage) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', uploadedImage);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setResults(data);
      setCurrentPage('results');
    } catch (err) {
      setError('Failed to analyze image. Make sure the backend server is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToHome = () => {
    setCurrentPage('upload');
    setUploadedImage(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
  };

  const getSeverityColor = (severity) => {
    if (severity?.toLowerCase().includes('high')) {
      return 'bg-red-100 text-red-800 border-red-300';
    } else if (severity?.toLowerCase().includes('moderate')) {
      return 'bg-orange-100 text-orange-800 border-orange-300';
    } else if (severity?.toLowerCase().includes('low')) {
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    }
    return 'bg-green-100 text-green-800 border-green-300';
  };

  const getSeverityIcon = (severity) => {
    if (severity?.toLowerCase().includes('high')) {
      return <AlertTriangle className="w-5 h-5 text-red-600" />;
    } else if (severity?.toLowerCase().includes('moderate')) {
      return <AlertCircle className="w-5 h-5 text-orange-600" />;
    } else if (severity?.toLowerCase().includes('low')) {
      return <AlertCircle className="w-5 h-5 text-yellow-600" />;
    }
    return <CheckCircle className="w-5 h-5 text-green-600" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {currentPage === 'upload' ? (
        <div className="container mx-auto px-4 py-12 max-w-2xl">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Leaf className="w-8 h-8 text-green-600" />
              <h1 className="text-4xl font-bold text-green-800">Plant Disease Classifier</h1>
            </div>
            <p className="text-lg text-green-700">Upload a photo of your plant to identify potential diseases</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              className="border-2 border-dashed border-green-300 rounded-lg p-12 text-center hover:border-green-500 transition-colors cursor-pointer bg-white"
            >
              <input
                type="file"
                id="file-upload"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />
              <label htmlFor="file-upload" className="cursor-pointer block">
                {imagePreview ? (
                  <div className="space-y-4">
                    <img
                      src={imagePreview}
                      alt="Plant preview"
                      className="max-h-64 mx-auto rounded-lg object-contain"
                    />
                    <p className="text-green-600 text-sm">Click or drag to change image</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="w-16 h-16 mx-auto text-green-400" />
                    <div>
                      <p className="text-lg text-green-700 mb-2">
                        Drop your plant image here or click to browse
                      </p>
                      <p className="text-sm text-green-600">
                        Supports: JPG, PNG, JPEG
                      </p>
                    </div>
                  </div>
                )}
              </label>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-center">{error}</p>
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={!uploadedImage || loading}
              className="w-full mt-6 px-6 py-3 text-lg font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                'Analyze Plant'
              )}
            </button>
          </div>

          <div className="mt-6 bg-green-50 border border-green-200 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-green-800 mb-3">📸 How to Take the Perfect Photo</h2>
            <ul className="space-y-2 text-green-700">
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Good lighting:</strong> Take photos in natural daylight for best results</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Clear focus:</strong> Ensure the affected area is in sharp focus</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Close-up:</strong> Get close enough to show disease symptoms clearly</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Show the whole leaf:</strong> Include both healthy and affected parts if possible</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Avoid shadows:</strong> Make sure the plant is evenly lit without harsh shadows</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span><strong>Clean background:</strong> A plain background helps the classifier focus on the plant</span>
              </li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="container mx-auto px-4 py-12 max-w-6xl">
          <button
            onClick={handleBackToHome}
            className="mb-6 px-4 py-2 text-green-700 hover:text-green-800 hover:bg-green-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Analyze Another Plant
          </button>

          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Leaf className="w-8 h-8 text-green-600" />
              <h1 className="text-4xl font-bold text-green-800">Analysis Results</h1>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-green-800 mb-4">Uploaded Image</h2>
              <img
                src={imagePreview}
                alt="Analyzed plant"
                className="w-full rounded-lg object-contain max-h-80"
              />
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-green-800 mb-4">Diagnosis</h2>
              
              {results && (
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-green-600 mb-1">Detected Disease</p>
                    <p className="text-lg font-medium text-green-900">{results.disease}</p>
                  </div>

                  <div>
                    <p className="text-sm text-green-600 mb-2">Severity Level</p>
                    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border ${getSeverityColor(results.severity)}`}>
                      {getSeverityIcon(results.severity)}
                      <span className="font-medium">{results.severity}</span>
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-green-600 mb-1">Confidence</p>
                    <div className="flex items-center gap-3">
                      <div className="flex-1 bg-green-200 rounded-full h-3 overflow-hidden">
                        <div
                          className="bg-green-600 h-full rounded-full transition-all"
                          style={{ width: `${results.confidence}%` }}
                        />
                      </div>
                      <span className="text-lg font-medium text-green-900">{results.confidence}%</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {results && results.isPlant && (
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h2 className="text-2xl font-semibold text-green-800 mb-3">Treatment Recommendations</h2>
              <p className="text-green-700 leading-relaxed">{results.treatment}</p>
            </div>
          )}

          {results && !results.isPlant && (
            <div className="bg-red-50 border border-red-200 rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-red-800 mb-3">⚠️ Not a Plant</h2>
              <p className="text-red-700">{results.treatment}</p>
            </div>
          )}

          <div className="bg-amber-50 border border-amber-200 rounded-lg shadow-lg p-6">
            <p className="text-amber-800">
              <strong>Note:</strong> This is an automated analysis and should not replace professional diagnosis. 
              For serious plant health concerns, please consult with a local agricultural extension office or plant pathologist.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}