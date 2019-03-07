//import * as process from "babel-core";

const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

//require('bulma/bulma.sass');

module.exports = {
    entry: './src/app.js',
    output: {
        filename: 'js/main.js',
        path: path.resolve(__dirname, 'assets'),
        publicPath: 'assets'
    },
    module: {
        rules: [
                {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            }, {
                test: /\.js$/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            presets: ["@babel/preset-env"]
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: "css/[name].css",
            chunkFilename: "css/[id].css"
        })
    ],
    watch: true
};