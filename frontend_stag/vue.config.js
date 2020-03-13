module.exports = {
  publicPath: "/stag/static",
  outputDir: '../stag',
  productionSourceMap: false,
  pwa: {
    name: 'Bloomingmath',
    themeColor: '#334',
    msTileColor: '#334',
    manifestOptions: {
      background_color: '#334'
    }
  },
  devServer: {
    // public: "127.0.0.1",
    contentBase: "src",
    compress: true,
    port: 8080,
    watchOptions: {
      poll: true,
    },
    proxy: {
      "/contents": {
        target: "http://localhost:8000",
        changeOrigin: true,
        timeout: 5000
      },
      "/users": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/groups": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/nodes": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  },
}