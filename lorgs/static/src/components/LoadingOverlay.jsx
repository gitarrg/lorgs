import React from 'react'



export default function LoadingOverlay() {
    return (
        <div className="loading_overlay h1 shadow">
            <i className="fas fa-circle-notch fa-spin"></i>
            <span> loading..</span>
        </div>
    )
}
