
// Imports
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
const CopyPlugin = require("copy-webpack-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const TerserPlugin = require("terser-webpack-plugin")
const path = require("path")

const variables = require("./variables.js")

// Constants
const DEBUG = process.env.NODE_ENV !== "production";


// Config
module.exports = {

    mode: process.env.NODE_ENV || 'development',

    /***************************************************************************
     * Input
     */
    entry: {
        app: path.resolve(__dirname, "frontend/src/App.tsx"),
        style: path.resolve(__dirname, "frontend/scss/main.scss"),
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
        "reselect": "Reselect",
    },


    /***************************************************************************
     * Output
     */
    output: {
        path: path.resolve(__dirname, "static"),
        filename: '[name].js',
        chunkFilename: DEBUG ? '[name].bundle.js' : '[name].[contenthash].bundle.js',
        publicPath: "/static/",

        clean: true, // Clean the output directory before emit.
    },


    /***************************************************************************
     * Rules
     */

    module: {
        rules: [

            /************ Javascript ************/
            {
                test: /\.[tj]sx?$/,  // jsx, tsx, js and ts
                include: path.resolve(__dirname, "frontend/src"),
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ["@babel/react", "@babel/preset-typescript"]
                    }
                }
            },

            /********** global CSS/SCSS *********/
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, "frontend/scss"),
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",  // Translates CSS into CommonJS
                    "sass-loader"   // Compiles Sass to CSS
                ]
            },

            /********* CSS/SCSS Modules *********/
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, "frontend/src"),
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",  // Translates CSS into CommonJS
                        options: {
                            importLoaders: 1,
                            modules: {
                                localIdentName: DEBUG ? "[name]__[local]__[hash:base64:4]" : "[hash:base64:8]",
                            }
                        }
                    },
                    "sass-loader"   // Compiles Sass to CSS
                ]
            },
        ]
    },


    /***************************************************************************
     * Plugins
     */
    plugins: [
        new MiniCssExtractPlugin({
            filename: DEBUG ? "[name].bundle.css" : "[name].[contenthash].bundle.css",
        }),

        new CopyPlugin({
            patterns: [{
                from: "frontend/public",
                // to: "", // into the root
                globOptions: {
                    ignore: ["**/index.html"]
                }
            }],
        }),

        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, "frontend/public/index.html"),
            minimize: !DEBUG,
            hash: true, // append cache busting hash
            inject: 'body',

            templateParameters: {
                ...variables.get_vars(process.env.NODE_ENV),
                DEBUG: DEBUG,
            },
        }),

        new BundleAnalyzerPlugin({
            analyzerMode: 'disabled', // will be used via CLI
            // generateStatsFile: true,
        }),
    ],


    /***************************************************************************
     * Optimization
     */
    optimization: {

        usedExports: true,  // tree shacking

        // fix some dev server issues
        runtimeChunk: DEBUG ? 'single' : "false",

        minimize: !DEBUG,
        minimizer: [new TerserPlugin({
            terserOptions: {
                compress: {
                    drop_console: true,
                }
            }
        })],
    },


    /***************************************************************************
     * Dev Server Config
     */
    devServer: {

        port: 9001,

        static: {
            directory: path.join(__dirname, "/frontend/public"),
            publicPath: "/static",       // as "/"
        },

        historyApiFallback: {
            index: '/static/index.html'
        }
    }
}
