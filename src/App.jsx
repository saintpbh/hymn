
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import HymnList from './components/HymnList';
import HymnViewer from './components/HymnViewer';
import hymnsDataRaw from './data/hymns.json'; // This might be empty initially
import './App.css';

// Fallback if empty (e.g. before scrape finishes)
const hymnsData = Array.isArray(hymnsDataRaw) && hymnsDataRaw.length > 0 ? hymnsDataRaw : [];

function App() {
  const [currentHymn, setCurrentHymn] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const data = hymnsData;

  // Poll for data updates purely for dev experience (optional)
  // In prod, this would be static.
  // We'll rely on HMR or reload.

  const handleSelectHymn = (number) => {
    setCurrentHymn(number);
    setIsSidebarOpen(false); // Close sidebar on selection if on mobile (handled in Sidebar, but dual safeguard)
  };

  const handleNext = () => {
    if (currentHymn < 645) handleSelectHymn(currentHymn + 1);
  };

  const handlePrev = () => {
    if (currentHymn > 1) handleSelectHymn(currentHymn - 1);
  };

  return (
    <div className="app-container">
      {currentHymn ? (
        <HymnViewer
          hymnNumber={currentHymn}
          onNext={handleNext}
          onPrev={handlePrev}
          onToggleSidebar={() => setIsSidebarOpen(true)}
          hymnsData={data}
          onClose={() => setCurrentHymn(null)} /* Not used yet but good API */
        />
      ) : (
        <>
          <HymnList
            hymnsData={data}
            onSelectHymn={handleSelectHymn}
            onToggleSidebar={() => setIsSidebarOpen(true)}
          />
        </>
      )}

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onSelectHymn={handleSelectHymn}
        currentHymnNumber={currentHymn}
      />
    </div>
  );
}

export default App;
