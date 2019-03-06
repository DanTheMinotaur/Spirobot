const path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var extractPlugin = new ExtractTextPlugin({
    filename: 'main.css'
});

//require('bulma/bulma.sass');

module.exports = {
    entry: './src/app.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'assets/js')
    },
    module: {
        rules: [
                {
                test: /\.scss$/,
                use: extractPlugin.extract({
                    use: ['css-loader', 'scss-loader']
                })
            }, {
                test: /\.js$/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            presets: ["es2015"]
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        extractPlugin
    ],
    watch: true
};