const path = require('path');

module.exports = {
    entry: './frontend_src/app.js',
    output: {
        'filename': 'main.js',
        path: path.resolve(__dirname, 'backend_src/static_gen')
    },
    externals: {
        jquery: 'jQuery'
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: [/node_modules/, /venv/],
                loader: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    },
};
