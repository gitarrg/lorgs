import type Boss from '../../types/boss'
import type Role from '../../types/role'
import type Spec from '../../types/spec'
import type Class from '../../types/class'
import WebpImg from "../WebpImg"


export default function Icon({
    spec,
    className="",
    size="m",
    alt=""
} : {
    spec: Spec | Class | Role | Boss
    className?: string,
    size?: "xs" | "s" | "m" | "l",
    alt?: string,
} ) {

    // @ts-ignore
    const name_slug = spec.code ?? spec.class?.name_slug ?? spec.name_slug


    return (
        <WebpImg
            className={`icon-${size} rounded wow-border-${name_slug} ${className}`}
            src={spec.icon_path}
            alt={alt}
        />
    )
}
