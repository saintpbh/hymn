
import React, { useState } from 'react';
import './HymnViewer.css';
import { ChevronLeft, ChevronRight, Menu } from 'lucide-react';

const HymnViewer = ({ hymnNumber, onNext, onPrev, onToggleSidebar, hymnsData, onClose }) => {
    const [status, setStatus] = useState('loading'); // loading, loaded, error

    const hymn = hymnsData.find(h => h.number === hymnNumber);
    const rawPath = hymn ? hymn.imagePath : `/hymns/${hymnNumber}.jpg`;
    // Resolve base URL for subdirectory deployment
    const imagePath = `${import.meta.env.BASE_URL}${rawPath.startsWith('/') ? rawPath.slice(1) : rawPath}`;

    const handleLoad = () => setStatus('loaded');
    const handleError = () => setStatus('error');

    // Reset status when hymnNumber changes is handled by the key prop on the img or wrapper


    // Helper to resolve image path with base URL
    const getImagePath = (path) => {
        if (!path) return '';
        // If path starts with /, remove it to append to base (which usually ends with /)
        const smoothPath = path.startsWith('/') ? path.slice(1) : path;
        return `${import.meta.env.BASE_URL}${smoothPath}`;
    };

    return (
        <div className={`hymn-viewer ${isMenuOpen ? 'menu-open' : ''}`} onClick={handleTap}>
            <header className={`viewer-header ${showHeader ? 'visible' : 'hidden'}`}>
                <button className="back-btn" onClick={(e) => { e.stopPropagation(); onClose(); }}>
                    <ChevronLeft size={24} />
                </button>
                <h2 className="header-title">
                    <span className="hymn-number">No. {hymn.number}</span>
                    <span className="hymn-title-text">{hymn.title}</span>
                </h2>
                <button className="menu-btn" onClick={(e) => { e.stopPropagation(); onToggleSidebar(); }}>
                    <Menu size={24} />
                </button>
            </header>

            <div className="hymn-content">
                {loading && <div className="loading-spinner">Loading...</div>}
                {error && <div className="error-message">Hymn not found</div>}
                <img
                    src={getImagePath(hymn.imagePath)}
                    alt={hymn.title}
                    className={`hymn-image ${loading ? 'hidden' : ''}`}
                    onLoad={handleLoad}
                    onError={handleError}
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
