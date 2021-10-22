export default function FormGroup({title="", children}) {
    return (
        <div>
            {title && <h4 className="mb-0">{title}</h4>}
            <div className="">
                {children}
            </div>
        </div>
    )
}
