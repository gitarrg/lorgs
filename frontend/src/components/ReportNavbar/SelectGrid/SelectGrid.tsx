import type { ReactNode } from "react"


type SelectGridProps = {
    title?: string
    children: ReactNode
}


export default function SelectGrid({title="", children} : SelectGridProps) {
    return (
        <div className="flex-grow-1">
            {title && <h4 className="mb-1">{title}</h4>}
            <div className="d-flex flex-column gap-2">
                {children}
            </div>
        </div>
    )
}
