import { NavLink } from 'react-router-dom';
import { get_spec } from "../../store/specs";
import { useAppSelector } from '../../store/store_hooks';
import WebpImg from '../WebpImg';


export default function NavBarSpecButton({ spec_slug } : {spec_slug: string}) {


    const mode = useAppSelector(state => state.ui.mode);
    const boss_slug : string = useAppSelector(state => state.ui.boss_slug);
    const spec = useAppSelector(state => get_spec(state, spec_slug));

    if (!spec) { return <p>nope: {spec_slug}</p>; }

    const class_name = spec.class.name_slug;
    const link = `/${mode}/${spec.full_name_slug}/${boss_slug}`;

    // Render
    return (

        <NavLink to={link} className={`wow-${class_name}`} activeClassName="active">
            <WebpImg
                className={`mr-1 icon-spec icon-m rounded wow-border-${class_name}`}
                src={spec.icon_path}
                alt={spec.full_name}
                title={spec.full_name} />
            <span className={`wow-${class_name}`}>
                {spec.full_name}
            </span>
        </NavLink>
    );
}
