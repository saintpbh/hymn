
import React, { useState } from 'react';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import './Sidebar.css';

const RANGES = [
    { label: '1-100', start: 1, end: 100 },
    { label: '101-200', start: 101, end: 200 },
    { label: '201-300', start: 201, end: 300 },
    { label: '301-400', start: 301, end: 400 },
    { label: '401-500', start: 401, end: 500 },
    { label: '501-600', start: 501, end: 600 },
    { label: '601-645', start: 601, end: 645 },
];

const Sidebar = ({ onSelectHymn, currentHymnNumber, isOpen, onClose }) => {
    const [expandedRange, setExpandedRange] = useState(null);

    const toggleRange = (label) => {
        setExpandedRange(expandedRange === label ? null : label);
    };

    const handleHymnClick = (number) => {
        onSelectHymn(number);
        if (window.innerWidth < 768) {
            onClose(); // Close sidebar on mobile after selection
        }
    };

    return (
        <>
            {/* Overlay for mobile */}
            <div
                className={`sidebar-overlay ${isOpen ? 'open' : ''}`}
                onClick={onClose}
            />

            <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <h2>Hymn Index</h2>
                    <button className="close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                <div className="sidebar-content">
                    {RANGES.map((range) => (
                        <div key={range.label} className="range-group">
                            <button
                                className={`range-btn ${expandedRange === range.label ? 'active' : ''}`}
                                onClick={() => toggleRange(range.label)}
                            >
                                <span className="range-label">{range.label}</span>
                                {expandedRange === range.label ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                            </button>

                            <div className={`hymn-grid ${expandedRange === range.label ? 'expanded' : ''}`}>
                                {Array.from({ length: range.end - range.start + 1 }, (_, i) => range.start + i).map((num) => (
                                    <button
                                        key={num}
                                        className={`hymn-num-btn ${currentHymnNumber === num ? 'current' : ''}`}
                                        onClick={() => handleHymnClick(num)}
                                    >
                                        {num}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </aside>
        </>
    );
};

export default Sidebar;
