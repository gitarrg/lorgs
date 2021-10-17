
// Imports
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
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


    /***************************************************************************
     * Output
     */
    output: {
        path: path.resolve(__dirname, "lorgs/static/_generated"),
        filename: '[name].js',
        chunkFilename: '[name].[contenthash].bundle.js',
        publicPath: "/static/_generated/",
    },


    /***************************************************************************
     * Rules
     */

    module: {
        rules: [

            /************ Javascript ************/
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

            /********** global CSS/SCSS *********/
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, "lorgs/templates/scss"),
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",  // Translates CSS into CommonJS
                    "sass-loader"   // Compiles Sass to CSS
                ]
            },

            /********* CSS/SCSS Modules *********/
            {
                test: /\.scss$/,
                exclude: path.resolve(__dirname, "lorgs/templates/scss"),
                use: [
                    MiniCssExtractPlugin.loader,
                    // "style-loader",
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
            filename: "[name].[contenthash].bundle.css",
        }),

        new HtmlWebpackPlugin({
            template: "lorgs/templates/index.html",
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
            generateStatsFile: true,
        }),
    ],


    /***************************************************************************
     * Optimization
     */
    optimization: {

        usedExports: true,  // tree shacking

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
            directory: path.join(__dirname, "lorgs/static"),
            publicPath: "/static",       // as "/"
        },

        historyApiFallback: {
            index: '/static/_generated/index.html'
        }
    }
}
