


export default function FormGroup({name, className="", children}) {
    // 
    return (
        <div className="search-group">
            <h4 className="mb-0">{name}</h4>
            <div className={`bg-dark p-1 rounded border ${className}`}>
                {children}
            </div>
        </div>
    )
}
