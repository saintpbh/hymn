
import React, { useState } from 'react';
import './HymnViewer.css';
import { ChevronLeft, ChevronRight, Menu } from 'lucide-react';

const HymnViewer = ({ hymnNumber, onNext, onPrev, onToggleSidebar, hymnsData }) => {
    const [status, setStatus] = useState('loading'); // loading, loaded, error

    const hymn = hymnsData.find(h => h.number === hymnNumber);
    const title = hymn ? hymn.title : `Hymn ${hymnNumber}`;
    const imagePath = hymn ? hymn.imagePath : `/hymns/${hymnNumber}.jpg`;

    const handleImageLoad = () => setStatus('loaded');
    const handleImageError = () => setStatus('error');

    // Reset status when hymnNumber changes is handled by the key prop on the img or wrapper


    return (
        <div className="hymn-viewer">
            <header className="viewer-header">
                <div className="header-left">
                    <button className="nav-btn" onClick={onPrev}>
                        <ChevronLeft size={24} />
                    </button>
                    <div className="hymn-info">
                        <h1>{hymnNumber}장</h1>
                        <span className="hymn-title">{title}</span>
                    </div>
                    <button className="nav-btn" onClick={onNext}>
                        <ChevronRight size={24} />
                    </button>
                </div>

                <button className="menu-btn" onClick={onToggleSidebar}>
                    <Menu size={24} />
                </button>
            </header>

            <div className="viewer-content">
                {status === 'loading' && <div className="loading-spinner">Loading...</div>}
                {status === 'error' && <div className="error-msg">Hymn not found</div>}

                <img
                    key={hymnNumber}
                    src={imagePath}
                    alt={`Hymn ${hymnNumber}`}
                    className={`hymn-image ${status === 'loading' ? 'hidden' : ''}`}
                    onLoad={handleImageLoad}
                    onError={handleImageError}
                />
            </div>
        </div>
    );
};

export default HymnViewer;
