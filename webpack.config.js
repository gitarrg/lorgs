
// Imports
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const path = require("path")

// Constants
const DEBUG = process.env.NODE_ENV !== "production";


// Config
module.exports = {

    mode: process.env.NODE_ENV || 'development',

    entry: {
        // main: path.resolve(__dirname, "lorgs/static/main.js"),
        app: path.resolve(__dirname, "lorgs/frontend/App.jsx"),
        style: path.resolve(__dirname, "lorgs/templates/scss/main.scss"),
    },

    // modules that will be loaded externally
    externals: {
        'react': 'React',
        'konva': 'Konva',
        "redux": "Redux",
        'react-redux': "ReactRedux",
    },

    module: {
        rules: [

            {
                test: /\.jsx$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/react']
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
    },

    // for testing
    optimization: {
        minimize: process.env.NODE_ENV == "production",
        minimizer: [new TerserPlugin({
            terserOptions: {
                compress: {
                    // drop_console: true,
                }
            }
        })],
    },

    plugins: [
        new MiniCssExtractPlugin(),
    ],

}
