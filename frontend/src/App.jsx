import UploadForm from './components/UploadForm';
import GetResponse from "./components/GetResponse";

function App() {
  return (
    <div className="min-h-screen bg-white flex flex-col justify-between">
      {/* Header */}
      <UploadForm />

      {/* Spacer to allow scrolling if needed */}
      <div className="flex-1" />

      {/* Question Input */}
      <GetResponse />
    </div>
  );
}

export default App;
