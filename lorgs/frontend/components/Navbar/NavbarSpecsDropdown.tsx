import NavBarSpecButton from './NavBarSpecButton';


export default function NavbarSpecsDropdown({ specs } : { specs: string[] }) {

    const specs_sorted = [...specs].sort();

    return (
        <div className="nav_dropdown__content specs_nav_dropdown bg-dark border rounded">
            <div className="p-2 d-grid gap-1">
                {specs_sorted.map(spec_slug => <NavBarSpecButton key={spec_slug} spec_slug={spec_slug} />
                )}
            </div>
        </div>
    );
}
