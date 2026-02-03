
import React, { useState, useEffect, useRef, useCallback } from 'react';
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

    // Navigator Visibility Logic
    const [isNavVisible, setIsNavVisible] = useState(true);
    const timerRef = useRef(null);

    const resetTimer = useCallback(() => {
        if (timerRef.current) clearTimeout(timerRef.current);
        if (isNavVisible) {
            timerRef.current = setTimeout(() => {
                setIsNavVisible(false);
            }, 5000);
        }
    }, [isNavVisible]);

    useEffect(() => {
        resetTimer();
        return () => {
            if (timerRef.current) clearTimeout(timerRef.current);
        };
    }, [resetTimer]);

    const handleContainerClick = () => {
        setIsNavVisible(prev => !prev);
    };

    const handleNavAction = (e, action) => {
        if (e) e.stopPropagation();
        setIsNavVisible(true);
        // We need to manually trigger resetTimer logic because calling setIsNavVisible(true) 
        // won't trigger the effect if it's already true.
        if (timerRef.current) clearTimeout(timerRef.current);
        timerRef.current = setTimeout(() => {
            setIsNavVisible(false);
        }, 5000);

        if (action) action();
    };

    // Reset status when hymnNumber changes is handled by the key prop on the img or wrapper


    return (
        <div className="hymn-viewer-container" onClick={handleContainerClick}>
            <header className="viewer-header">
                <button className="back-btn" onClick={(e) => { e.stopPropagation(); onClose(); }}>
                    <ChevronLeft size={24} />
                </button>
                <div className="hymn-indicator">
                    <span className="number">{hymnNumber}장</span>
                    <span className="label">Hymn {hymnNumber}</span>
                </div>
                <button className="menu-btn" onClick={(e) => { e.stopPropagation(); onToggleSidebar(); }}>
                    <Menu size={24} />
                </button>
            </header>

            <div className="viewer-content">
                {status === 'loading' && <div className="loading-spinner">Loading Hymn...</div>}
                {status === 'error' && <div className="error-msg">Hymn not found</div>}
                <img
                    key={hymnNumber}
                    src={imagePath}
                    alt={`Hymn ${hymnNumber}`}
                    className={`hymn-image ${status === 'loading' ? 'hidden' : ''}`}
                    onLoad={handleLoad}
                    onError={handleError}
                    style={{ display: status === 'loaded' ? 'block' : 'none' }}
                />
            </div>

            {/* Floating Navigation (Bottom) */}
            <div className={`floating-nav ${isNavVisible ? '' : 'nav-hidden'}`} onClick={(e) => e.stopPropagation()}>
                <button
                    onClick={(e) => handleNavAction(e, onPrev)}
                    disabled={hymnNumber <= 1}
                    className="float-btn"
                >
                    <ChevronLeft size={28} />
                </button>
                <button
                    onClick={(e) => handleNavAction(e, onNext)}
                    disabled={hymnNumber >= 645}
                    className="float-btn"
                >
                    <ChevronRight size={28} />
                </button>
            </div>
        </div>
    );
};

export default HymnViewer;
