
import React, { useState, useMemo } from 'react';
import './HymnList.css';
import { Search } from 'lucide-react';

const HymnList = ({ hymnsData, onSelectHymn }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const filteredHymns = useMemo(() => {
        if (!searchTerm) return hymnsData;
        const lower = searchTerm.toLowerCase();
        return hymnsData.filter(h =>
            h.number.toString().includes(lower) ||
            h.title.toLowerCase().includes(lower)
        );
    }, [hymnsData, searchTerm]);

    return (
        <div className="hymn-list-container">
            <div className="search-bar-container">
                <div className="search-input-wrapper">
                    <Search size={20} className="search-icon" />
                    <input
                        type="text"
                        placeholder="Search hymn number or title..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>
            </div>

            <div className="list-content">
                {filteredHymns.length === 0 ? (
                    <div className="empty-state">No hymns found</div>
                ) : (
                    <ul className="hymn-items">
                        {filteredHymns.map((hymn) => (
                            <li key={hymn.number} onClick={() => onSelectHymn(hymn.number)}>
                                <div className="hymn-item">
                                    <span className="hymn-number">{hymn.number}</span>
                                    <span className="hymn-title-text">{hymn.title}</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default HymnList;
