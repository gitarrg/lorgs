export default function FormGroup({title="", children}) {
    return (
        <div>
            {title && <h4 className="mb-0">{title}</h4>}
            <div className="bg-dark rounded p-2">
                {children}
            </div>
        </div>
    )
}
