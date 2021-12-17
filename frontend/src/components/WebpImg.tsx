

interface WebpImgProps {
    src: string

    [x: string]: any;
}

export default function WebpImg({src, ...props} : WebpImgProps) {

    const webp = src.substr(0, src.lastIndexOf(".")) + ".webp";

    return (
        <picture>
            <source srcSet={webp} type="image/webp" />
            <img src={src} {...props} />
        </picture>
    );
};
