
import React, { useState } from 'react';
import './HymnViewer.css';
import { ChevronLeft, ChevronRight, Menu } from 'lucide-react';

const HymnViewer = ({ hymnNumber, onNext, onPrev, onToggleSidebar, hymnsData, onClose }) => {
    const [status, setStatus] = useState('loading'); // loading, loaded, error

    const hymn = hymnsData.find(h => h.number === hymnNumber);
    const imagePath = hymn ? hymn.imagePath : `/hymns/${hymnNumber}.jpg`;

    const handleLoad = () => setStatus('loaded');
    const handleError = () => setStatus('error');

    // Reset status when hymnNumber changes is handled by the key prop on the img or wrapper


    return (
        <div className="hymn-viewer-container">
            {/* Glass Header */}
            <header className="viewer-header">
                <button onClick={onClose} className="nav-icon-btn" aria-label="Back">
                    <ChevronLeft size={24} />
                </button>
                <div className="hymn-indicator">
                    <span className="number">{hymnNumber}장</span>
                    <span className="label">Hymn {hymnNumber}</span>
                </div>
                <button onClick={onToggleSidebar} className="nav-icon-btn" aria-label="Menu">
                    <Menu size={24} />
                </button>
            </header>

            {/* Main Content */}
            <div className="viewer-content">
                {status === 'loading' && <div className="loading-spinner">Loading Hymn...</div>}
                {status === 'error' && <div className="error-msg">Hymn not found</div>}

                <img
                    key={hymnNumber}
                    src={imagePath}
                    alt={`Hymn ${hymnNumber}`}
                    className="hymn-image"
                    onLoad={handleLoad}
                    onError={handleError}
                    style={{ display: status === 'loaded' ? 'block' : 'none' }}
                />
            </div>

            {/* Floating Navigation (Bottom) */}
            <div className="floating-nav">
                <button onClick={onPrev} disabled={hymnNumber <= 1} className="float-btn">
                    <ChevronLeft size={28} />
                </button>
                <button onClick={onNext} disabled={hymnNumber >= 645} className="float-btn">
                    <ChevronRight size={28} />
                </button>
            </div>
        </div>
    );
};

export default HymnViewer;
