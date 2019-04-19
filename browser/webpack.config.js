//import * as process from "babel-core";

const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = (env, args) => ({
    entry: './src/app.js',
    output: {
        filename: 'js/app.js',
        path: path.resolve(__dirname, 'assets'),
        publicPath: 'assets'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: "babel-loader"
            },
            {
                test: /\.scss$/,
                use: [
                    args.mode === 'production' ? MiniCssExtractPlugin.loader : "style-loader",
                    "css-loader",
                    'resolve-url-loader',
                    "sass-loader?sourceMap"
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
});