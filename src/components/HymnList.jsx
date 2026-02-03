
import React, { useState, useMemo, useRef, useEffect } from 'react';
import './HymnList.css';
import { Search, Menu } from 'lucide-react';

const HymnList = ({ hymnsData, onSelectHymn, onToggleSidebar }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const inputRef = useRef(null);

    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.focus();
        }
    }, []);

    const handleSearchChange = (e) => {
        const val = e.target.value;
        const lastChar = val.slice(-1);

        // Handle special dialer keys
        if (lastChar === '*' || lastChar === '#') {
            const numberStr = val.slice(0, -1);
            const number = parseInt(numberStr, 10);

            // Visual feedback: show '장'
            setSearchTerm(numberStr + '장');

            // Find match and navigate
            if (!isNaN(number)) {
                onSelectHymn(number);
            }
            return;
        }

        setSearchTerm(val);
    };

    const filteredHymns = useMemo(() => {
        if (!searchTerm) return hymnsData;
        const lower = searchTerm.toLowerCase();
        // Clean numeric search for better matching (ignore '장')
        const numericSearch = lower.replace(/[^0-9]/g, '');

        return hymnsData.filter(h => {
            // If term is purely numeric (or "123장"), match number exactly or partially
            if (numericSearch && h.number.toString().includes(numericSearch)) return true;
            // Title match
            return h.title.toLowerCase().includes(lower);
        });
    }, [hymnsData, searchTerm]);

    return (
        <div className="hymn-list-container">
            <div className="search-bar-container">
                <div className="search-input-wrapper">
                    <Search size={20} className="search-icon" />
                    <input
                        ref={inputRef}
                        type="tel"
                        placeholder="장 또는 가사로 검색하세요."
                        value={searchTerm}
                        onChange={handleSearchChange}
                        className="search-input"
                    />
                </div>
                <button
                    onClick={onToggleSidebar}
                    style={{
                        background: 'none',
                        border: 'none',
                        marginLeft: '12px',
                        cursor: 'pointer',
                        color: 'var(--text-charcoal)'
                    }}
                    aria-label="Menu"
                >
                    <Menu size={24} />
                </button>
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
