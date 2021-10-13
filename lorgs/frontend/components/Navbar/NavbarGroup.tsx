

export default function NavbarGroup({children, className}) {

    if (!children) return null
    return (
        <div className={`navbar_group p-1 bg-dark border rounded ${className || ""}`}>
            {children}
        </div>
    )
}
