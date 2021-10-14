
// Imports
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const path = require("path")

// Constants
const DEBUG = process.env.NODE_ENV !== "production";


// Config
module.exports = {

    mode: process.env.NODE_ENV || 'development',

    entry: {
        app: path.resolve(__dirname, "lorgs/frontend/App.tsx"),
        style: path.resolve(__dirname, "lorgs/templates/scss/main.scss"),
    },

    resolve: {
        extensions: [".tsx", ".ts", "jsx", ".js"]
    },

    // modules that will be loaded externally
    externals: {
        'react': 'React',
        'react-dom': "ReactDOM",
        'konva': 'Konva',
        "redux": "Redux",
        'react-redux': "ReactRedux",
        'react-hook-form': "ReactHookForm",
        "reselect": "Reselect",
    },

    module: {
        rules: [

            {
                test: /\.[tj]sx?$/,  // jsx, tsx, js and ts
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ["@babel/react", "@babel/preset-typescript"]
                    }
                }
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",   // Translates CSS into CommonJS
                    "sass-loader"   // Compiles Sass to CSS
                ]
            }
        ]
    },

    output: {
        path: path.resolve(__dirname, "lorgs/static/_generated"),
        filename: '[name].js',
        chunkFilename: '[name].[contenthash].bundle.js',
    },

    // for testing
    optimization: {

        usedExports: true,  // tree shacking

        splitChunks: {
            cacheGroups: {
                // group for all the node modules
                vendors: {
                    test: /[\\/]node_modules[\\/]/,
                    name: "vendor",
                    chunks: "all",
                }
            }
        },

        minimize: process.env.NODE_ENV == "production",
        minimizer: [new TerserPlugin({
            terserOptions: {
                compress: {
                    drop_console: true,
                }
            }
        })],
    },

    plugins: [
        new MiniCssExtractPlugin(),
        // new BundleAnalyzerPlugin(),
    ],
}
