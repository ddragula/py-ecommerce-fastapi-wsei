import React from 'react';
import './Content.css';

export const Content: React.FC<React.PropsWithChildren> = (props) => {
    return (
        <div className="Content-container">
            {props.children}
        </div>
    );
}
