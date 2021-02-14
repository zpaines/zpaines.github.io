const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = {
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'bundle.[contenthash].js',
    path: path.resolve(__dirname),
  },
  mode: 'development',
  plugins: [new HtmlWebpackPlugin({
    title: 'index.html',
    template: 'src/your_league.html',
    inject: 'body',
  })],
};
