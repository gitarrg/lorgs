import type Boss from '../../types/boss'
import type Role from '../../types/role'
import type Spec from '../../types/spec'


export default function Icon({
    spec,
    className="",
    size="m",
    alt=""
} : {
    spec: Spec | Role | Boss
    className?: string,
    size?: "xs" | "s" | "m" | "l",
    alt?: string,
} ) {

    // @ts-ignore
    const name_slug = spec.code ?? spec.class.name_slug


    return (
        <img
            className={`icon-${size} rounded wow-border-${name_slug} ${className}`}
            src={spec.icon_path}
            alt={alt}
        />
    )
}
